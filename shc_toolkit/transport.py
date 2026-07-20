"""Transport-agnostic interface for SHC API operations.

Defines the SHCTransport Protocol that both SHCClient (REST v2) and
SHCMCPClient (MCP Streamable HTTP) implement. The factory in __init__.py
selects the transport at runtime via SHC_TRANSPORT env var or explicit
parameter.

Transport selection:
    SHC_TRANSPORT=rest   → SHCClient    (default; ~165 hand-written methods)
    SHC_TRANSPORT=mcp    → SHCMCPClient (124 TOOL_MAP entries; live MCP
                                         server exposes 157 tools total)
    SHC_TRANSPORT=auto   → try MCP, fall back to REST

Both transports share identical method names and return shapes for all
core operations. The REST client has additional methods (snapshots, ISO,
rDNS, console, firewall detail, contacts, affiliate, KB, etc.) that the
MCP client exposes via the live server's full 157-tool catalog (request
with header `X-MCP-Tools: all`).

NOTE on `confirm` semantics across transports: methods that take
`*, confirm: bool = True` behave differently depending on transport:
  - REST (SHCClient): `confirm=False` is PROBE MODE — surfaces the 409
    `confirmation_required` to the caller without auto-completing the
    re-send. The caller reads `e.confirmation_id` and decides.
  - MCP (SHCMCPClient): `confirm` is IGNORED — the MCP transport always
    auto-completes the confirmation re-send inside `call_tool`. Probe
    mode is not currently implementable on MCP without a wrapper change.
Transport-agnostic callers should not rely on `confirm=False` surfacing
the 409 uniformly; if probe mode is required, use REST explicitly.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class SHCTransport(Protocol):
    """Interface contract for SHC API transports.

    Both SHCClient and SHCMCPClient must implement these methods.
    Method signatures match SHCClient (client.py) exactly.

    The Protocol declares the shared surface — every method here is
    implemented on BOTH transports. REST-only methods (e.g.
    `revoke_api_key` which is identity-class per SHC v2.4.13 and not
    exposed by the MCP server) are NOT on this Protocol.
    """

    # ── Account ──────────────────────────────────────────────

    def get_account(self) -> dict: ...
    def get_account_balance(self) -> dict: ...
    def get_account_activity(self, limit: int = 20, offset: int = 0) -> dict: ...
    def update_preferences(self, *, confirm: bool = True, **kwargs) -> dict: ...
    def set_credit_handling(self, *, confirm: bool = True, **kwargs) -> dict: ...

    # ── API Keys ─────────────────────────────────────────────

    def list_api_keys(self) -> list[dict]: ...

    # ── VM Lifecycle (core) ──────────────────────────────────

    def list_vms(self) -> list[dict]: ...
    def get_vm(self, service_id: int) -> dict: ...
    def get_vm_summary(self, service_id: int) -> dict: ...
    def get_vm_detail(self, service_id: int) -> dict: ...
    def start_vm(self, service_id: int) -> dict: ...
    def stop_vm(self, service_id: int) -> dict: ...
    def restart_vm(self, service_id: int) -> dict: ...
    def shutdown_vm(self, service_id: int) -> dict: ...
    def reset_vm(self, service_id: int) -> dict: ...

    def cancel_vm(
        self, service_id: int, *, immediate: bool = True, confirm: bool = True
    ) -> dict: ...
    def reinstall_vm(
        self, service_id: int, *, confirm: bool = True, **kwargs
    ) -> dict: ...

    # ── VM Data ──────────────────────────────────────────────

    def get_vm_metrics(self, service_id: int) -> dict: ...
    def get_vm_bandwidth(self, service_id: int) -> dict: ...
    def get_vm_credentials(self, service_id: int, *, confirm: bool = True) -> dict: ...

    # ── Backups ──────────────────────────────────────────────

    def list_backups(self, service_id: int) -> list[dict]: ...
    def create_backup(self, service_id: int, name: str | None = None) -> dict: ...

    def restore_backup(
        self, service_id: int, backup_id: str, *, confirm: bool = True
    ) -> dict: ...

    def delete_backup(
        self, service_id: int, backup_id: str, *, confirm: bool = True
    ) -> dict: ...

    def set_backup_protection(
        self,
        service_id: int,
        backup_id: str,
        protected: bool,
        *,
        confirm: bool = True,
    ) -> dict: ...

    # ── Snapshots ────────────────────────────────────────────

    def list_snapshots(self, service_id: int) -> list[dict]: ...
    def create_snapshot(self, service_id: int, name: str | None = None) -> dict: ...

    def restore_snapshot(
        self, service_id: int, snapshot_id: str, *, confirm: bool = True
    ) -> dict: ...

    def delete_snapshot(
        self, service_id: int, snapshot_id: str, *, confirm: bool = True
    ) -> dict: ...

    def set_snapshot_protection(
        self,
        service_id: int,
        snapshot_id: str,
        protected: bool,
        *,
        confirm: bool = True,
    ) -> dict: ...

    # ── Jobs ─────────────────────────────────────────────────

    def list_jobs(self, service_id: int) -> list[dict]: ...
    def get_job(self, service_id: int, job_id: str) -> dict: ...

    # ── Ordering ─────────────────────────────────────────────

    def get_catalog(self, **kwargs) -> list[dict]: ...
    def preview_order(self, **kwargs) -> dict: ...
    def submit_order(self, idempotency_key: str | None = None, **kwargs) -> dict: ...

    # ── Upgrades ─────────────────────────────────────────────

    def list_upgrade_options(self, service_id: int) -> list[dict]: ...
    def preview_upgrade(self, service_id: int, package_id: int) -> dict: ...
    def upgrade_vm(self, service_id: int, package_id: int) -> dict: ...

    # ── VM term + addons (v2.4.3) ────────────────────────────

    def list_vm_addons(self, service_id: int) -> list[dict]: ...
    def get_vm_addon_options(self, service_id: int) -> dict: ...
    def create_vm_addon(
        self, service_id: int, *, confirm: bool = True, **kwargs
    ) -> dict: ...
    def preview_vm_addon(self, service_id: int, **kwargs) -> dict: ...
    def get_vm_term_options(self, service_id: int) -> dict: ...
    def change_vm_term(
        self, service_id: int, *, confirm: bool = True, **kwargs
    ) -> dict: ...
    def preview_vm_term_change(self, service_id: int, **kwargs) -> dict: ...

    # ── Orders (v2.4.3) ──────────────────────────────────────

    def list_orders(self, **params) -> list[dict]: ...
    def get_order(self, order_id: int) -> dict: ...
    def cancel_pending_order(self, order_id: int, *, confirm: bool = True) -> dict: ...

    # ── VM power + lifecycle (v2.4.6) ────────────────────────

    def standby_vm(self, service_id: int, *, confirm: bool = True) -> dict: ...
    def preview_standby(self, service_id: int) -> dict: ...
    def resume_vm(self, service_id: int) -> dict: ...
    def list_events(self, **params) -> list[dict]: ...

    # ── Cloud-init (v2.4.7+) ────────────────────────────────

    def validate_vm_cloud_init(self, service_id: int, *, cloud_init: str) -> dict: ...
    def update_vm_cloud_init(
        self, service_id: int, *, cloud_init: str, confirm: bool = True
    ) -> dict: ...
    def delete_vm_cloud_init(
        self, service_id: int, *, confirm: bool = True
    ) -> dict: ...

    # ── SSH Keys ─────────────────────────────────────────────

    def list_ssh_keys(self, service_id: int | None = None) -> list[dict]: ...

    def add_ssh_key(
        self, service_id: int, public_key: str, label: str = ""
    ) -> dict: ...
    def apply_ssh_key_live(self, service_id: int, public_key: str) -> dict: ...
    def set_stored_ssh_key(
        self, service_id: int, public_key: str, *, confirm: bool = True
    ) -> dict: ...
    def delete_stored_ssh_key(
        self, service_id: int, *, confirm: bool = True
    ) -> dict: ...

    # ── Firewall ─────────────────────────────────────────────

    def get_firewall(self, service_id: int) -> dict: ...
    def set_firewall_policy(self, service_id: int, policy: str) -> dict: ...
    def create_firewall_rule(self, service_id: int, **kwargs) -> dict: ...
    def delete_firewall_rule(self, service_id: int, position: int) -> dict: ...

    # ── ISO ──────────────────────────────────────────────────

    def list_isos(self, service_id: int) -> list[dict]: ...
    def mount_iso(self, service_id: int, iso_id: str) -> dict: ...
    def unmount_iso(self, service_id: int, *, confirm: bool = True) -> dict: ...

    # ── Contacts (v2.4.24) ───────────────────────────────────

    def create_contact(self, *, confirm: bool = True, **kwargs) -> dict: ...

    # ── Affiliate (v2.4.24) ──────────────────────────────────

    def set_affiliate_payout_destination(
        self, *, confirm: bool = True, **kwargs
    ) -> dict: ...

    # ── Reverse DNS ──────────────────────────────────────────

    def list_rdns(self, service_id: int) -> list[dict]: ...
    def set_rdns(self, service_id: int, ip: str, ptr: str) -> dict: ...
    def clear_rdns(self, service_id: int, ip: str) -> dict: ...

    # ── Console ──────────────────────────────────────────────

    def get_console_availability(self, service_id: int) -> dict: ...
    def create_console_session(self, service_id: int) -> dict: ...

    # ── Templates ────────────────────────────────────────────

    def list_templates(self) -> list[dict]: ...

    # ── Billing ──────────────────────────────────────────────

    def list_invoices(self, **params) -> dict: ...
    def get_invoice(self, invoice_id: int) -> dict: ...
    def pay_invoice(self, invoice_id: int, idempotency_key: str) -> dict: ...
    def list_transactions(self, limit: int = 20, offset: int = 0) -> dict: ...

    # ── Support ──────────────────────────────────────────────

    def list_support_tickets(self, limit: int = 20, offset: int = 0) -> dict: ...

    def create_support_ticket(
        self,
        subject: str,
        message: str,
        department_id: int,
        priority: str = "medium",
        service_id: int | None = None,
        **kwargs,
    ) -> dict: ...

    def close_support_ticket(self, ticket_id: int, *, confirm: bool = True) -> dict: ...

    # ── Wait / Poll ──────────────────────────────────────────

    def wait_for_provisioning(
        self, service_id: int, timeout: int = 300, interval: int = 10
    ) -> dict: ...

    def wait_for_job(
        self, service_id: int, job_id: str, timeout: int = 600, interval: int = 10
    ) -> dict: ...

    # ── Health ───────────────────────────────────────────────

    def check_vm_health(self, service_id: int) -> dict: ...


# ── Transport Selection ────────────────────────────────────────

MCP_ENDPOINT = "https://mcp.sovereignhybridcompute.com/"
REST_BASE_URL = "https://blesta.sovereignhybridcompute.com/user-api/v2"


def resolve_transport(explicit: str | None = None) -> str:
    """Determine which transport to use.

    Priority:
    1. Explicit parameter
    2. SHC_TRANSPORT env var
    3. Default: 'rest' (MCP requires optional dependency)

    Returns 'rest' or 'mcp'.
    """
    import os

    choice = explicit or os.environ.get("SHC_TRANSPORT", "rest")
    choice = choice.lower().strip()

    if choice == "auto":
        return "rest"

    if choice not in ("rest", "mcp"):
        raise ValueError(f"Invalid transport '{choice}'. Use 'rest', 'mcp', or 'auto'.")

    return choice
