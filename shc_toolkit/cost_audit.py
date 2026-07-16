"""Cost tracking and balance-diff auditing for SHC VM sessions.

Records session metadata at order time and performs the single authoritative
audit at cancel time, when the actual charge + refund have settled.

SHC uses post-pay billing: credit is NOT deducted at order time. The charge
appears asynchronously via the billing cycle. Attempting to audit at order
time produces false mismatches ($0.00 diff vs expected daily price).

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
HOURLY_PRECISION = 4
PRICE_TOLERANCE_USD = 0.01


@dataclass
class CostSession:
    service_id: int
    package_id: int
    daily_price: float
    ordered_at: datetime
    credit_before_order: float | None = None


@dataclass
class CostReport:
    service_id: int
    package_id: int
    daily_price: float
    ordered_at: datetime
    canceled_at: datetime
    duration_hours: float
    expected_cost: float
    actual_net_cost: float | None = None
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
            "actual_net_cost": self.actual_net_cost,
            "mismatch": self.mismatch,
            "notes": self.notes,
        }


class CostTracker:
    """Track session metadata at order time; audit at cancel time.

    The ONLY audit happens at cancel, comparing the full-lifecycle balance
    diff (credit_before_order - credit_after_cancel) to the expected
    prorated cost. This avoids false mismatches from post-pay billing.
    """

    def __init__(self, client: SHCClient) -> None:
        self._client = client
        self._sessions: dict[int, CostSession] = {}

    def track_order(
        self,
        service_id: int,
        package_id: int,
        credit_before: float | None = None,
    ) -> CostSession:
        """Record session metadata at order time. No audit — just tracking.

        Args:
            service_id: The VM service ID.
            package_id: The package ordered.
            credit_before: Credit balance snapshot from before the order,
                used later at cancel time for the full-lifecycle diff.
        """
        daily_price = self._client.estimate_daily_cost(package_id)
        session = CostSession(
            service_id=service_id,
            package_id=package_id,
            daily_price=daily_price,
            ordered_at=datetime.now(timezone.utc),
            credit_before_order=credit_before,
        )
        self._sessions[service_id] = session
        log.info(
            "Cost audit: tracking svc %s — $%.2f/day",
            service_id, daily_price,
        )
        return session

    def audit_cancel(
        self,
        service_id: int,
        credit_after_cancel: float | None = None,
    ) -> CostReport | None:
        """Single authoritative audit at cancel time.

        Computes the full-lifecycle net cost as the balance diff between
        credit_before_order and credit_after_cancel, then compares to the
        expected prorated cost.

        Args:
            service_id: The VM service ID.
            credit_after_cancel: Credit balance snapshot from after cancel.
                None if balance couldn't be captured.
        """
        session = self._sessions.get(service_id)
        if not session:
            log.debug("Cost audit: no tracked session for svc %s", service_id)
            return None

        now = datetime.now(timezone.utc)
        hours = (now - session.ordered_at).total_seconds() / 3600

        hourly_rate = round(session.daily_price / 24, HOURLY_PRECISION)
        charged_hours = max(hours, MIN_CHARGE_HOURS)
        expected_cost = _truncate(charged_hours * hourly_rate, 2)

        actual_net_cost = None
        if (
            session.credit_before_order is not None
            and credit_after_cancel is not None
        ):
            actual_net_cost = round(
                session.credit_before_order - credit_after_cancel, 2
            )

        report = CostReport(
            service_id=service_id,
            package_id=session.package_id,
            daily_price=session.daily_price,
            ordered_at=session.ordered_at,
            canceled_at=now,
            duration_hours=round(hours, 2),
            expected_cost=expected_cost,
            actual_net_cost=actual_net_cost,
        )

        if actual_net_cost is not None:
            diff = abs(actual_net_cost - expected_cost)
            if diff <= PRICE_TOLERANCE_USD:
                log.info(
                    "Cost audit: svc %s — %.1f hrs, net $%.2f, expected $%.2f — OK",
                    service_id, hours, actual_net_cost, expected_cost,
                )
            else:
                report.mismatch = True
                report.notes.append(f"net_cost_diff_${actual_net_cost - expected_cost:+.2f}")
                ledger_cost = self._ledger_cost(service_id)
                if ledger_cost is not None and abs(ledger_cost - expected_cost) <= PRICE_TOLERANCE_USD:
                    report.mismatch = False
                    report.notes.append("ledger_confirms_expected_concurrent_balance_noise")
                    log.info(
                        "Cost audit: svc %s — balance diff $%.2f ≠ expected $%.2f, "
                        "but ledger confirms $%.2f — concurrent activity, OK",
                        service_id, actual_net_cost, expected_cost, ledger_cost,
                    )
                elif ledger_cost is not None:
                    log.warning(
                        "Cost audit: svc %s — MISMATCH: net $%.2f, ledger $%.2f, expected $%.2f",
                        service_id, actual_net_cost, ledger_cost, expected_cost,
                    )
                else:
                    log.warning(
                        "Cost audit: svc %s — MISMATCH: net $%.2f, expected $%.2f (diff $%+.2f)",
                        service_id, actual_net_cost, expected_cost,
                        actual_net_cost - expected_cost,
                    )
        else:
            report.notes.append("balance_diff_unavailable")
            log.info(
                "Cost audit: svc %s — %.1f hrs, expected $%.2f (balance diff unavailable)",
                service_id, hours, expected_cost,
            )

        del self._sessions[service_id]
        return report

    def _ledger_cost(self, service_id: int) -> float | None:
        """Sum of all charges for this VM from the per-VM payment ledger."""
        try:
            payments = self._client.get_vm_payments(service_id)
        except Exception as exc:
            log.debug("Cost audit: ledger fetch failed for svc %s: %s", service_id, exc)
            return None

        charges = []
        for p in payments:
            for field_name in ("total", "paid", "amount"):
                raw = p.get(field_name)
                if raw is None:
                    continue
                try:
                    val = float(raw)
                except (TypeError, ValueError):
                    continue
                if val > 0:
                    charges.append(val)
                    break
        return round(sum(charges), 2) if charges else 0.0

    def current_burn(self, service_id: int) -> float:
        """Current expected cost for a running VM (does not call the API)."""
        session = self._sessions.get(service_id)
        if not session:
            return 0.0
        elapsed = datetime.now(timezone.utc) - session.ordered_at
        hours = elapsed.total_seconds() / 3600
        hourly_rate = round(session.daily_price / 24, HOURLY_PRECISION)
        return _truncate(max(hours, MIN_CHARGE_HOURS) * hourly_rate, 2)

    def session_report(self, service_id: int) -> dict | None:
        """Full cost report for a tracked session (VM may still be running)."""
        session = self._sessions.get(service_id)
        if not session:
            return None

        now = datetime.now(timezone.utc)
        hours = (now - session.ordered_at).total_seconds() / 3600
        hourly_rate = round(session.daily_price / 24, HOURLY_PRECISION)
        expected_cost = _truncate(max(hours, MIN_CHARGE_HOURS) * hourly_rate, 2)

        return {
            "service_id": session.service_id,
            "package_id": session.package_id,
            "daily_price": session.daily_price,
            "hourly_rate": round(hourly_rate, 6),
            "ordered_at": session.ordered_at.isoformat(),
            "elapsed_hours": round(hours, 2),
            "current_expected_cost": expected_cost,
        }

    def all_sessions(self) -> list[dict]:
        """Cost reports for all tracked sessions."""
        return [
            self.session_report(sid)
            for sid in self._sessions
            if sid is not None
        ]


def _truncate(amount: float, decimals: int) -> float:
    factor = 10 ** decimals
    return float(int(amount * factor)) / factor
