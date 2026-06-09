"""
SHC User API client.

Supports VM lifecycle, ordering, snapshots, SSH keys, and billing.
Base URL: https://blesta.sovereignhybridcompute.com/user-api/v1
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://blesta.sovereignhybridcompute.com/user-api/v1"


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
        # Only set Content-Type when sending a body
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

    def _get(self, path: str) -> dict[str, Any]:
        return self._request("GET", path)

    def _post(self, path: str, data: dict | None = None) -> dict[str, Any]:
        return self._request("POST", path, json=data or {})

    def _patch(self, path: str, data: dict | None = None) -> dict[str, Any]:
        return self._request("PATCH", path, json=data or {})

    def _delete(self, path: str) -> dict[str, Any]:
        return self._request("DELETE", path)

    # ── Account ──────────────────────────────────────────────

    def get_account(self) -> dict:
        return self._get("/account")

    def get_billing_balance(self) -> dict:
        return self._get("/billing/balance")

    # ── Ordering ─────────────────────────────────────────────

    def get_catalog(self) -> list[dict]:
        return self._get("/ordering/catalog").get("items", [])

    def preview_order(self, **kwargs) -> dict:
        return self._post("/ordering/preview", kwargs)

    def submit_order(self, **kwargs) -> dict:
        return self._post("/ordering/submit", kwargs)

    # ── VM Lifecycle ─────────────────────────────────────────

    def list_vms(self) -> list[dict]:
        return self._get("/vm").get("items", [])

    def get_vm(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}")

    def get_vm_summary(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/summary")

    def start_vm(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/start")

    def stop_vm(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/stop")

    def restart_vm(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/restart")

    def cancel_vm(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/cancel")

    def reinstall_vm(self, service_id: int, **kwargs) -> dict:
        return self._patch(f"/vm/{service_id}/reinstall", kwargs)

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

    # ── SSH Keys ─────────────────────────────────────────────

    def list_ssh_keys(self, service_id: int) -> list[dict]:
        return self._get(f"/vm/{service_id}/ssh-keys").get("items", [])

    def add_ssh_key(self, service_id: int, public_key: str, label: str = "") -> dict:
        return self._post(
            f"/vm/{service_id}/ssh-keys",
            {"public_key": public_key, "label": label},
        )

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
