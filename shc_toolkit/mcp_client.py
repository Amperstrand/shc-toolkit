"""SHC MCP client — implements SHCTransport via MCP Streamable HTTP.

Connects to the flagship SHC MCP server (https://mcp.sovereignhybridcompute.com/)
and exposes the same method surface as SHCClient (REST). Both clients are
interchangeable behind the SHCTransport Protocol.

Auth: Bearer shc_live_... operate key (same key as REST).
Transport: Streamable HTTP (JSON-RPC 2.0 over HTTP POST).
Confirmation: Destructive/spend ops return a confirmation_id; the client
auto-resubmits with X-User-Api-Confirm, same as the REST client.

Usage:
    from shc_toolkit import create_client

    c = create_client(transport="mcp")
    vms = c.list_vms()
    c.start_vm(123)

The MCP server exposes 116 tools (23 core). This client maps all core tools
to method names matching SHCClient. Non-core tools are callable via
``call_tool(name, arguments)``.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import requests

from .client import SHCError

log = logging.getLogger(__name__)

MCP_ENDPOINT = "https://mcp.sovereignhybridcompute.com/mcp"
MCP_PROTOCOL_VERSION = "2025-06-18"

# ── MCP tool name → method mapping ─────────────────────────────
# Maps SHCClient method names to MCP tool names (camelCase).
# Core 23 tools are guaranteed on the MCP server.
TOOL_MAP: dict[str, str] = {
    # Account
    "get_account": "getAccount",
    "get_billing_balance": "getBillingBalance",
    # API Keys
    # API Keys
    "list_api_keys": "listApiKeys",
    # VM lifecycle
    "list_vms": "listVirtualMachines",
    "get_vm": "getVirtualMachine",
    "get_vm_summary": "getVirtualMachineSummary",
    "get_vm_detail": "getVirtualMachineDetail",
    "start_vm": "startVirtualMachine",
    "stop_vm": "stopVirtualMachine",
    "restart_vm": "restartVirtualMachine",
    "reinstall_vm": "reinstallVirtualMachine",
    "cancel_vm": "cancelVirtualMachine",
    # Jobs
    "list_jobs": "listVirtualMachineJobs",
    "get_job": "getVirtualMachineJob",
    # Backups
    "list_backups": "listVirtualMachineBackups",
    "create_backup": "createVirtualMachineBackup",
    # Ordering
    "get_catalog": "getOrderingCatalog",
    "submit_order": "createVirtualMachineOrder",
    # Upgrades
    "list_upgrade_options": "getServiceUpgradeOptions",
    "preview_upgrade": "previewServiceUpgrade",
    "upgrade_vm": "upgradeService",
    # VM term + addons (v2.4.3)
    "list_vm_addons": "listServiceAddons",
    "get_vm_addon_options": "getServiceAddonOptions",
    "create_vm_addon": "createServiceAddon",
    "preview_vm_addon": "previewServiceAddon",
    "get_vm_term_options": "getVirtualMachineTermOptions",
    "change_vm_term": "changeVirtualMachineTerm",
    "preview_vm_term_change": "previewVirtualMachineTermChange",
    # Orders (v2.4.3)
    "list_orders": "listOrders",
    "get_order": "getOrder",
    "cancel_pending_order": "cancelPendingOrder",
    # Quotations (v2.4.3)
    "list_quotations": "listQuotations",
    "get_quotation": "getQuotation",
    "approve_quotation": "approveQuotation",
    "list_quotation_invoices": "listQuotationInvoices",
    # Nostr account linking (v2.4.3)
    "link_nostr_identity": "linkNostrIdentity",
    "unlink_nostr_identity": "unlinkNostrIdentity",
    "update_nip05": "updateNip05",
    # Documents + Downloads (v2.4.3)
    "list_documents": "listClientDocuments",
    "download_document": "downloadClientDocument",
    "list_downloads": "listDownloadFiles",
    "download_file": "downloadDownloadFile",
    # Support extras (v2.4.3)
    "get_support_ticket_attachment": "getSupportTicketAttachment",
    "submit_support_ticket_feedback": "submitSupportTicketFeedback",
    # Invoice electronic (v2.4.3)
    "get_invoice_electronic": "getInvoiceElectronic",
    # Billing
    "list_invoices": "listInvoices",
    "get_invoice": "getInvoice",
    "get_payment": "getPayment",
    "list_payment_methods": "listPaymentMethods",
    "get_transaction": "getTransaction",
    "add_credit": "submitCreditTopup",
    # Account
    "get_account_balance": "getAccountBalance",
    "get_preferences": "getAccountPreferences",
    "update_preferences": "updateAccountPreferences",
    "get_autodebit": "getAutoDebit",
    "get_credit_handling": "getCreditHandling",
    "set_credit_handling": "updateCreditHandling",
    # Contacts
    "list_contacts": "listContacts",
    "get_contact": "getContact",
    "create_contact": "createContact",
    "update_contact": "updateContact",
    "delete_contact": "deleteContact",
    "list_contact_permissions": "getContactPermissionOptions",
    # SSH Keys
    "set_stored_ssh_key": "setServiceSshKey",
    "delete_stored_ssh_key": "deleteServiceSshKey",
    "remove_ssh_key_live": "deleteLiveServiceSshKey",
    # Support
    "list_support_tickets": "listSupportTickets",
    "get_support_ticket": "getSupportTicket",
    "create_support_ticket": "createSupportTicket",
    "reply_support_ticket": "replySupportTicket",
    "close_support_ticket": "closeSupportTicket",
    # Affiliate
    "get_affiliate_overview": "getAffiliateAccount",
    "list_affiliate_payouts": "listAffiliatePayouts",
    "list_affiliate_referrals": "listAffiliateReferrals",
    "get_affiliate_payout_destination": "getAffiliatePayoutDestination",
    "set_affiliate_payout_destination": "updateAffiliatePayoutDestination",
    "request_affiliate_payout": "requestAffiliatePayout",
    "enroll_affiliate": "enrollAffiliate",
    # Managers
    "list_managers": "listAccountManagers",
    "invite_manager": "inviteAccountManager",
    "list_manager_permissions": "getManagerPermissionOptions",
    # KB
    "search_kb": "searchKb",
    "get_kb_article": "getKbArticle",
    # Snapshots (extended)
    "list_snapshots": "listVirtualMachineSnapshots",
    "create_snapshot": "createVirtualMachineSnapshot",
    "delete_snapshot": "deleteVirtualMachineSnapshot",
    "restore_snapshot": "restoreVirtualMachineSnapshot",
    "verify_snapshot": "verifyVirtualMachineSnapshot",
    "set_snapshot_protection": "setVirtualMachineSnapshotProtection",
    # Backups (extended)
    "delete_backup": "deleteVirtualMachineBackup",
    "restore_backup": "restoreVirtualMachineBackup",
    "verify_backup": "verifyVirtualMachineBackup",
    "set_backup_protection": "setVirtualMachineBackupProtection",
    # Firewall (extended)
    "edit_firewall_rule": "updateVirtualMachineFirewallRule",
    # Emails
    "list_emails": "listEmails",
    "get_email": "getEmail",
    # Managed accounts
    "list_managed_accounts": "listManagedAccounts",
    # Extended VM operations
    "get_vm_renewal_quote": "getRenewalQuote",
    "list_isos": "getVirtualMachineIso",
    "get_account_activity": "listAccountActivity",
    "rekey_zk_backup": "rekeyVirtualMachineZkBackup",
    "submit_vm_renewal": "submitVirtualMachineRenewal",
    "standby_vm": "standbyVirtualMachine",
    "preview_standby": "previewVirtualMachineStandby",
    "resume_vm": "resumeVirtualMachine",
    # Remaining niche tools
    "delete_manager": "deleteManager",
    "list_kb_categories": "listKbCategories",
    "list_images": "listImages",
    "relinquish_managed_account": "relinquishManagedAccount",
    "respond_to_managed_account_invitation": "respondToManagedAccountInvitation",
    "update_account_manager": "updateAccountManager",
    "get_invoice_pdf": "getInvoicePdf",
    "list_events": "listEvents",
}

# Reverse map for debugging
METHOD_MAP: dict[str, str] = {v: k for k, v in TOOL_MAP.items()}


class SHCMCPClient:
    """SHC client backed by the MCP Streamable HTTP transport.

    Implements the same method surface as SHCClient (REST), delegating
    to MCP tools on the flagship server. Destructive/spend operations
    are auto-confirmed via the MCP confirmation flow.

    Args:
        api_key: SHC API key (shc_live_...). Falls back to SHC_API_KEY env.
        endpoint: MCP server URL. Defaults to flagship server.
    """

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str = MCP_ENDPOINT,
    ):
        self.api_key = api_key or os.environ.get("SHC_API_KEY", "")
        if not self.api_key:
            raise ValueError("SHC_API_KEY not set and no api_key provided")
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": MCP_PROTOCOL_VERSION,
        })
        self._request_id = 0
        self._initialized = False
        self._cache_ttl = 300
        self._cache: dict[str, tuple[float, Any]] = {}

    def _cache_get(self, key):
        if self._cache_ttl <= 0:
            return None
        entry = self._cache.get(key)
        if entry is None:
            return None
        import time
        ts, data = entry
        if time.time() - ts > self._cache_ttl:
            del self._cache[key]
            return None
        return data

    def _cache_set(self, key, data):
        if self._cache_ttl > 0:
            import time
            self._cache[key] = (time.time(), data)
        return data

    def invalidate_cache(self, prefix=None):
        if prefix is None:
            self._cache.clear()
        else:
            self._cache = {k: v for k, v in self._cache.items() if not k.startswith(prefix)}

    # ── MCP Protocol ─────────────────────────────────────────

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _ensure_initialized(self):
        """Send MCP initialize handshake once."""
        if self._initialized:
            return
        resp = self._send_jsonrpc("initialize", {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {
                "name": "shc-toolkit",
                "version": "0.4.0",
            },
        })
        log.debug("MCP initialized: %s", resp.get("result", {}).get("serverInfo"))
        try:
            self._send_jsonrpc("notifications/initialized", _notification=True)
        except (json.JSONDecodeError, SHCError):
            pass
        self._initialized = True

    def _send_jsonrpc(
        self,
        method: str,
        params: dict | None = None,
        *,
        _notification: bool = False,
    ) -> dict:
        """Send a JSON-RPC 2.0 request to the MCP server."""
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": method,
        }
        if not _notification:
            payload["id"] = self._next_id()
        if params:
            payload["params"] = params

        resp = self.session.post(self.endpoint, json=payload, timeout=60)
        if resp.status_code == 401:
            raise SHCError(
                "unauthorized",
                "MCP server rejected API key. Ensure you have a valid "
                "shc_live_ operate key.",
            )
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "5"))
            raise SHCError(
                "rate_limited",
                f"MCP rate limited. Retry after {retry_after}s.",
            )
        if resp.status_code >= 500:
            raise SHCError(
                "internal_error",
                f"MCP server error {resp.status_code}: {resp.text[:200]}",
            )

        # Parse response: could be JSON or SSE
        body = self._parse_mcp_response(resp)
        if _notification:
            return {}

        if "error" in body:
            err = body["error"]
            JSONRPC_ERROR_CODES = {
                -32700: "parse_error",
                -32600: "invalid_request",
                -32601: "method_not_found",
                -32602: "invalid_params",
                -32603: "internal_error",
            }
            numeric_code = err.get("code", -1)
            err_code = JSONRPC_ERROR_CODES.get(numeric_code, f"mcp_error_{numeric_code}")
            exc = SHCError(err_code, err.get("message", str(err)), None, err.get("data"))
            # Capture confirmation_id from error data
            if isinstance(exc.details, dict):
                conf = exc.details.get("confirmation", {})
                if isinstance(conf, dict):
                    exc.confirmation_id = conf.get("confirmation_id")
            raise exc

        return body

    @staticmethod
    def _parse_mcp_response(resp: requests.Response) -> dict:
        """Parse MCP response — handles SSE, JSON, and non-JSON notification acks."""
        content_type = resp.headers.get("Content-Type", "")

        if "text/event-stream" in content_type:
            for line in resp.text.splitlines():
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if data:
                        return json.loads(data)
            raise SHCError("internal_error", "SSE response had no data lines")

        if "application/json" not in content_type:
            return {}

        text = resp.text.strip()
        if not text:
            return {}

        json_start = text.find("{")
        if json_start < 0:
            return {}
        return json.loads(text[json_start:])

    def call_tool(self, name: str, arguments: dict | None = None) -> Any:
        """Call an MCP tool by name. Auto-handles confirmation flow.

        Args:
            name: MCP tool name (e.g. 'listVirtualMachines').
            arguments: Tool arguments dict.

        Returns:
            The tool result data (unwrapped from MCP content array).
        """
        self._ensure_initialized()
        args = arguments or {}

        for attempt in range(2):
            resp = self._send_jsonrpc("tools/call", {
                "name": name,
                "arguments": args,
            })

            result = resp.get("result", {})
            sc = result.get("structuredContent", {})

            if sc.get("status") == "confirmation_required":
                how_to = sc.get("how_to_proceed", {})
                retry_args = how_to.get("arguments")
                if retry_args and attempt == 0:
                    args = retry_args
                    continue

            try:
                return self._unwrap_tool_result(resp)
            except SHCError as e:
                cid = getattr(e, "confirmation_id", None)
                if not cid and isinstance(e.details, dict):
                    cid = e.details.get("confirmation_id")
                    conf = e.details.get("confirmation", {})
                    if not cid and isinstance(conf, dict):
                        cid = conf.get("confirmation_id")
                if not cid or attempt > 0:
                    raise
                args = {**args, "_confirmation_id": cid}

    @staticmethod
    def _unwrap_tool_result(resp: dict) -> Any:
        """Extract data from MCP tool result, handling isError responses."""
        result = resp.get("result", {})

        if result.get("isError"):
            sc = result.get("structuredContent", {})
            err = sc.get("error", {})
            raise SHCError(
                err.get("code", "mcp_tool_error"),
                err.get("message", "MCP tool returned an error"),
                sc.get("request_id"),
                sc,
                err.get("error_code"),
                err.get("retry_after_seconds"),
            )

        sc = result.get("structuredContent")
        if isinstance(sc, dict):
            if "result" in sc:
                return sc["result"]
            if "data" in sc:
                data = sc["data"]
                if isinstance(data, dict) and "data" in data:
                    data = data["data"]
                return data

        content = result.get("content", [])
        if not content:
            return result

        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))

        combined = "\n".join(texts).strip()
        if not combined:
            return result

        try:
            return json.loads(combined)
        except (json.JSONDecodeError, ValueError):
            return combined

    @staticmethod
    def _extract_items(result: Any) -> list[dict]:
        if isinstance(result, dict):
            return result.get("items", [])
        return result if isinstance(result, list) else []

    # ── Convenience: call tool by Python method name ─────────

    def _call(self, method_name: str, **kwargs) -> Any:
        """Call the MCP tool mapped to a Python method name.

        Converts kwargs from snake_case to the MCP tool's expected
        arguments (typically camelCase with serviceId instead of
        service_id, etc.).
        """
        tool_name = TOOL_MAP.get(method_name, method_name)
        args = self._convert_args(kwargs)
        return self.call_tool(tool_name, args if args else None)

    @staticmethod
    def _convert_args(kwargs: dict) -> dict:
        """Convert Python kwargs to MCP tool arguments.

        Handles common snake_case → camelCase conversions and
        service_id → serviceId, etc.
        """
        if not kwargs:
            return {}

        result = {}
        for key, val in kwargs.items():
            # Convert snake_case keys to camelCase for MCP
            if "_" in key:
                parts = key.split("_")
                camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
                result[camel] = val
            else:
                result[key] = val
        return result

    # ── Core methods (match SHCClient interface) ─────────────

    # Account
    def get_account(self) -> dict:
        return self._call("get_account")

    def get_account_balance(self) -> dict:
        cached = self._cache_get("balance")
        if cached is not None:
            return cached
        result = self._call("get_account_balance")
        return self._cache_set("balance", result)

    def get_available_credit(self):
        cached = self._cache_get("credit")
        if cached is not None:
            return cached
        result = self.get_account_balance()
        if isinstance(result, dict):
            for b in result.get("balances", result.get("credit", [])):
                if b.get("currency") == "USD":
                    try:
                        amt = float(b.get("available_credit", b.get("amount", 0)))
                        return self._cache_set("credit", amt)
                    except (ValueError, TypeError):
                        pass
        return 0.0

    def check_credit(self, required):
        available = self.get_available_credit()
        if available < required:
            from .client import InsufficientCreditError
            raise InsufficientCreditError(required, available)

    def get_account_activity(self, limit: int = 20, offset: int = 0) -> dict:
        return self._call("get_account_balance", limit=limit, offset=offset)

    def list_api_keys(self) -> list[dict]:
        result = self._call("list_api_keys")
        return self._extract_items(result)

    # VM Lifecycle
    def list_vms(self) -> list[dict]:
        result = self._call("list_vms")
        return self._extract_items(result)

    def get_vm(self, service_id: int) -> dict:
        return self._call("get_vm", service_id=service_id)

    def get_vm_summary(self, service_id: int) -> dict:
        return self._call("get_vm_summary", service_id=service_id)

    def get_vm_detail(self, service_id: int) -> dict:
        return self._call("get_vm_detail", service_id=service_id)

    def start_vm(self, service_id: int) -> dict:
        return self._call("start_vm", service_id=service_id)

    def stop_vm(self, service_id: int) -> dict:
        return self._call("stop_vm", service_id=service_id)

    def restart_vm(self, service_id: int) -> dict:
        return self._call("restart_vm", service_id=service_id)

    def shutdown_vm(self, service_id: int) -> dict:
        # Not in core 23 — try the full tool catalog
        return self.call_tool("shutdownVirtualMachine", {"serviceId": service_id})

    def reset_vm(self, service_id: int) -> dict:
        return self.call_tool("resetVirtualMachine", {"serviceId": service_id})

    def cancel_vm(
        self, service_id: int, *, immediate: bool = True, confirm: bool = True
    ) -> dict:
        body: dict[str, Any] = {"immediate": True} if immediate else {}
        result = self.call_tool("cancelVirtualMachine", {
            "serviceId": service_id, "body": body,
        })
        self.invalidate_cache("credit")
        return result

    def reinstall_vm(self, service_id: int, *, confirm: bool = True, **kwargs) -> dict:
        return self.call_tool("reinstallVirtualMachine", {
            "serviceId": service_id, "body": self._convert_args(kwargs),
        })

    # Jobs
    def list_jobs(self, service_id: int) -> list[dict]:
        result = self._call("list_jobs", service_id=service_id)
        return self._extract_items(result)

    def get_job(self, service_id: int, job_id: str) -> dict:
        return self._call("get_job", service_id=service_id, job_id=job_id)

    # Backups
    def list_backups(self, service_id: int) -> list[dict]:
        result = self._call("list_backups", service_id=service_id)
        return self._extract_items(result)

    def create_backup(self, service_id: int, name: str | None = None) -> dict:
        body: dict[str, Any] = {}
        if name:
            body["name"] = name
        return self.call_tool("createVirtualMachineBackup", {
            "serviceId": service_id, "body": body,
        })

    def restore_backup(
        self, service_id: int, backup_id: str, *, confirm: bool = True
    ) -> dict:
        return self.call_tool("restoreVirtualMachineBackup", {
            "serviceId": service_id, "backupId": backup_id,
        })

    def delete_backup(
        self, service_id: int, backup_id: str, *, confirm: bool = True
    ) -> dict:
        return self.call_tool("deleteVirtualMachineBackup", {
            "serviceId": service_id, "body": {"backup_id": backup_id},
        })

    def verify_backup(self, service_id: int, backup_id: str) -> dict:
        return self.call_tool("verifyVirtualMachineBackup", {
            "serviceId": service_id, "body": {"backup_id": backup_id},
        })

    def set_backup_protection(self, service_id: int, backup_id: str, protected: bool) -> dict:
        return self.call_tool("setVirtualMachineBackupProtection", {
            "serviceId": service_id, "body": {"backup_id": backup_id, "protected": protected},
        })

    def get_backup_restore_hints(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineBackupRestoreHints", {"serviceId": service_id})

    # Snapshots
    def list_snapshots(self, service_id: int) -> list[dict]:
        result = self.call_tool("listVirtualMachineSnapshots", {"serviceId": service_id})
        return self._extract_items(result)

    def create_snapshot(self, service_id: int, name: str | None = None) -> dict:
        body: dict[str, Any] = {}
        if name:
            body["name"] = name
        return self.call_tool("createVirtualMachineSnapshot", {
            "serviceId": service_id, "body": body,
        })

    def restore_snapshot(
        self, service_id: int, snapshot_id: str, *, confirm: bool = True
    ) -> dict:
        return self.call_tool("restoreVirtualMachineSnapshot", {
            "serviceId": service_id, "body": {"snapshot_id": snapshot_id},
        })

    def delete_snapshot(
        self, service_id: int, snapshot_id: str, *, confirm: bool = True
    ) -> dict:
        return self.call_tool("deleteVirtualMachineSnapshot", {
            "serviceId": service_id, "body": {"snapshot_id": snapshot_id},
        })

    def verify_snapshot(self, service_id: int, snapshot_id: str) -> dict:
        return self.call_tool("verifyVirtualMachineSnapshot", {
            "serviceId": service_id, "body": {"snapshot_id": snapshot_id},
        })

    def set_snapshot_protection(self, service_id: int, snapshot_id: str, protected: bool) -> dict:
        return self.call_tool("setVirtualMachineSnapshotProtection", {
            "serviceId": service_id, "body": {"snapshot_id": snapshot_id, "protected": protected},
        })

    def get_snapshot_restore_hints(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineSnapshotRestoreHints", {"serviceId": service_id})

    # File Restore
    def list_file_restore_sources(self, service_id: int) -> list[dict]:
        result = self.call_tool("listVmFileRestoreSources", {"serviceId": service_id})
        return self._extract_items(result)

    def browse_file_restore(self, service_id: int, source: str, path: str = "/") -> list[dict]:
        result = self.call_tool("listVmFileRestoreEntries", {
            "serviceId": service_id, "body": {"source": source, "path": path},
        })
        return self._extract_items(result)

    # Data Preferences
    def get_data_preferences(self, service_id: int) -> dict:
        return self.call_tool("getVmDataPreferences", {"serviceId": service_id})

    def set_data_preferences(self, service_id: int, **kwargs) -> dict:
        return self.call_tool("updateVmDataPreferences", {
            "serviceId": service_id, "body": kwargs,
        })

    # Ordering
    def get_catalog(self, **kwargs) -> list[dict]:
        cached = self._cache_get("catalog:full")
        if cached is not None:
            return cached if isinstance(cached, list) else cached.get("items", [])
        result = self._call("get_catalog")
        if isinstance(result, dict):
            data = result.get("items", [])
        else:
            data = result if isinstance(result, list) else []
        return self._cache_set("catalog:full", data)

    def preview_order(self, **kwargs) -> dict:
        return self.call_tool("previewVirtualMachineOrder", {"body": kwargs})

    def submit_order(self, idempotency_key: str | None = None, **kwargs) -> dict:
        args: dict[str, Any] = {"body": kwargs}
        if idempotency_key:
            args["Idempotency-Key"] = idempotency_key
        return self.call_tool("createVirtualMachineOrder", args)

    # Upgrades
    def list_upgrade_options(self, service_id: int) -> list[dict]:
        result = self._call("list_upgrade_options", service_id=service_id)
        return self._extract_items(result)

    def preview_upgrade(self, service_id: int, package_id: int) -> dict:
        return self._call("preview_upgrade", service_id=service_id, package_id=package_id)

    def upgrade_vm(self, service_id: int, package_id: int) -> dict:
        return self._call("upgrade_vm", service_id=service_id, package_id=package_id)

    # VM term + addons (v2.4.3)
    def list_vm_addons(self, service_id: int) -> list[dict]:
        return self._extract_items(self._call("list_vm_addons", service_id=service_id))

    def get_vm_addon_options(self, service_id: int) -> dict:
        return self._call("get_vm_addon_options", service_id=service_id)

    def create_vm_addon(self, service_id: int, **body) -> dict:
        return self.call_tool("createServiceAddon", {"serviceId": service_id, "body": body})

    def preview_vm_addon(self, service_id: int, **body) -> dict:
        return self.call_tool("previewServiceAddon", {"serviceId": service_id, "body": body})

    def get_vm_term_options(self, service_id: int) -> dict:
        return self._call("get_vm_term_options", service_id=service_id)

    def change_vm_term(self, service_id: int, **body) -> dict:
        return self.call_tool("changeVirtualMachineTerm", {"serviceId": service_id, "body": body})

    def preview_vm_term_change(self, service_id: int, **body) -> dict:
        return self.call_tool("previewVirtualMachineTermChange", {"serviceId": service_id, "body": body})

    # Orders (v2.4.3)
    def list_orders(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_orders", **params))

    def get_order(self, order_id: int) -> dict:
        return self._call("get_order", order_id=order_id)

    def cancel_pending_order(self, order_id: int) -> dict:
        return self.call_tool("cancelPendingOrder", {"orderId": order_id})

    # Quotations (v2.4.3)
    def list_quotations(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_quotations", **params))

    def get_quotation(self, quotation_id: int) -> dict:
        return self._call("get_quotation", quotation_id=quotation_id)

    def approve_quotation(self, quotation_id: int) -> dict:
        return self.call_tool("approveQuotation", {"quotationId": quotation_id})

    def list_quotation_invoices(self, quotation_id: int) -> list[dict]:
        return self._extract_items(self._call("list_quotation_invoices", quotation_id=quotation_id))

    # Nostr account linking (v2.4.3)
    def link_nostr_identity(self, **body) -> dict:
        return self.call_tool("linkNostrIdentity", {"body": body})

    def unlink_nostr_identity(self, **body) -> dict:
        return self.call_tool("unlinkNostrIdentity", {"body": body})

    def update_nip05(self, **body) -> dict:
        return self.call_tool("updateNip05", {"body": body})

    # Documents + Downloads (v2.4.3)
    def list_documents(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_documents", **params))

    def download_document(self, document_id: int) -> dict:
        return self._call("download_document", document_id=document_id)

    def list_downloads(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_downloads", **params))

    def download_file(self, file_id: int) -> dict:
        return self._call("download_file", file_id=file_id)

    # Support extras (v2.4.3)
    def get_support_ticket_attachment(self, ticket_id: int, attachment_id: int) -> dict:
        return self.call_tool("getSupportTicketAttachment", {"ticketId": ticket_id, "attachmentId": attachment_id})

    def submit_support_ticket_feedback(self, ticket_id: int, rating: int, comment: str | None = None) -> dict:
        body: dict[str, Any] = {"rating": rating}
        if comment:
            body["comment"] = comment
        return self.call_tool("submitSupportTicketFeedback", {"ticketId": ticket_id, "body": body})

    # Invoice electronic (v2.4.3)
    def get_invoice_electronic(self, invoice_id: int) -> dict:
        return self._call("get_invoice_electronic", invoice_id=invoice_id)

    # Billing
    def list_invoices(self, **params) -> dict:
        return self._call("list_invoices", **params) or {}

    def get_invoice(self, invoice_id: int) -> dict:
        return self._call("get_invoice", invoice_id=invoice_id)

    def pay_invoice(self, invoice_id: int, idempotency_key: str) -> dict:
        return self.call_tool("submitPaymentCheckout", {
            "invoiceId": invoice_id, "idempotencyKey": idempotency_key,
        })

    def list_transactions(self, limit: int = 20, offset: int = 0) -> dict:
        return self.call_tool("listTransactions", {"limit": limit, "offset": offset})

    def get_payment(self, invoice_id: int) -> dict:
        return self._call("get_payment", invoice_id=invoice_id)

    def list_payment_methods(self) -> list[dict]:
        return self._extract_items(self._call("list_payment_methods"))

    def get_transaction(self, transaction_id: int) -> dict:
        return self._call("get_transaction", transaction_id=transaction_id)

    def add_credit(self, amount: str, idempotency_key: str, **kwargs) -> dict:
        body: dict[str, Any] = {"amount": amount, "idempotency_key": idempotency_key, **kwargs}
        return self.call_tool("submitCreditTopup", {"body": body})

    # Account
    def get_billing_balance(self) -> dict:
        return self._call("get_billing_balance")

    def get_preferences(self) -> dict:
        return self._call("get_preferences")

    def update_preferences(self, **body) -> dict:
        return self.call_tool("updateAccountPreferences", {"body": body})

    def get_autodebit(self) -> dict:
        return self._call("get_autodebit")

    def get_credit_handling(self) -> dict:
        return self._call("get_credit_handling")

    def set_credit_handling(self, **body) -> dict:
        return self.call_tool("updateCreditHandling", {"body": body})

    # Contacts
    def list_contacts(self) -> list[dict]:
        return self._extract_items(self._call("list_contacts"))

    def get_contact(self, contact_id: int) -> dict:
        return self._call("get_contact", contact_id=contact_id)

    def create_contact(self, **body) -> dict:
        return self.call_tool("createContact", {"body": body})

    def update_contact(self, contact_id: int, **body) -> dict:
        return self.call_tool("updateContact", {"contactId": contact_id, "body": body})

    def delete_contact(self, contact_id: int) -> dict:
        return self.call_tool("deleteContact", {"contactId": contact_id})

    def list_contact_permissions(self) -> dict:
        return self._call("list_contact_permissions")

    # SSH Keys (extended)
    def set_stored_ssh_key(self, service_id: int, ssh_key: str) -> dict:
        return self.call_tool("setServiceSshKey", {"body": {"service_id": service_id, "ssh_key": ssh_key}})

    def delete_stored_ssh_key(self, service_id: int) -> dict:
        return self.call_tool("deleteServiceSshKey", {"serviceId": service_id})

    def remove_ssh_key_live(self, service_id: int) -> dict:
        return self.call_tool("deleteLiveServiceSshKey", {"serviceId": service_id})

    # Support (extended)
    def list_support_tickets(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_support_tickets", **params))

    def get_support_ticket(self, ticket_id: int) -> dict:
        return self._call("get_support_ticket", ticket_id=ticket_id)

    def create_support_ticket(self, **body) -> dict:
        return self.call_tool("createSupportTicket", {"body": body})

    def reply_support_ticket(self, ticket_id: int, **body) -> dict:
        return self.call_tool("replySupportTicket", {"ticketId": ticket_id, "body": body})

    def close_support_ticket(self, ticket_id: int) -> dict:
        return self.call_tool("closeSupportTicket", {"ticketId": ticket_id})

    # Affiliate
    def get_affiliate_overview(self) -> dict:
        return self._call("get_affiliate_overview")

    def list_affiliate_payouts(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_affiliate_payouts", **params))

    def list_affiliate_referrals(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_affiliate_referrals", **params))

    def get_affiliate_payout_destination(self) -> dict:
        return self._call("get_affiliate_payout_destination")

    def set_affiliate_payout_destination(self, **body) -> dict:
        return self.call_tool("updateAffiliatePayoutDestination", {"body": body})

    def request_affiliate_payout(self, **body) -> dict:
        return self.call_tool("requestAffiliatePayout", {"body": body})

    def enroll_affiliate(self) -> dict:
        return self._call("enroll_affiliate")

    # Managers
    def list_managers(self) -> list[dict]:
        return self._extract_items(self._call("list_managers"))

    def invite_manager(self, **body) -> dict:
        return self.call_tool("inviteAccountManager", {"body": body})

    def list_manager_permissions(self) -> dict:
        return self._call("list_manager_permissions")

    # KB
    def search_kb(self, q: str, **params) -> list[dict]:
        return self._extract_items(self._call("search_kb", q=q, **params))

    def get_kb_article(self, article_id: int) -> dict:
        return self._call("get_kb_article", article_id=article_id)

    # Emails
    def list_emails(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_emails", **params))

    def get_email(self, email_id: int) -> dict:
        return self._call("get_email", email_id=email_id)

    # Managed accounts
    def list_managed_accounts(self) -> list[dict]:
        return self._extract_items(self._call("list_managed_accounts"))

    # Extended VM operations
    def get_vm_renewal_quote(self, service_id: int) -> dict:
        return self._call("get_vm_renewal_quote", service_id=service_id)

    def list_isos(self, service_id: int) -> list[dict]:
        return self._extract_items(self._call("list_isos", service_id=service_id))

    def rekey_zk_backup(self, service_id: int, **body) -> dict:
        return self.call_tool("rekeyVirtualMachineZkBackup", {"serviceId": service_id, "body": body})

    def submit_vm_renewal(self, service_id: int, **body) -> dict:
        return self.call_tool("submitVirtualMachineRenewal", {"serviceId": service_id, "body": body})

    def standby_vm(self, service_id: int) -> dict:
        return self.call_tool("standbyVirtualMachine", {"serviceId": service_id})

    def preview_standby(self, service_id: int) -> dict:
        return self.call_tool("previewVirtualMachineStandby", {"serviceId": service_id})

    def resume_vm(self, service_id: int) -> dict:
        return self.call_tool("resumeVirtualMachine", {"serviceId": service_id})

    def list_events(self, **params) -> list[dict]:
        return self._extract_items(self._call("list_events", **params))

    # Remaining niche tools
    def delete_manager(self, **body) -> dict:
        return self.call_tool("deleteManager", {"body": body})

    def list_kb_categories(self) -> list[dict]:
        return self._extract_items(self._call("list_kb_categories"))

    def list_images(self) -> list[dict]:
        return self._extract_items(self._call("list_images"))

    def relinquish_managed_account(self, **body) -> dict:
        return self.call_tool("relinquishManagedAccount", {"body": body})

    def respond_to_managed_account_invitation(self, **body) -> dict:
        return self.call_tool("respondToManagedAccountInvitation", {"body": body})

    def update_account_manager(self, **body) -> dict:
        return self.call_tool("updateAccountManager", {"body": body})

    def get_invoice_pdf(self, invoice_id: int) -> dict:
        return self._call("get_invoice_pdf", invoice_id=invoice_id)

    # VM Data
    def get_vm_metrics(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineMetrics", {"serviceId": service_id})

    def get_vm_bandwidth(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineBandwidth", {"serviceId": service_id})

    def get_vm_credentials(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineCredentials", {"serviceId": service_id})

    def get_vm_network(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineNetwork", {"serviceId": service_id})

    def get_vm_activity(self, service_id: int) -> list[dict]:
        result = self.call_tool("listVirtualMachineActivity", {"serviceId": service_id})
        return self._extract_items(result)

    def get_vm_payments(self, service_id: int) -> list[dict]:
        result = self.call_tool("listVirtualMachinePayments", {"serviceId": service_id})
        return self._extract_items(result)

    # SSH Keys
    def list_ssh_keys(self, service_id: int | None = None) -> list[dict]:
        result = self.call_tool("listServiceSshKeys", {})
        return self._extract_items(result)

    def add_ssh_key(
        self, service_id: int, public_key: str, label: str = ""
    ) -> dict:
        return self.call_tool("setServiceSshKey", {
            "body": {
                "service_id": service_id,
                "public_key": public_key,
                "label": label,
            },
        })

    def apply_ssh_key_live(self, service_id: int, public_key: str) -> dict:
        return self.call_tool("applyLiveServiceSshKey", {
            "serviceId": service_id, "publicKey": public_key,
        })

    # Firewall
    def get_firewall(self, service_id: int) -> dict:
        return self.call_tool("getVirtualMachineFirewall", {"serviceId": service_id})

    def set_firewall_policy(self, service_id: int, policy: str) -> dict:
        return self.call_tool("updateVirtualMachineFirewallPolicy", {
            "serviceId": service_id, "body": {"policy": policy},
        })

    def create_firewall_rule(self, service_id: int, **kwargs) -> dict:
        return self.call_tool("addVirtualMachineFirewallRule", {
            "serviceId": service_id, "body": kwargs,
        })

    def edit_firewall_rule(self, service_id: int, position: int, **kwargs) -> dict:
        return self.call_tool("updateVirtualMachineFirewallRule", {
            "serviceId": service_id, "body": {"position": position, **kwargs},
        })

    def delete_firewall_rule(self, service_id: int, position: int) -> dict:
        return self.call_tool("deleteVirtualMachineFirewallRule", {
            "serviceId": service_id, "body": {"position": position},
        })

    # ISO
    def mount_iso(self, service_id: int, iso_id: str) -> dict:
        return self.call_tool("mountVirtualMachineIso", {
            "serviceId": service_id, "isoId": iso_id,
        })

    def unmount_iso(self, service_id: int) -> dict:
        return self.call_tool("unmountVirtualMachineIso", {"serviceId": service_id})

    # Reverse DNS
    def list_rdns(self, service_id: int) -> list[dict]:
        result = self.call_tool("getVirtualMachineReverseDns", {"serviceId": service_id})
        return self._extract_items(result)

    def set_rdns(self, service_id: int, ip: str, ptr: str) -> dict:
        return self.call_tool("setVirtualMachineReverseDns", {
            "serviceId": service_id, "ip": ip, "hostname": ptr,
        })

    def clear_rdns(self, service_id: int, ip: str) -> dict:
        return self.call_tool("deleteVirtualMachineReverseDns", {
            "serviceId": service_id, "ip": ip,
        })

    # Console
    def get_console_availability(self, service_id: int) -> dict:
        return self.call_tool("getVmConsoleAvailability", {"serviceId": service_id})

    def create_console_session(self, service_id: int) -> dict:
        return self.call_tool("mintVmConsoleSession", {"serviceId": service_id})

    # Templates
    def list_templates(self) -> list[dict]:
        cached = self._cache_get("templates")
        if cached is not None:
            return cached if isinstance(cached, list) else cached.get("items", [])
        result = self.call_tool("listTemplates", {})
        if isinstance(result, dict):
            data = result.get("items", [])
        else:
            data = result if isinstance(result, list) else []
        return self._cache_set("templates", data)

    # Support
    def list_support_departments(self) -> list[dict]:
        result = self.call_tool("listSupportDepartments", {})
        return self._extract_items(result)

    # ── Wait / Poll ──────────────────────────────────────────

    def wait_for_provisioning(
        self, service_id: int, timeout: int = 300, interval: int = 10
    ) -> dict:
        """Poll until VM is active and has an IP assigned."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            vm = self.get_vm(service_id)
            svc = vm.get("service_status", "unknown")
            ips = vm.get("ips", [])
            log.info(
                "VM %s: service=%s, ips=%d", service_id, svc, len(ips)
            )
            if svc == "active" and ips:
                return vm
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
            log.info("Job %s: %s", job_id, status)
            if status in ("completed", "succeeded"):
                return job
            if status in ("failed", "error"):
                raise SHCError("job_failed", f"Job {job_id} failed: {job}")
            time.sleep(interval)
        raise SHCError("timeout", f"Job {job_id} not complete after {timeout}s")

    # ── Health (simplified — delegates to read-only calls) ───

    def check_vm_health(self, service_id: int) -> dict:
        """Return a basic health report. Less detailed than REST version
        (which probes TCP port 22 directly). Uses MCP read-only calls."""
        vm = self.get_vm(service_id)
        summary = self.get_vm_summary(service_id)
        return {
            "service_id": service_id,
            "hostname": vm.get("hostname", ""),
            "service_status": vm.get("service_status", "unknown"),
            "provisioning_state": vm.get("provisioning_state", "unknown"),
            "runtime_status": summary.get("runtime_status"),
            "ip_assigned": vm.get("ips", [{}])[0].get("ip") if vm.get("ips") else None,
            "has_active_job": summary.get("has_active_job", False),
            "note": "MCP transport — limited health detail. Use REST for "
                    "port-22 probing and full diagnostics.",
        }

    # ── Escape hatch ─────────────────────────────────────────

    def call(self, method: str, path: str, **kwargs) -> Any:
        """Escape hatch for endpoints without a named method.

        For MCP transport, this maps the REST path to the closest MCP tool.
        Not all REST paths have MCP equivalents.
        """
        raise SHCError(
            "method_not_found",
            f"MCP transport does not support arbitrary REST calls. "
            f"Use call_tool() with a specific MCP tool name instead. "
            f"Attempted: {method} {path}",
        )

    def list_tools(self) -> list[dict]:
        """List all available MCP tools on the server."""
        self._ensure_initialized()
        resp = self._send_jsonrpc("tools/list", {})
        return resp.get("result", {}).get("tools", [])
