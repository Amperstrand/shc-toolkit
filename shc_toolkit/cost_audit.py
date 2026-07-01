"""Cost tracking and invoice auditing for SHC VM sessions.

Records expected costs at order time (from catalog pricing), verifies actual
invoice amounts match, and audits refunds at cancel time against expected
hourly proration.

All verification is best-effort: if the API is unavailable or returns
unexpected data, the tracker logs a debug message and continues. It never
blocks an operation.

Usage:
    The tracker is automatically instantiated on every SHCClient. To
    access reports:

        c = SHCClient()
        vm = c.order_vm(hostname="test", size="nvme-2c-8gb")
        # ... use the VM ...
        report = c.cost_tracker.session_report(vm["service_id"])
        print(report)
        c.cancel_vm(vm["service_id"])
        cancel_report = c.cost_tracker.audit_cancel(vm["service_id"])
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
    invoice_id: int | None = None
    invoice_amount: float | None = None
    invoice_verified: bool = False


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
    actual_refund: float | None = None
    invoice_amount: float | None = None
    mismatch: bool = False
    notes: list[str] = field(default_factory=list)

    @property
    def hourly_rate(self) -> float:
        return self.daily_price / 24

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
            "actual_refund": self.actual_refund,
            "invoice_amount": self.invoice_amount,
            "mismatch": self.mismatch,
            "notes": self.notes,
        }


class CostTracker:
    """Track expected vs actual costs for SHC VM sessions."""

    def __init__(self, client: SHCClient) -> None:
        self._client = client
        self._sessions: dict[int, CostSession] = {}

    def track_order(
        self,
        service_id: int,
        package_id: int,
        invoice_id: int | None = None,
    ) -> CostSession:
        """Record expected cost at order time and verify invoice.

        Called automatically by SHCClient.order_vm(). Can also be called
        manually for orders placed via submit_order().
        """
        daily_price = self._client.estimate_daily_cost(package_id)
        session = CostSession(
            service_id=service_id,
            package_id=package_id,
            daily_price=daily_price,
            ordered_at=datetime.now(timezone.utc),
            invoice_id=invoice_id,
        )
        self._sessions[service_id] = session

        log.info(
            "Cost audit: tracking service %s (pkg %s) — expected $%.2f/day ($%.4f/hr)",
            service_id, package_id, daily_price, daily_price / 24,
        )

        if invoice_id:
            self._verify_invoice(session)

        return session

    def _verify_invoice(self, session: CostSession) -> None:
        """Fetch the invoice and compare its total to the expected daily price."""
        try:
            inv = self._client.get_invoice(session.invoice_id)
            raw_total = (
                inv.get("total")
                or inv.get("amount")
                or inv.get("paid")
                or inv.get("line_total", {}).get("total")
                or 0
            )
            actual = abs(float(raw_total))
            session.invoice_amount = actual

            diff = abs(actual - session.daily_price)
            session.invoice_verified = diff <= PRICE_TOLERANCE_USD

            if session.invoice_verified:
                log.info(
                    "Cost audit: invoice %s verified — $%.2f matches expected daily price",
                    session.invoice_id, actual,
                )
            else:
                log.warning(
                    "Cost audit: invoice %s MISMATCH for service %s — "
                    "expected $%.2f, actual $%.2f (diff $%+.2f)",
                    session.invoice_id, session.service_id,
                    session.daily_price, actual, actual - session.daily_price,
                )
        except Exception as exc:
            log.debug(
                "Cost audit: could not verify invoice %s: %s",
                session.invoice_id, exc,
            )

    def audit_cancel(self, service_id: int) -> CostReport | None:
        """At cancel time, compute expected vs actual cost and refund.

        Called automatically by SHCClient.cancel_vm(). Returns a CostReport
        with the full session cost breakdown.
        """
        session = self._sessions.get(service_id)
        if not session:
            log.debug("Cost audit: no tracked session for service %s", service_id)
            return None

        now = datetime.now(timezone.utc)
        duration = now - session.ordered_at
        hours = duration.total_seconds() / 3600

        hourly_rate = session.daily_price / 24
        expected_cost = round(max(hours, MIN_CHARGE_HOURS) * hourly_rate, 4)
        expected_refund = round(session.daily_price - expected_cost, 4)

        report = CostReport(
            service_id=service_id,
            package_id=session.package_id,
            daily_price=session.daily_price,
            ordered_at=session.ordered_at,
            canceled_at=now,
            duration_hours=round(hours, 2),
            expected_cost=expected_cost,
            expected_refund=max(expected_refund, 0.0),
            invoice_amount=session.invoice_amount,
        )

        self._check_actual_refund(session, report)

        if report.mismatch:
            log.warning(
                "Cost audit: session %s — %.1f hrs, expected cost $%.4f, "
                "expected refund $%.4f, actual refund $%.4f — MISMATCH",
                service_id, hours, expected_cost,
                expected_refund, report.actual_refund,
            )
        else:
            log.info(
                "Cost audit: session %s — %.1f hrs, net cost $%.4f, refund $%.4f",
                service_id, hours, expected_cost,
                report.actual_refund if report.actual_refund is not None else expected_refund,
            )

        return report

    def _check_actual_refund(self, session: CostSession, report: CostReport) -> None:
        """Try to determine the actual refund from payment records."""
        try:
            payments = self._client.get_vm_payments(session.service_id)
        except Exception as exc:
            log.debug("Cost audit: could not fetch payments: %s", exc)
            report.notes.append("payment_fetch_failed")
            return

        refunds = []
        charges = []
        for p in payments:
            amount = float(p.get("amount", 0))
            if amount < 0:
                refunds.append(abs(amount))
            elif amount > 0:
                charges.append(amount)

        if refunds:
            report.actual_refund = round(sum(refunds), 4)
            diff = abs(report.actual_refund - report.expected_refund)
            if diff > PRICE_TOLERANCE_USD:
                report.mismatch = True
                report.notes.append(
                    f"refund_diff_${report.actual_refund - report.expected_refund:+.4f}"
                )

        if charges and not refunds:
            report.notes.append("no_refund_recorded_yet")

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
            "invoice_id": session.invoice_id,
            "invoice_amount": session.invoice_amount,
            "invoice_verified": session.invoice_verified,
        }

    def all_sessions(self) -> list[dict]:
        """Cost reports for all tracked sessions."""
        return [
            self.session_report(sid)
            for sid in self._sessions
            if sid is not None
        ]
