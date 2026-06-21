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
import time
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
        self.request_id = request_id
        self.details = details
        super().__init__(
            f"[{code}] {message}"
            + (f" (req={request_id})" if request_id else "")
        )


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
        body = resp.json()
        if not resp.ok:
            err = body.get("error", {})
            raise SHCError(
                err.get("code", "unknown"),
                err.get("message", resp.text),
                err.get("request_id"),
                err.get("details"),
            )
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

    def add_credit(self, amount: str, currency: str = "USD") -> dict:
        return self._post("/account/credit", {"amount": amount, "currency": currency})

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

    def create_support_ticket(self, subject: str, body: str, department_id: int | None = None,
                              priority: str = "medium", service_id: int | None = None) -> dict:
        data: dict[str, Any] = {"subject": subject, "body": body, "priority": priority}
        if department_id:
            data["department_id"] = department_id
        if service_id:
            data["service_id"] = service_id
        return self._post("/support/tickets", data)

    def reply_support_ticket(self, ticket_id: int, body: str) -> dict:
        return self._post(f"/support/tickets/{ticket_id}/replies", {"body": body})

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

    def submit_order(self, idempotency_key: str | None = None, **kwargs) -> dict:
        """Submit a VM order. Handles confirmation flow automatically.

        Args:
            idempotency_key: Optional client-generated idempotency key.
                If omitted, one is generated. Use a deterministic key
                (e.g. hash of commit+branch+mode) to prevent duplicate
                orders when retrying failed tests.
            **kwargs: Order fields (package_id, pricing_id, hostname, etc.)

        Automatically:
        - Removes invalid 'pay' field (not in v2 schema)
        - Omits empty config_options
        - Handles the confirmation_required flow (409 → confirm → resubmit)
        """
        import uuid
        kwargs.pop("pay", None)
        if "config_options" in kwargs and not kwargs["config_options"]:
            del kwargs["config_options"]
        if not idempotency_key:
            idem = f"order-{uuid.uuid4().hex[:24]}"
        else:
            idem = idempotency_key

        headers = {"Idempotency-Key": idem}
        try:
            return self._post("/ordering/submit", kwargs, headers=headers)
        except SHCError as e:
            if e.code != "confirmation_required":
                raise
            cid = None
            if isinstance(e.details, list):
                for d in e.details:
                    if isinstance(d, dict) and "confirmation_id" in str(d.get("issue", "")):
                        pass
            if not cid:
                import requests as req_lib
                r = req_lib.post(
                    f"{self.base_url}/ordering/submit",
                    json=kwargs,
                    headers={**headers, "Authorization": f"Bearer {self.api_key}"},
                )
                body = r.json()
                sc = body.get("confirmation", {}).get("structuredContent", {})
                cid = sc.get("confirmation_id")
            if not cid:
                raise
            headers["X-User-Api-Confirm"] = cid
            return self._post("/ordering/submit", kwargs, headers=headers)

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

    def cancel_vm(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/cancel")

    def reinstall_vm(self, service_id: int, **kwargs) -> dict:
        return self._patch(f"/vm/{service_id}/reinstall", kwargs)

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

    def restore_snapshot(self, service_id: int, snapshot_id: str) -> dict:
        return self._post(
            f"/vm/{service_id}/snapshots/restore", {"snapshot_id": snapshot_id}
        )

    def delete_snapshot(self, service_id: int, snapshot_id: str) -> dict:
        return self._post(
            f"/vm/{service_id}/snapshots/delete", {"snapshot_id": snapshot_id}
        )

    # ── Backups ──────────────────────────────────────────────

    def list_backups(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/backups").get("items", [])

    def create_backup(self, service_id: int, name: str | None = None) -> dict:
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        return self._post(f"/vm/{service_id}/backups", data)

    def restore_backup(self, service_id: int, backup_id: str) -> dict:
        return self._post(f"/vm/{service_id}/backups/restore", {"backup_id": backup_id})

    def delete_backup(self, service_id: int, backup_id: str) -> dict:
        return self._post(f"/vm/{service_id}/backups/delete", {"backup_id": backup_id})

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

    # ── SSH Keys ─────────────────────────────────────────────

    def list_ssh_keys(self, service_id: int | None = None) -> list[dict]:
        if service_id:
            return self._get(f"/vm/{service_id}/ssh-keys").get("items", [])
        return self._get("/ssh-key").get("items", [])

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
        return self._post(f"/vm/{service_id}/ssh-keys/apply-live", {"public_key": public_key})

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
        return self._delete(f"/vm/{service_id}/firewall/rules/{position}")

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
