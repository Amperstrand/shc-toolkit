"""
SHC User API client.

Full coverage of the SHC v2 User API: VM lifecycle, ordering, snapshots,
backups, SSH keys, billing, support tickets, account management, firewall,
metrics, ISO, reverse DNS, affiliate, and more.
Base URL: https://blesta.sovereignhybridcompute.com/user-api/v2
"""

from __future__ import annotations

import json
import logging
import os
import socket
import time
from datetime import datetime, timezone
from typing import Any

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://blesta.sovereignhybridcompute.com/user-api/v2"


class SHCError(Exception):
    """API error with code, message, and request_id for support."""

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str | None = None,
        details: Any = None,
    ):
        self.code = code
        self.message = message
        self.request_id = request_id
        self.details = details
        self.confirmation_id: str | None = None
        super().__init__(
            f"[{code}] {message}"
            + (f" (req={request_id})" if request_id else "")
        )


class ProvisioningStuckError(SHCError):
    """VM stuck in a terminal failure pattern during provisioning.

    The full health report dict is attached as ``.health_report``.
    """

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str | None = None,
        details: Any = None,
    ):
        super().__init__(code, message, request_id, details)
        self.health_report = details


class SHCClient:
    """Lightweight client for the SHC User API.

    Usage:
        c = SHCClient()  # reads SHC_API_KEY from env
        vms = c.list_vms()
        summary = c.get_vm_summary(123)

    Auth: Bearer token (API key from /account/api-keys).
    """

    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL):
        self.api_key = api_key or os.environ.get("SHC_API_KEY", "")
        if not self.api_key:
            raise ValueError("SHC_API_KEY not set and no api_key provided")
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.api_key}"

    # ── Internal ─────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if "json" in kwargs:
            self.session.headers["Content-Type"] = "application/json"
        elif "Content-Type" in self.session.headers:
            del self.session.headers["Content-Type"]

        resp = self.session.request(method, url, **kwargs)
        text = resp.text
        json_start = text.find("{")
        if json_start > 0:
            text = text[json_start:]
        import json as _json
        body = _json.loads(text) if text.strip() else {}
        if not resp.ok:
            err = body.get("error", {})
            exc = SHCError(
                err.get("code", "unknown"),
                err.get("message", resp.text),
                err.get("request_id"),
                err.get("details"),
            )
            # Capture confirmation_id from 409 body so _confirmed_request
            # can auto-resubmit without a second round-trip.
            conf = body.get("confirmation", {})
            if conf:
                exc.confirmation_id = (
                    conf.get("structuredContent", {}).get("confirmation_id")
                )
            raise exc
        return body.get("data", body)

    def call(self, method: str, path: str, **kwargs) -> Any:
        """Call any SHC API endpoint directly.

        Escape hatch for endpoints not yet wrapped in a named method.
        Uses the same auth, base URL, and response unwrapping as all
        typed methods.

        Examples:
            c.call("GET", "/vm/123/metrics")
            c.call("POST", "/support/tickets", json={"subject": "Bug"})
            c.call("PATCH", "/vm/123/firewall/policy", json={"default_policy": "DROP"})
        """
        return self._request(method.upper(), path, **kwargs)

    def _get(self, path: str, params: dict | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    def _post(self, path: str, data: dict | None = None, **kwargs) -> dict[str, Any]:
        return self._request("POST", path, json=data or {}, **kwargs)

    def _patch(self, path: str, data: dict | None = None, **kwargs) -> dict[str, Any]:
        return self._request("PATCH", path, json=data or {}, **kwargs)

    def _put(self, path: str, data: dict | None = None, **kwargs) -> dict[str, Any]:
        return self._request("PUT", path, json=data or {}, **kwargs)

    def _delete(self, path: str, **kwargs) -> dict[str, Any]:
        return self._request("DELETE", path, **kwargs)

    def _confirmed_request(
        self, method: str, path: str, *, confirm: bool = True, **kwargs
    ) -> dict[str, Any]:
        """Execute a request, auto-handling the confirmation_required 409 flow.

        On confirmation_required, extracts the single-use confirmation_id
        and resubmits with X-User-Api-Confirm header.  Pass confirm=False
        to probe (will raise SHCError on 409 instead of auto-confirming).
        """
        try:
            return self._request(method, path, **kwargs)
        except SHCError as e:
            if not confirm or e.code != "confirmation_required":
                raise
            cid = getattr(e, "confirmation_id", None)
            if not cid:
                raise
            headers = dict(kwargs.pop("headers", None) or {})
            headers["X-User-Api-Confirm"] = cid
            return self._request(method, path, headers=headers, **kwargs)

    # ── Account ──────────────────────────────────────────────

    def get_account(self) -> dict:
        return self._get("/account")

    def update_account(self, **kwargs) -> dict:
        return self._patch("/account", kwargs)

    def update_contact(self, **kwargs) -> dict:
        return self._patch("/account/contact", kwargs)

    def change_password(self, current: str, new: str) -> dict:
        return self._post("/account/password", {"current_password": current, "new_password": new})

    def get_2fa_status(self) -> dict:
        return self._get("/account/2fa")

    def get_account_activity(self, limit: int = 20, offset: int = 0) -> dict:
        return self._get("/account/activity", params={"limit": limit, "offset": offset})

    def get_preferences(self) -> dict:
        return self._get("/account/preferences")

    def update_preferences(self, **kwargs) -> dict:
        return self._patch("/account/preferences", kwargs)

    def get_autodebit(self) -> dict:
        return self._get("/account/autodebit")

    def get_credit_handling(self) -> dict:
        return self._get("/account/credit-handling")

    def set_credit_handling(self, **kwargs) -> dict:
        return self._put("/account/credit-handling", kwargs)

    def add_credit(self, amount: str, currency: str = "USD", idempotency_key: str | None = None) -> dict:
        import uuid
        idem = idempotency_key or f"credit-{uuid.uuid4().hex[:24]}"
        return self._post("/account/credit", {
            "amount": amount,
            "currency": currency,
            "idempotency_key": idem,
        })

    def get_account_balance(self) -> dict:
        return self._get("/account/balance")

    # ── API Keys ─────────────────────────────────────────────

    def list_api_keys(self) -> list[dict]:
        return self._get("/account/api-keys").get("items", [])

    def create_api_key(self, method_scope: str = "full", area_subset: list[str] | None = None,
                       expires_in_days: int | None = None, label: str = "") -> dict:
        data: dict[str, Any] = {"method_scope": method_scope, "label": label}
        if area_subset:
            data["area_subset"] = area_subset
        if expires_in_days:
            data["expires_in_days"] = expires_in_days
        return self._post("/account/api-keys", data)

    def revoke_api_key(self, key_id: str) -> dict:
        return self._delete(f"/account/api-keys/{key_id}")

    # ── Contacts ─────────────────────────────────────────────

    def list_contacts(self) -> list[dict]:
        return self._get("/contacts").get("items", [])

    def create_contact(self, **kwargs) -> dict:
        return self._post("/contacts", kwargs)

    def get_contact(self, contact_id: int) -> dict:
        return self._get(f"/contacts/{contact_id}")

    def delete_contact(self, contact_id: int) -> dict:
        return self._delete(f"/contacts/{contact_id}")

    def list_contact_permissions(self) -> list[dict]:
        return self._get("/contacts/permission-options").get("items", [])

    # ── Support Tickets ──────────────────────────────────────

    def list_support_departments(self) -> list[dict]:
        return self._get("/support/departments").get("items", [])

    def list_support_tickets(self, limit: int = 20, offset: int = 0) -> dict:
        return self._get("/support/tickets", params={"limit": limit, "offset": offset})

    def get_support_ticket(self, ticket_id: int) -> dict:
        return self._get(f"/support/tickets/{ticket_id}")

    def create_support_ticket(self, subject: str, message: str, department_id: int,
                              priority: str = "medium", service_id: int | None = None,
                              **kwargs) -> dict:
        data: dict[str, Any] = {"subject": subject, "message": message,
                                "department_id": department_id, "priority": priority}
        if service_id:
            data["service_id"] = service_id
        data.update(kwargs)
        return self._post("/support/tickets", data)

    def reply_support_ticket(self, ticket_id: int, message: str) -> dict:
        return self._post(f"/support/tickets/{ticket_id}/replies", {"message": message})

    def close_support_ticket(self, ticket_id: int) -> dict:
        return self._post(f"/support/tickets/{ticket_id}/close")

    # ── Knowledge Base ───────────────────────────────────────

    def list_kb_articles(self) -> list[dict]:
        return self._get("/kb").get("items", [])

    def search_kb(self, query: str) -> list[dict]:
        return self._get("/kb/search", params={"q": query}).get("items", [])

    def get_kb_article(self, article_id: int) -> dict:
        return self._get(f"/kb/{article_id}")

    # ── Account Managers ─────────────────────────────────────

    def list_managed_accounts(self) -> list[dict]:
        return self._get("/managed-accounts").get("items", [])

    def list_managers(self) -> list[dict]:
        return self._get("/managers").get("items", [])

    def invite_manager(self, email: str, permissions: list[str] | None = None) -> dict:
        data: dict[str, Any] = {"email": email}
        if permissions:
            data["permissions"] = permissions
        return self._post("/managers", data)

    def list_manager_permissions(self) -> list[dict]:
        return self._get("/managers/permission-options").get("items", [])

    def get_billing_balance(self) -> dict:
        return self._get("/billing/balance")

    # ── Billing & Payments ───────────────────────────────────

    def list_invoices(self, **params) -> dict:
        return self._get("/invoices", params=params if params else None)

    def get_invoice(self, invoice_id: int) -> dict:
        return self._get(f"/invoices/{invoice_id}")

    def get_invoice_pdf_url(self, invoice_id: int) -> str:
        return f"{self.base_url}/invoices/{invoice_id}/pdf"

    def pay_invoice(self, invoice_id: int, idempotency_key: str) -> dict:
        return self._post(
            f"/payment/{invoice_id}/checkout",
            {"gateway": "btcpay_server", "idempotency_key": idempotency_key},
        )

    def get_payment(self, invoice_id: int) -> dict:
        return self._get(f"/payment/{invoice_id}")

    def list_payment_methods(self) -> list[dict]:
        return self._get("/payment-methods").get("items", [])

    def list_transactions(self, limit: int = 20, offset: int = 0) -> dict:
        return self._get("/transactions", params={"limit": limit, "offset": offset})

    def get_transaction(self, transaction_id: str) -> dict:
        return self._get(f"/transactions/{transaction_id}")

    def list_emails(self, limit: int = 20, offset: int = 0) -> dict:
        return self._get("/emails", params={"limit": limit, "offset": offset})

    def get_email(self, email_id: int) -> dict:
        return self._get(f"/emails/{email_id}")

    # ── Quotations ───────────────────────────────────────────

    def list_quotations(self) -> list[dict]:
        return self._get("/quotations").get("items", [])

    def get_quotation(self, quotation_id: int) -> dict:
        return self._get(f"/quotations/{quotation_id}")

    def get_quotation_invoices(self, quotation_id: int) -> list[dict]:
        return self._get(f"/quotations/{quotation_id}/invoices").get("items", [])

    # ── Affiliate ────────────────────────────────────────────

    def get_affiliate_overview(self) -> dict:
        return self._get("/affiliate")

    def enroll_affiliate(self) -> dict:
        return self._post("/affiliate/enroll")

    def get_affiliate_payout_destination(self) -> dict:
        return self._get("/affiliate/payout-destination")

    def set_affiliate_payout_destination(self, **kwargs) -> dict:
        return self._put("/affiliate/payout-destination", kwargs)

    def list_affiliate_payouts(self) -> list[dict]:
        return self._get("/affiliate/payouts").get("items", [])

    def request_affiliate_payout(self, amount: str, currency: str = "BTC") -> dict:
        return self._post("/affiliate/payouts", {"amount": amount, "currency": currency})

    def list_affiliate_referrals(self) -> list[dict]:
        return self._get("/affiliate/referrals").get("items", [])

    # ── Ordering ─────────────────────────────────────────────

    def get_catalog(self) -> list[dict]:
        return self._get("/ordering/catalog").get("items", [])

    def preview_order(self, **kwargs) -> dict:
        return self._post("/ordering/preview", kwargs)

    def submit_order(self, idempotency_key: str | None = None, *, include_dev_vps_options: bool = True, **kwargs) -> dict:
        """Submit a VM order with auto-confirmation and idempotency.

        Removes invalid 'pay' field, omits empty config_options, generates
        an Idempotency-Key if none provided, and auto-handles confirmation.

        When include_dev_vps_options is True (default) and the caller has not
        already supplied order_form_id/options, injects the Dev VPS defaults
        (order_form_id=11, template=debian13-cloud, ipv4=none). Without these
        options SHC's Proxmox layer does not know which template to deploy and
        the VM sits in ``pending`` indefinitely.
        """
        import uuid
        kwargs.pop("pay", None)
        if "config_options" in kwargs and not kwargs["config_options"]:
            del kwargs["config_options"]
        if include_dev_vps_options and "config_options" not in kwargs and "options" not in kwargs:
            kwargs.setdefault("order_form_id", 11)
        idem = idempotency_key or f"order-{uuid.uuid4().hex[:24]}"
        headers = {"Idempotency-Key": idem}
        return self._confirmed_request(
            "POST", "/ordering/submit", json=kwargs, headers=headers
        )

    # ── VM Lifecycle ─────────────────────────────────────────

    def list_vms(self) -> list[dict]:
        return self._get("/vm").get("items", [])

    def get_vm(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}")

    def get_vm_summary(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/summary")

    def start_vm(self, service_id: int) -> dict:
        return self._patch(f"/vm/{service_id}/start")

    def stop_vm(self, service_id: int) -> dict:
        return self._patch(f"/vm/{service_id}/stop")

    def restart_vm(self, service_id: int) -> dict:
        return self._patch(f"/vm/{service_id}/restart")

    def shutdown_vm(self, service_id: int) -> dict:
        return self._patch(f"/vm/{service_id}/shutdown")

    def reset_vm(self, service_id: int) -> dict:
        return self._patch(f"/vm/{service_id}/reset")

    def cancel_vm(self, service_id: int, *, immediate: bool = True, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/cancel", confirm=confirm,
            json={"immediate": True} if immediate else {},
        )

    def reinstall_vm(self, service_id: int, *, confirm: bool = True, **kwargs) -> dict:
        return self._confirmed_request(
            "PATCH", f"/vm/{service_id}/reinstall", confirm=confirm, json=kwargs
        )

    def get_vm_detail(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/detail")

    def get_vm_activity(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/activity").get("items", [])

    def get_vm_metrics(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/metrics")

    def get_vm_bandwidth(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/bandwidth")

    def get_vm_network(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/network")

    def upgrade_vm(self, service_id: int, package_id: int) -> dict:
        return self._patch(f"/vm/{service_id}/upgrade", {"package_id": package_id})

    def preview_upgrade(self, service_id: int, package_id: int) -> dict:
        return self._post(f"/vm/{service_id}/upgrade/preview", {"package_id": package_id})

    def list_upgrade_options(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/upgrade-options").get("items", [])

    def get_vm_payments(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/payments").get("items", [])

    def get_vm_renewal_quote(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/renew")

    # ── Snapshots ────────────────────────────────────────────

    def list_snapshots(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/snapshots").get("items", [])

    def create_snapshot(self, service_id: int, name: str | None = None) -> dict:
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        return self._post(f"/vm/{service_id}/snapshots", data)

    def restore_snapshot(self, service_id: int, snapshot_id: str, *, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/snapshots/restore",
            confirm=confirm, json={"snapshot_id": snapshot_id},
        )

    def delete_snapshot(self, service_id: int, snapshot_id: str, *, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/snapshots/delete",
            confirm=confirm, json={"snapshot_id": snapshot_id},
        )

    # ── Backups ──────────────────────────────────────────────

    def list_backups(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/backups").get("items", [])

    def create_backup(self, service_id: int, name: str | None = None) -> dict:
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        return self._post(f"/vm/{service_id}/backups", data)

    def restore_backup(self, service_id: int, backup_id: str, *, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/backups/restore",
            confirm=confirm, json={"backup_id": backup_id},
        )

    def delete_backup(self, service_id: int, backup_id: str, *, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/backups/delete",
            confirm=confirm, json={"backup_id": backup_id},
        )

    def set_backup_protection(self, service_id: int, backup_id: str, protected: bool) -> dict:
        return self._patch(f"/vm/{service_id}/backups/protection", {"backup_id": backup_id, "protected": protected})

    def get_backup_restore_hints(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/backups/restore-hints")

    def list_file_restore_sources(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/file-restore/sources").get("items", [])

    def browse_file_restore(self, service_id: int, source: str, path: str = "/") -> list[dict]:
        return self._get(f"/vm/{service_id}/file-restore/list", params={"source": source, "path": path}).get("items", [])

    def get_data_preferences(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/data-preferences")

    def set_data_preferences(self, service_id: int, **kwargs) -> dict:
        return self._patch(f"/vm/{service_id}/data-preferences", kwargs)

    def get_vm_credentials(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/credentials")

    # ── SSH Keys ─────────────────────────────────────────────

    def list_ssh_keys(self, service_id: int | None = None) -> list[dict]:
        items = self._get("/ssh-key").get("items", [])
        if service_id:
            return [k for k in items if k.get("service_id") == service_id]
        return items

    def add_ssh_key(self, service_id: int, public_key: str, label: str = "") -> dict:
        return self._post(
            f"/vm/{service_id}/ssh-keys",
            {"public_key": public_key, "label": label},
        )

    def set_stored_ssh_key(self, service_id: int, public_key: str) -> dict:
        return self._post("/ssh-key", {"service_id": service_id, "public_key": public_key})

    def delete_stored_ssh_key(self, service_id: int) -> dict:
        return self._delete("/ssh-key", params={"service_id": service_id})

    def apply_ssh_key_live(self, service_id: int, public_key: str) -> dict:
        return self._post(f"/vm/{service_id}/ssh-keys/apply-live", {"ssh_key": public_key})

    def remove_ssh_key_live(self, service_id: int, public_key: str) -> dict:
        return self._delete(f"/vm/{service_id}/ssh-keys/live", params={"public_key": public_key})

    # ── Firewall ─────────────────────────────────────────────

    def get_firewall(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/firewall")

    def set_firewall_policy(self, service_id: int, policy: str) -> dict:
        return self._patch(f"/vm/{service_id}/firewall/policy", {"default_policy": policy})

    def create_firewall_rule(self, service_id: int, **kwargs) -> dict:
        return self._post(f"/vm/{service_id}/firewall/rules", kwargs)

    def edit_firewall_rule(self, service_id: int, position: int, **kwargs) -> dict:
        return self._patch(f"/vm/{service_id}/firewall/rules/{position}", kwargs)

    def delete_firewall_rule(self, service_id: int, position: int) -> dict:
        return self._confirmed_request("DELETE", f"/vm/{service_id}/firewall/rules/{position}")

    # ── ISO ──────────────────────────────────────────────────

    def list_isos(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/iso").get("items", [])

    def mount_iso(self, service_id: int, iso_id: str) -> dict:
        return self._post(f"/vm/{service_id}/iso/mount", {"iso_id": iso_id})

    def unmount_iso(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/iso/unmount")

    # ── Reverse DNS ──────────────────────────────────────────

    def list_rdns(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/rdns").get("items", [])

    def set_rdns(self, service_id: int, ip: str, ptr: str) -> dict:
        return self._post(f"/vm/{service_id}/rdns", {"ip": ip, "ptr": ptr})

    def clear_rdns(self, service_id: int, ip: str) -> dict:
        return self._delete(f"/vm/{service_id}/rdns", params={"ip": ip})

    # ── Console ──────────────────────────────────────────────

    def get_console_availability(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/console")

    def create_console_session(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/console/session")

    # ── Templates ────────────────────────────────────────────

    def list_templates(self) -> list[dict]:
        return self._get("/vm/templates").get("items", [])

    def list_images(self) -> list[dict]:
        return self._get("/image").get("items", [])

    # ── Jobs ─────────────────────────────────────────────────

    def list_jobs(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/jobs").get("items", [])

    def get_job(self, service_id: int, job_id: str) -> dict:
        return self._get(f"/vm/{service_id}/jobs/{job_id}")

    # ── Billing ──────────────────────────────────────────────

    def list_invoices(self) -> list[dict]:
        return self._get("/invoices").get("items", [])

    def get_invoice(self, invoice_id: int) -> dict:
        return self._get(f"/invoices/{invoice_id}")

    def pay_invoice(self, invoice_id: int, idempotency_key: str) -> dict:
        """Pay an invoice via BTCPay. Returns checkout info or paid status."""
        return self._post(
            f"/payment/{invoice_id}/checkout",
            {
                "gateway": "btcpay_server",
                "idempotency_key": idempotency_key,
            },
        )

    # ── Wait / Poll ──────────────────────────────────────────

    def wait_for_provisioning(
        self, service_id: int, timeout: int = 300, interval: int = 10
    ) -> dict:
        """Poll until VM is running and SSH-able.

        Note: provisioning_state may lag behind actual availability.
        Also checks service_status == 'active' and IP assignment.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            vm = self.get_vm(service_id)
            svc = vm.get("service_status", "unknown")
            prov = vm.get("provisioning_state", "unknown")
            ips = vm.get("ips", [])
            log.info(
                f"VM {service_id}: service={svc}, provisioning={prov}, ips={len(ips)}"
            )
            if svc == "active" and ips:
                return vm
            if prov in ("failed", "error"):
                raise SHCError("provisioning_failed", f"VM provisioning failed: {vm}")
            time.sleep(interval)
        raise SHCError("timeout", f"VM {service_id} not ready after {timeout}s")

    def wait_for_job(
        self, service_id: int, job_id: str, timeout: int = 600, interval: int = 10
    ) -> dict:
        """Poll a job until it completes."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            job = self.get_job(service_id, job_id)
            status = job.get("status", "unknown")
            log.info(f"Job {job_id}: {status}")
            if status in ("completed", "succeeded"):
                return job
            if status in ("failed", "error"):
                raise SHCError("job_failed", f"Job {job_id} failed: {job}")
            time.sleep(interval)
        raise SHCError("timeout", f"Job {job_id} not complete after {timeout}s")

    # ── VM Health ───────────────────────────────────────────

    _TERMINAL_DIAGNOSES = frozenset({
        "CLOUD_INIT_DISABLED_DEADLOCK",
        "NETWORK_UNREACHABLE",
        "EMPTY_ACTIVITY_LOG",
    })

    def check_vm_health(self, service_id: int) -> dict:
        """Return a structured health report diagnosing common failure patterns.

        Gathers data from /vm, /vm/detail, /vm/summary, /firewall,
        /activity, and /bandwidth, probes TCP port 22, and classifies
        the VM's state into a diagnosis_code.
        """
        vm = self.get_vm(service_id)
        # Prefer /detail over /summary for runtime status: /summary omits
        # the runtime object entirely (returns null runtime_status even
        # when the VM is actually running — confirmed API bug).
        detail = self.get_vm_detail(service_id)
        summary = self.get_vm_summary(service_id)
        firewall = self.get_firewall(service_id)
        activity = self.get_vm_activity(service_id)
        bandwidth = self.get_vm_bandwidth(service_id)

        hostname = vm.get("hostname", "")
        service_status = vm.get("service_status", "unknown")
        provisioning_state = vm.get("provisioning_state", "unknown")
        bootstrap_completed_at = vm.get("bootstrap_completed_at")

        runtime_status_summary = summary.get("runtime_status")
        rt = detail.get("runtime") or {}
        runtime_status_detail = rt.get("raw_status") or rt.get("state")
        runtime_field_consistent = (
            runtime_status_summary == runtime_status_detail
        )

        ips = vm.get("ips", [])
        ip_assigned = ips[0]["ip"] if ips else None

        port_22_reachable = False
        if ip_assigned:
            try:
                s = socket.create_connection((ip_assigned, 22), timeout=3)
                s.close()
                port_22_reachable = True
            except OSError:
                pass

        age_seconds = self._compute_vm_age(vm, bandwidth)

        activity_count = len(activity)
        bandwidth_used = bandwidth.get("used_bytes", 0)

        diagnosis_code, diagnosis = self._diagnose(
            provisioning_state=provisioning_state,
            bootstrap_completed_at=bootstrap_completed_at,
            age_seconds=age_seconds,
            runtime_field_consistent=runtime_field_consistent,
            ip_assigned=ip_assigned,
            port_22_reachable=port_22_reachable,
            runtime_status_detail=runtime_status_detail,
            activity_count=activity_count,
        )

        return {
            "service_id": service_id,
            "hostname": hostname,
            "age_seconds": age_seconds,
            "service_status": service_status,
            "provisioning_state": provisioning_state,
            "bootstrap_completed_at": bootstrap_completed_at,
            "runtime_status_summary": runtime_status_summary,
            "runtime_status_detail": runtime_status_detail,
            "runtime_field_consistent": runtime_field_consistent,
            "ip_assigned": ip_assigned,
            "port_22_reachable": port_22_reachable,
            "firewall_policy": firewall.get("policy", {}),
            "activity_events": activity_count,
            "bandwidth_used_bytes": bandwidth_used,
            "diagnosis": diagnosis,
            "diagnosis_code": diagnosis_code,
        }

    @staticmethod
    def _compute_vm_age(vm: dict, bandwidth: dict) -> int:
        """Estimate VM age in seconds from date_created.

        Handles server-side timezone offset bug where date_created can
        be hours ahead of real UTC; falls back to bandwidth as_of epoch,
        then to abs(delta) so stuck VMs always report a large age.
        """
        date_created = vm.get("date_created")
        if not date_created:
            return 0
        try:
            created = datetime.fromisoformat(date_created)
        except (ValueError, TypeError):
            return 0
        now = datetime.now(timezone.utc)
        delta = int((now - created).total_seconds())
        if delta >= 0:
            return delta
        as_of_epoch = bandwidth.get("as_of_epoch")
        if as_of_epoch:
            delta2 = int(as_of_epoch - created.timestamp())
            if delta2 >= 0:
                return delta2
        return abs(delta)

    @staticmethod
    def _diagnose(
        *,
        provisioning_state: str,
        bootstrap_completed_at: str | None,
        age_seconds: int,
        runtime_field_consistent: bool,
        ip_assigned: str | None,
        port_22_reachable: bool,
        runtime_status_detail: str | None,
        activity_count: int,
    ) -> tuple[str, str]:
        """Classify VM state into a (diagnosis_code, diagnosis) tuple."""
        if (
            provisioning_state == "provisioning"
            and bootstrap_completed_at is None
            and age_seconds > 300
        ):
            return (
                "CLOUD_INIT_DISABLED_DEADLOCK",
                "VM stuck in provisioning; cloud-init likely disabled or "
                "failed. Bootstrap signal never fired.",
            )
        if not runtime_field_consistent:
            return (
                "RUNTIME_FIELD_DIVERGENCE",
                "API field inconsistency: /summary and /detail disagree on "
                "runtime_status. Use /detail.",
            )
        if (
            ip_assigned
            and not port_22_reachable
            and runtime_status_detail == "running"
        ):
            return (
                "NETWORK_UNREACHABLE",
                "VM is running and has an IP assigned, but port 22 is "
                "unreachable from outside. Likely network/bridge/hypervisor "
                "issue.",
            )
        if activity_count == 0 and age_seconds > 600:
            return (
                "EMPTY_ACTIVITY_LOG",
                "No activity events recorded despite VM age > 10min. "
                "Observability gap.",
            )
        if provisioning_state == "ready" and port_22_reachable:
            return ("HEALTHY", "VM is healthy and SSH-reachable.")
        if provisioning_state == "provisioning" and age_seconds <= 300:
            return (
                "PROVISIONING_IN_PROGRESS",
                "VM is still provisioning (within normal timeframe).",
            )
        return ("UNKNOWN", "No specific diagnosis matched.")

    def wait_for_provisioning_healthy(
        self,
        service_id: int,
        timeout: int = 300,
        interval: int = 10,
        *,
        probe_port_22: bool = True,
    ) -> dict:
        """Poll until VM is healthy or a terminal failure is detected.

        Returns the VM dict on success.  Raises ProvisioningStuckError
        (with .health_report) when check_vm_health returns a terminal
        diagnosis code.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            health = self.check_vm_health(service_id)
            code = health["diagnosis_code"]
            log.info(
                f"VM {service_id} health: {code} "
                f"(prov={health['provisioning_state']}, "
                f"ssh={health['port_22_reachable']})"
            )
            if code in self._TERMINAL_DIAGNOSES:
                raise ProvisioningStuckError(
                    "provisioning_stuck",
                    f"VM {service_id}: {health['diagnosis']}",
                    details=health,
                )
            if health["provisioning_state"] == "ready":
                if probe_port_22 and not health["port_22_reachable"]:
                    raise ProvisioningStuckError(
                        "provisioning_stuck",
                        f"VM {service_id} provisioned but port 22 "
                        f"unreachable.",
                        details=health,
                    )
                return self.get_vm(service_id)
            time.sleep(interval)
        health = self.check_vm_health(service_id)
        raise SHCError(
            "timeout",
            f"VM {service_id} not healthy after {timeout}s "
            f"(last diagnosis: {health['diagnosis_code']})",
            details=health,
        )
