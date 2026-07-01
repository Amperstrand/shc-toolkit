"""Cost tracking and balance-diff auditing for SHC VM sessions.

Captures credit balance before and after each order/cancel, computes the
**diff** (never logs or stores the absolute balance), and compares it to
the expected cost based on catalog pricing and hourly proration.

All verification is best-effort: if the API is unavailable, the tracker
logs a debug message and continues. It never blocks an operation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import SHCClient

log = logging.getLogger("shc.cost")

MIN_CHARGE_HOURS = 1.0
PRICE_TOLERANCE_USD = 0.02


@dataclass
class CostSession:
    service_id: int
    package_id: int
    daily_price: float
    ordered_at: datetime
    actual_charge: float | None = None
    charge_verified: bool = False


@dataclass
class CostReport:
    service_id: int
    package_id: int
    daily_price: float
    ordered_at: datetime
    canceled_at: datetime
    duration_hours: float
    expected_cost: float
    expected_refund: float
    actual_charge: float | None = None
    actual_refund: float | None = None
    ledger_refund: float | None = None
    mismatch: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "service_id": self.service_id,
            "package_id": self.package_id,
            "daily_price": self.daily_price,
            "ordered_at": self.ordered_at.isoformat(),
            "canceled_at": self.canceled_at.isoformat(),
            "duration_hours": round(self.duration_hours, 2),
            "expected_cost": self.expected_cost,
            "expected_refund": self.expected_refund,
            "actual_charge": self.actual_charge,
            "actual_refund": self.actual_refund,
            "ledger_refund": self.ledger_refund,
            "net_cost": self._net_cost(),
            "mismatch": self.mismatch,
            "notes": self.notes,
        }

    def _net_cost(self) -> float | None:
        charge = self.actual_charge if self.actual_charge is not None else self.daily_price
        refund = self.actual_refund or 0.0
        return round(charge - refund, 4)


class CostTracker:
    """Track expected vs actual costs via balance diffs.

    Absolute balance is NEVER stored or logged — only the diff between
    before and after snapshots.
    """

    def __init__(self, client: SHCClient) -> None:
        self._client = client
        self._sessions: dict[int, CostSession] = {}

    def track_order(
        self,
        service_id: int,
        package_id: int,
        actual_charge: float | None = None,
    ) -> CostSession:
        """Record expected cost at order time and verify via balance diff.

        Args:
            service_id: The VM service ID.
            package_id: The package ordered.
            actual_charge: Credit diff (before - after) from the order.
                None if balance couldn't be captured.
        """
        daily_price = self._client.estimate_daily_cost(package_id)
        session = CostSession(
            service_id=service_id,
            package_id=package_id,
            daily_price=daily_price,
            ordered_at=datetime.now(timezone.utc),
            actual_charge=actual_charge,
        )
        self._sessions[service_id] = session

        if actual_charge is not None:
            diff = abs(actual_charge - daily_price)
            session.charge_verified = diff <= PRICE_TOLERANCE_USD
            if session.charge_verified:
                log.info(
                    "Cost audit: order svc %s — charged $%.4f, expected $%.4f — OK",
                    service_id, actual_charge, daily_price,
                )
            else:
                log.warning(
                    "Cost audit: order svc %s — CHARGE MISMATCH: "
                    "charged $%.4f, expected $%.4f (diff $%+.4f)",
                    service_id, actual_charge, daily_price,
                    actual_charge - daily_price,
                )
        else:
            log.info(
                "Cost audit: tracking svc %s — expected $%.4f/day (balance diff unavailable)",
                service_id, daily_price,
            )

        return session

    def audit_cancel(
        self,
        service_id: int,
        actual_refund: float | None = None,
    ) -> CostReport | None:
        """At cancel time, compare actual refund diff to expected proration.

        Args:
            service_id: The VM service ID.
            actual_refund: Credit diff (after - before) from the cancel.
                None if balance couldn't be captured.
        """
        session = self._sessions.get(service_id)
        if not session:
            log.debug("Cost audit: no tracked session for svc %s", service_id)
            return None

        now = datetime.now(timezone.utc)
        hours = (now - session.ordered_at).total_seconds() / 3600

        hourly_rate = session.daily_price / 24
        expected_cost = round(max(hours, MIN_CHARGE_HOURS) * hourly_rate, 4)
        expected_refund = round(max(session.daily_price - expected_cost, 0.0), 4)

        report = CostReport(
            service_id=service_id,
            package_id=session.package_id,
            daily_price=session.daily_price,
            ordered_at=session.ordered_at,
            canceled_at=now,
            duration_hours=round(hours, 2),
            expected_cost=expected_cost,
            expected_refund=expected_refund,
            actual_charge=session.actual_charge,
            actual_refund=actual_refund,
        )

        if actual_refund is not None:
            diff = abs(actual_refund - expected_refund)
            if diff > PRICE_TOLERANCE_USD:
                ledger_refund = self._ledger_refund(service_id)
                if ledger_refund is not None and abs(ledger_refund - expected_refund) <= PRICE_TOLERANCE_USD:
                    report.mismatch = False
                    report.notes.append("balance_diff_noisy_concurrent_activity")
                    report.ledger_refund = ledger_refund
                    log.info(
                        "Cost audit: cancel svc %s — balance diff $%.4f ≠ expected $%.4f, "
                        "but per-VM ledger confirms $%.4f — concurrent activity, OK",
                        service_id, actual_refund, expected_refund, ledger_refund,
                    )
                elif ledger_refund is not None:
                    report.mismatch = True
                    report.notes.append("ledger_confirms_mismatch")
                    report.ledger_refund = ledger_refund
                    log.warning(
                        "Cost audit: cancel svc %s — REFUND MISMATCH confirmed by ledger: "
                        "balance diff $%.4f, ledger $%.4f, expected $%.4f",
                        service_id, actual_refund, ledger_refund, expected_refund,
                    )
                else:
                    report.mismatch = True
                    report.notes.append(
                        f"refund_diff_${actual_refund - expected_refund:+.4f}"
                    )
                    log.warning(
                        "Cost audit: cancel svc %s — REFUND MISMATCH: "
                        "refunded $%.4f, expected $%.4f (diff $%+.4f)",
                        service_id, actual_refund, expected_refund,
                        actual_refund - expected_refund,
                    )
            else:
                log.info(
                    "Cost audit: cancel svc %s — refunded $%.4f, expected $%.4f — OK",
                    service_id, actual_refund, expected_refund,
                )
        else:
            report.notes.append("refund_diff_unavailable")

        charge_str = (
            f"${session.actual_charge:.4f}" if session.actual_charge is not None else "?"
        )
        refund_str = (
            f"${actual_refund:.4f}" if actual_refund is not None else "?"
        )
        net = report._net_cost()
        log.info(
            "Cost audit: session svc %s — %.1f hrs, charged %s, refunded %s, net $%.4f",
            service_id, hours, charge_str, refund_str, net,
        )

        return report

    def _ledger_refund(self, service_id: int) -> float | None:
        """Look up per-VM ledger to isolate this VM's refund from concurrent activity.

        Returns the sum of negative (credit/refund) entries, or None if the
        ledger can't be fetched.
        """
        try:
            payments = self._client.get_vm_payments(service_id)
        except Exception as exc:
            log.debug("Cost audit: ledger fetch failed for svc %s: %s", service_id, exc)
            return None

        refunds = []
        for p in payments:
            for field_name in ("total", "paid", "amount"):
                raw = p.get(field_name)
                if raw is None:
                    continue
                try:
                    val = float(raw)
                except (TypeError, ValueError):
                    continue
                if val < 0:
                    refunds.append(abs(val))
                    break
        return round(sum(refunds), 4) if refunds else 0.0

    def current_burn(self, service_id: int) -> float:
        """Current expected cost for a running VM (does not call the API)."""
        session = self._sessions.get(service_id)
        if not session:
            return 0.0
        elapsed = datetime.now(timezone.utc) - session.ordered_at
        hours = elapsed.total_seconds() / 3600
        return round(max(hours, MIN_CHARGE_HOURS) * session.daily_price / 24, 4)

    def session_report(self, service_id: int) -> dict | None:
        """Full cost report for a tracked session (VM may still be running)."""
        session = self._sessions.get(service_id)
        if not session:
            return None

        now = datetime.now(timezone.utc)
        hours = (now - session.ordered_at).total_seconds() / 3600
        hourly_rate = session.daily_price / 24
        expected_cost = round(max(hours, MIN_CHARGE_HOURS) * hourly_rate, 4)

        return {
            "service_id": session.service_id,
            "package_id": session.package_id,
            "daily_price": session.daily_price,
            "hourly_rate": round(hourly_rate, 6),
            "ordered_at": session.ordered_at.isoformat(),
            "elapsed_hours": round(hours, 2),
            "current_expected_cost": expected_cost,
            "actual_charge": session.actual_charge,
            "charge_verified": session.charge_verified,
        }

    def all_sessions(self) -> list[dict]:
        """Cost reports for all tracked sessions."""
        return [
            self.session_report(sid)
            for sid in self._sessions
            if sid is not None
        ]
