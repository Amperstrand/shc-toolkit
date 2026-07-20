"""
SHC User API client.

Full coverage of the SHC v2 User API: VM lifecycle, ordering, snapshots,
backups, SSH keys, billing, support tickets, account management, firewall,
metrics, ISO, reverse DNS, affiliate, and more.
Base URL: https://blesta.sovereignhybridcompute.com/user-api/v2
"""

from __future__ import annotations

import json as _json
import logging
import os
import socket
import uuid
import time
from datetime import datetime, timezone
from typing import Any

import httpx
import requests

log = logging.getLogger(__name__)

BASE_URL = "https://blesta.sovereignhybridcompute.com/user-api/v2"

_CACHE_TTL = 300


class SHCError(Exception):
    """Base exception for all SHC API errors.

    error_code is a machine-stable identifier (not_found, invalid_token,
    vm_locked, insufficient_credit, upstream_failure, rate_limited, ...)
    that does not change with message wording. Use it for programmatic
    error handling instead of string-matching messages.

    For granular catching, use the specific subclasses:

    - SHCNotFoundError: resource not found (404, error_code=not_found)
    - SHCAuthError: authentication/authorization failure (401/403)
    - SHCRateLimitError: rate limited (429, has retry_after_seconds)
    - SHCConfirmationRequiredError: destructive op needs confirmation (409)
    - SHCServerError: upstream 5xx error
    - InsufficientCreditError: balance too low for an order
    - ProvisioningStuckError: VM stuck in failure pattern
    """

    def __init__(
        self,
        code: str,
        message: str,
        request_id: str | None = None,
        details: Any = None,
        error_code: str | None = None,
        retry_after_seconds: int | None = None,
    ):
        self.code = code
        self.message = message
        self.request_id = request_id
        self.details = details
        self.error_code = error_code
        self.retry_after_seconds = retry_after_seconds
        self.confirmation_id: str | None = None
        super().__init__(
            f"[{error_code or code}] {message}"
            + (f" (req={request_id})" if request_id else "")
            + (f" retry_after={retry_after_seconds}s" if retry_after_seconds else "")
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


class InsufficientCreditError(SHCError):
    """Raised when account balance is too low to complete an order."""

    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        super().__init__(
            "insufficient_credit",
            f"Insufficient credit: need ${required:.2f}, have ${available:.2f}. "
            f"Add credit at https://blesta.sovereignhybridcompute.com/client/",
        )


class SHCNotFoundError(SHCError):
    """Resource not found (HTTP 404)."""


class SHCAuthError(SHCError):
    """Authentication or authorization failure (HTTP 401/403)."""


class SHCRateLimitError(SHCError):
    """Rate limited (HTTP 429). Check retry_after_seconds."""


class SHCConfirmationRequiredError(SHCError):
    """Destructive operation requires confirmation (HTTP 409).

    The confirmation_id is available on the exception instance. The
    _confirmed_request method handles this automatically.
    """


class SHCServerError(SHCError):
    """Upstream server error (HTTP 5xx)."""


_ERROR_CODE_MAP: dict[str, type[SHCError]] = {
    "not_found": SHCNotFoundError,
    "invalid_token": SHCAuthError,
    "unauthorized": SHCAuthError,
    "forbidden": SHCAuthError,
    "rate_limited": SHCRateLimitError,
    "confirmation_required": SHCConfirmationRequiredError,
    "upstream_failure": SHCServerError,
    "internal_error": SHCServerError,
}


def _raise_shc_error(
    code: str,
    message: str,
    request_id: str | None = None,
    details: Any = None,
    error_code: str | None = None,
    retry_after_seconds: int | None = None,
) -> None:
    """Raise the most specific SHCError subclass for the given error_code.

    Falls back to the generic SHCError for unknown error codes.
    """
    ec = error_code or code
    cls = _ERROR_CODE_MAP.get(ec, SHCError)
    exc = cls(code, message, request_id, details, error_code, retry_after_seconds)
    raise exc


class SHCClient:
    """Lightweight client for the SHC User API.

    Usage:
        c = SHCClient()  # reads SHC_API_KEY from env
        vms = c.list_vms()
        summary = c.get_vm_summary(123)

    Auth: Bearer token (API key from /account/api-keys).

    Caching:
        Catalog, templates, balance, and upgrade options are cached with a
        5-minute TTL. Use cache_ttl=0 to disable or call invalidate_cache().
    """

    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL,
                 cache_ttl: int = _CACHE_TTL, max_retries: int = 3,
                 backoff_base: float = 1.0, backoff_cap: float = 60.0):
        self.api_key = api_key or os.environ.get("SHC_API_KEY", "")
        if not self.api_key:
            raise ValueError("SHC_API_KEY not set and no api_key provided")
        self.base_url = base_url
        self.session = httpx.Client(timeout=30.0)
        self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        self._cache_ttl = cache_ttl
        self._cache: dict[str, tuple[float, Any]] = {}
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._backoff_cap = backoff_cap
        self._raw_client: Any = None

        from .cost_audit import CostTracker
        self.cost_tracker = CostTracker(self)

    @property
    def raw(self) -> Any:
        """Access the auto-generated type-safe client (WorkOS pattern).

        Returns a ``shc_toolkit.generated.Client`` (httpx-based) that
        provides 149 endpoint methods with full Pydantic type safety.

        Requires: ``pip install shc-toolkit[generated]``

        Usage::

            from shc_toolkit.generated.api.ordering import get_ordering_catalog
            c = SHCClient()
            catalog = get_ordering_catalog.sync(client=c.raw)
        """
        if self._raw_client is None:
            try:
                from .generated import Client
            except ImportError as e:
                raise ImportError(
                    "Generated client requires httpx + attrs. "
                    "Install with: pip install shc-toolkit[generated]"
                ) from e
            self._raw_client = Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
            )  # type: ignore[call-arg]
        return self._raw_client

    # ── Cache ───────────────────────────────────────────────

    def _cache_get(self, key: str) -> Any | None:
        if self._cache_ttl <= 0:
            return None
        entry = self._cache.get(key)
        if entry is None:
            return None
        ts, data = entry
        if time.time() - ts > self._cache_ttl:
            del self._cache[key]
            return None
        return data

    def _cache_set(self, key: str, data: Any) -> Any:
        if self._cache_ttl > 0:
            self._cache[key] = (time.time(), data)
        return data

    def invalidate_cache(self, prefix: str | None = None):
        """Clear cached data. If prefix given, only clear keys starting with it."""
        if prefix is None:
            self._cache.clear()
        else:
            self._cache = {k: v for k, v in self._cache.items() if not k.startswith(prefix)}

    # ── Credit ──────────────────────────────────────────────

    def get_available_credit(self) -> float:
        """Return available USD credit. Cached for cache_ttl seconds."""
        cached = self._cache_get("credit")
        if cached is not None:
            return cached
        result = self._get("/billing/balance")
        balances = result.get("balances", result.get("credit", []))
        for b in balances:
            if b.get("currency") == "USD":
                amt = float(b.get("available_credit", b.get("amount", 0)))
                return self._cache_set("credit", amt)
        return 0.0

    def check_credit(self, required: float) -> None:
        """Raise InsufficientCreditError if balance < required."""
        available = self.get_available_credit()
        if available < required:
            raise InsufficientCreditError(required, available)

    def estimate_daily_cost(self, package_id: int) -> float:
        """Look up daily price for a package. Cached."""
        cache_key = f"price:{package_id}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached
        for pkg in self.get_catalog():
            if pkg.get("package_id") == package_id:
                daily: dict = next((p for p in pkg.get("pricing", []) if p.get("period") == "day"), {})
                price = float(daily.get("price", 0))
                return self._cache_set(cache_key, price)
        return 0.0

    def _safe_credit(self) -> float | None:
        """Get available credit, returning None on failure (never raises)."""
        try:
            self.invalidate_cache("credit")
            return self.get_available_credit()
        except Exception:
            return None

    # ── Internal ─────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if "json" in kwargs:
            self.session.headers["Content-Type"] = "application/json"
        elif "Content-Type" in self.session.headers:
            del self.session.headers["Content-Type"]

        for attempt in range(self._max_retries):
            try:
                resp = self.session.request(method, url, timeout=30, **kwargs)
            except httpx.HTTPError:
                if attempt == self._max_retries - 1:
                    raise
                time.sleep(self._backoff_delay(attempt))
                continue

            if resp.status_code in (408, 429):
                retry_after = self._parse_retry_after(resp, attempt)
                time.sleep(retry_after)
                continue

            if resp.status_code >= 500 and attempt < self._max_retries - 1:
                time.sleep(self._backoff_delay(attempt))
                continue
            break

        text = resp.text
        body = _json.loads(text) if text.strip() else {}
        if resp.status_code >= 400:
            err = body.get("error", {})
            code = err.get("code", "unknown")
            message = err.get("message", resp.text)
            request_id = err.get("request_id")
            details = err.get("details")
            error_code = err.get("error_code")
            retry_after = err.get("retry_after_seconds")
            ec = error_code or code
            cls = _ERROR_CODE_MAP.get(ec, SHCError)
            exc = cls(code, message, request_id, details, error_code, retry_after)
            conf = body.get("confirmation", {})
            if conf:
                exc.confirmation_id = (
                    conf.get("confirmation_id")
                    or conf.get("structuredContent", {}).get("confirmation_id")
                )
            raise exc
        return body.get("data", body)

    def _backoff_delay(self, attempt: int) -> float:
        import random
        delay = min(self._backoff_cap, self._backoff_base * (2 ** attempt))
        jitter = delay * 0.2 * random.uniform(-1, 1)
        return min(self._backoff_cap, max(0, delay + jitter))

    def _parse_retry_after(self, resp, attempt: int) -> float:
        """Extract retry delay from 429 response, falling back to backoff."""
        retry_after = resp.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
        text = resp.text
        try:
            body = _json.loads(text[text.find("{"):]) if "{" in text else {}
            err = body.get("error", {})
            seconds = err.get("retry_after_seconds")
            if seconds:
                return float(seconds)
        except Exception:
            pass
        return self._backoff_delay(attempt)

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

    def _get_items(self, path: str, params: dict | None = None) -> list[dict]:
        return self._request("GET", path, params=params).get("items", [])

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

        Generates an Idempotency-Key once per call so the original
        request and the confirmation re-send share the same key.
        """
        idem_key = f"shc-{uuid.uuid4().hex[:24]}"
        headers = dict(kwargs.pop("headers", None) or {})
        if "Idempotency-Key" not in headers:
            headers["Idempotency-Key"] = idem_key
        kwargs["headers"] = headers
        try:
            return self._request(method, path, **kwargs)
        except SHCError as e:
            if not confirm or e.code != "confirmation_required":
                raise
            cid = getattr(e, "confirmation_id", None)
            if not cid:
                raise
            headers["X-User-Api-Confirm"] = cid
            return self._request(method, path, **kwargs)

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
        return self._get_items("/account/api-keys")

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

    @staticmethod
    def claim_agent_key(code: str, *, base_url: str | None = None) -> dict:
        """Claim a single-use agent API key by claim code.

        This endpoint is PUBLIC (``security: []``) — it does not require an
        authenticated ``SHCClient`` because the typical caller is an agent that
        does not yet hold any API key. The operator (who does have credentials)
        mints a key and hands the agent only the single-use claim code; the
        agent exchanges it here exactly once and receives the plaintext key,
        which is never recoverable again.

        Args:
            code: Single-use claim code (base64url, 22-128 chars). Burned on success.
            base_url: Override the default SHC API base URL.

        Returns:
            The claimed key material (``{"api_key": "shc_live_..."}`` shape).

        Raises:
            SHCError: 404 (unknown/expired/already-claimed — indistinguishable
                by design), 422 (malformed code), or 429 (rate limited).
        """
        url = f"{base_url or BASE_URL}/agent-keys/claim"
        resp = requests.post(url, json={"code": code}, timeout=30,
                             headers={"Content-Type": "application/json"})
        text = resp.text
        json_start = text.find("{")
        if json_start > 0:
            text = text[json_start:]
        body = _json.loads(text) if text.strip() else {}
        if resp.status_code >= 400:
            err = body.get("error", {})
            raise SHCError(
                err.get("code", "unknown"),
                err.get("message", resp.text),
                err.get("request_id"),
                err.get("details"),
            )
        return body.get("data", body)

    # ── Contacts ─────────────────────────────────────────────

    def list_contacts(self) -> list[dict]:
        return self._get_items("/contacts")

    def create_contact(self, **kwargs) -> dict:
        return self._post("/contacts", kwargs)

    def get_contact(self, contact_id: int) -> dict:
        return self._get(f"/contacts/{contact_id}")

    def delete_contact(self, contact_id: int) -> dict:
        return self._delete(f"/contacts/{contact_id}")

    def list_contact_permissions(self) -> list[dict]:
        return self._get_items("/contacts/permission-options")

    # ── Support Tickets ──────────────────────────────────────

    def list_support_departments(self) -> list[dict]:
        return self._get_items("/support/departments")

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
        return self._get_items("/kb")

    def search_kb(self, query: str) -> list[dict]:
        return self._get_items("/kb/search", params={"q": query})

    def get_kb_article(self, article_id: int) -> dict:
        return self._get(f"/kb/{article_id}")

    # ── Account Managers ─────────────────────────────────────

    def list_managed_accounts(self) -> list[dict]:
        return self._get_items("/managed-accounts")

    def list_managers(self) -> list[dict]:
        return self._get_items("/managers")

    def invite_manager(self, email: str, permissions: list[str] | None = None) -> dict:
        data: dict[str, Any] = {"email": email}
        if permissions:
            data["permissions"] = permissions
        return self._post("/managers", data)

    def list_manager_permissions(self) -> list[dict]:
        return self._get_items("/managers/permission-options")

    def get_billing_balance(self) -> dict:
        return self._get("/billing/balance")

    # ── Billing & Payments ───────────────────────────────────

    def list_invoices(self, **params) -> dict:
        return self._get("/invoices", params=params if params else None)

    def get_invoice(self, invoice_id: int) -> dict:
        return self._get(f"/invoices/{invoice_id}")

    def get_invoice_pdf_url(self, invoice_id: int) -> str:
        return f"{self.base_url}/invoices/{invoice_id}/pdf"

    def pay_invoice(self, invoice_id: int, idempotency_key: str | None = None) -> dict:
        if idempotency_key is None:
            idempotency_key = f"shc-{uuid.uuid4().hex[:24]}"
        return self._post(
            f"/payment/{invoice_id}/checkout",
            {"gateway": "btcpay_server", "idempotency_key": idempotency_key},
        )

    def get_payment(self, invoice_id: int) -> dict:
        return self._get(f"/payment/{invoice_id}")

    def list_payment_methods(self) -> list[dict]:
        return self._get_items("/payment-methods")

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
        return self._get_items("/quotations")

    def get_quotation(self, quotation_id: int) -> dict:
        return self._get(f"/quotations/{quotation_id}")

    def get_quotation_invoices(self, quotation_id: int) -> list[dict]:
        return self._get_items(f"/quotations/{quotation_id}/invoices")

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
        return self._get_items("/affiliate/payouts")

    def request_affiliate_payout(self, amount: str, currency: str = "BTC") -> dict:
        return self._post("/affiliate/payouts", {"amount": amount, "currency": currency})

    def list_affiliate_referrals(self) -> list[dict]:
        return self._get_items("/affiliate/referrals")

    # ── Ordering ─────────────────────────────────────────────

    def get_catalog(self, view: str = "full") -> list[dict]:
        """List buyable VM plans. Cached for cache_ttl seconds."""
        cache_key = f"catalog:{view}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached
        params = {"view": view} if view != "full" else None
        data = self._get("/ordering/catalog", params=params).get("items", [])
        return self._cache_set(cache_key, data)

    def get_config_options(self, package_id: int) -> dict[str, dict]:
        """Return config options for a package from the live catalog.

        Each option (ram, cpu, disk, ipv4s, template, gui_choice) has an
        option_id and a list of selectable values. Option IDs differ per
        package, so always read them from the catalog rather than hardcoding.

        Returns:
            Dict keyed by option name with option_id, label, and values.
        """
        for pkg in self.get_catalog():
            if pkg.get("package_id") != package_id:
                continue
            opts: dict[str, dict] = {}
            for block in pkg.get("available_config_options", []):
                for opt in block.get("options", []):
                    if opt["name"] in opts:
                        continue
                    opts[opt["name"]] = {
                        "option_id": opt["option_id"],
                        "label": opt.get("label", opt["name"]),
                        "values": [
                            v["value"] for v in opt.get("values", [])
                        ],
                    }
            return opts
        return {}

    def resolve_addons(
        self,
        package_id: int,
        *,
        ram_mb: int | None = None,
        cpu: int | None = None,
        disk_gb: int | None = None,
        template: str | None = None,
    ) -> dict[str, str]:
        """Translate friendly resource specs into SHC's config_options map.

        Args:
            package_id: Target package.
            ram_mb: Desired total RAM in MB (must be an available value).
            cpu: Desired total vCPU cores (must be an available value).
            disk_gb: Desired total disk in GB (must be an available value).
            template: OS template slug (e.g. "debian12-cloud").

        Returns:
            Dict of {option_id_str: value_str} for use in order/upgrade calls.

        Raises:
            ValueError: If a requested value is not available for the package.
        """
        opts = self.get_config_options(package_id)
        if not opts:
            raise ValueError(
                f"package_id {package_id} not found in catalog"
            )
        out: dict[str, str] = {}

        spec_map = [
            (ram_mb, "ram", ram_mb),
            (cpu, "cpu", cpu),
            (disk_gb, "disk", disk_gb),
        ]
        for requested, opt_name, raw_val in spec_map:
            if requested is None:
                continue
            opt = opts.get(opt_name)
            if not opt:
                raise ValueError(
                    f"Package {package_id} does not expose a '{opt_name}' option"
                )
            val_str = str(raw_val)
            if val_str not in opt["values"]:
                raise ValueError(
                    f"Package {package_id} {opt_name}={val_str} not available. "
                    f"Valid: {', '.join(opt['values'])}"
                )
            out[str(opt["option_id"])] = val_str

        if template is not None:
            opt = opts.get("template")
            if not opt:
                raise ValueError(
                    f"Package {package_id} does not expose a 'template' option"
                )
            if template not in opt["values"]:
                raise ValueError(
                    f"Template '{template}' not available for package {package_id}. "
                    f"Valid: {', '.join(opt['values'][:10])}..."
                )
            out[str(opt["option_id"])] = template

        return out

    def order_vm(
        self,
        *,
        hostname: str,
        size: str | None = None,
        package_id: int | None = None,
        pricing_id: int | None = None,
        ssh_key: str | None = None,
        ram_mb: int | None = None,
        cpu: int | None = None,
        disk_gb: int | None = None,
        template: str | None = None,
        config_options: dict[str, str] | None = None,
        check_credit: bool = True,
        pay: bool = True,
        **kwargs,
    ) -> dict:
        """Order a VM with friendly parameters.

        Either ``size`` or ``package_id``+``pricing_id`` selects the base plan.
        Resource add-ons (ram_mb, cpu, disk_gb, template) are translated to the
        package's config_options via resolve_addons(). Pass raw config_options
        directly to bypass translation.

        Args:
            hostname: VM hostname.
            size: Spec-encoding name like ``nvme-2c-8gb``. See sizes.SIZE_MAP.
            package_id: Raw package ID (alternative to size).
            pricing_id: Raw pricing ID (defaults to daily term for package).
            ssh_key: Path to SSH public key file.
            ram_mb, cpu, disk_gb, template: Add-ons resolved to config_options.
            config_options: Raw {option_id: value} map (overrides add-on kwargs).
            check_credit: Pre-check balance before submitting (default True).
            pay: Auto-pay after order (default True).
        """
        from .sizes import resolve_size

        if size and not package_id:
            package_id, pricing_id = resolve_size(size)
        if not package_id:
            raise ValueError("Either size= or package_id= is required")

        if config_options is None:
            addon_kwargs = {
                k: v for k, v in [
                    ("ram_mb", ram_mb), ("cpu", cpu),
                    ("disk_gb", disk_gb), ("template", template),
                ] if v is not None
            }
            if addon_kwargs:
                config_options = self.resolve_addons(package_id, **addon_kwargs)  # type: ignore[arg-type]

        if ssh_key:
            from pathlib import Path
            p = Path(ssh_key).expanduser()
            if p.exists():
                kwargs.setdefault("ssh_key", p.read_text().strip())

        order_kwargs: dict = {
            "package_id": package_id,
            "hostname": hostname,
            **kwargs,
        }
        if pricing_id:
            order_kwargs["pricing_id"] = pricing_id
        if config_options:
            order_kwargs["config_options"] = config_options

        credit_before = self._safe_credit()
        result = self.submit_order(
            check_credit=check_credit,
            include_dev_vps_options=not config_options,
            **order_kwargs,
        )
        if pay and result.get("invoice_id"):
            self.pay_invoice(result["invoice_id"])

        return result

    def preview_order(self, **kwargs) -> dict:
        return self._post("/ordering/preview", kwargs)

    def submit_order(
        self,
        idempotency_key: str | None = None,
        *,
        include_dev_vps_options: bool = True,
        check_credit: bool = True,
        **kwargs,
    ) -> dict:
        """Submit a VM order with auto-confirmation, idempotency, and credit pre-check.

        When check_credit is True (default), queries the daily price for the
        selected package and raises InsufficientCreditError if the balance is
        too low. This prevents creating orders that can't be paid.

        When include_dev_vps_options is True (default) and the caller has not
        already supplied order_form_id/options, injects the Dev VPS defaults.
        """
        import uuid
        kwargs.pop("pay", None)

        if check_credit:
            pkg_id = kwargs.get("package_id", 0)
            if pkg_id:
                daily_cost = self.estimate_daily_cost(pkg_id)
                if daily_cost > 0:
                    self.check_credit(daily_cost)

        if "config_options" in kwargs and not kwargs["config_options"]:
            del kwargs["config_options"]
        if include_dev_vps_options and "config_options" not in kwargs and "options" not in kwargs:
            kwargs.setdefault("order_form_id", 11)
        idem = idempotency_key or f"order-{uuid.uuid4().hex[:24]}"
        headers = {"Idempotency-Key": idem}
        credit_before = self._safe_credit()
        result = self._confirmed_request(
            "POST", "/ordering/submit", json=kwargs, headers=headers
        )

        pkg_id = kwargs.get("package_id", 0)
        service_ids = result.get("service_ids") or (
            [result["service_id"]] if result.get("service_id") else []
        )
        for sid in service_ids:
            if sid not in self.cost_tracker._sessions:
                self.cost_tracker.track_order(sid, pkg_id, credit_before)

        return result

    # ── VM Lifecycle ─────────────────────────────────────────

    def list_vms(self) -> list[dict]:
        return self._get_items("/vm")

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

    def standby_vm(self, service_id: int, *, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/standby", confirm=confirm,
        )

    def preview_standby(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/standby/preview")

    def resume_vm(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/resume")

    def cancel_vm(self, service_id: int, *, immediate: bool = True, confirm: bool = True) -> dict:
        result = self._confirmed_request(
            "POST", f"/vm/{service_id}/cancel", confirm=confirm,
            json={"immediate": True} if immediate else {},
        )
        self.invalidate_cache("credit")
        if immediate:
            credit_after = self._safe_credit()
            self.cost_tracker.audit_cancel(service_id, credit_after)
        return result

    def reap_orphans(
        self,
        *,
        max_age_hours: float = 2.0,
        hostname_prefixes: list[str] | None = None,
        exclude_hostnames: list[str] | None = None,
        dry_run: bool = False,
    ) -> list[dict]:
        """Destroy orphaned VMs that match test patterns and exceed max age.

        Identifies VMs whose hostname starts with a known test prefix and
        whose age exceeds max_age_hours, then cancels them immediately.

        Args:
            max_age_hours: Destroy VMs older than this (default: 2 hours).
            hostname_prefixes: List of prefixes to match (default: test patterns).
            exclude_hostnames: Never destroy these hostnames (default: production).
            dry_run: If True, report what would be destroyed without cancelling.

        Returns:
            List of destroyed (or would-be-destroyed) VM dicts.
        """
        from datetime import datetime, timezone

        if hostname_prefixes is None:
            hostname_prefixes = [
                "tf-acc-",
                "tollgate-",
                "test-",
                "tmp-",
                "ci-",
            ]

        if exclude_hostnames is None:
            exclude_hostnames = [
                "europa-vpn-vps",
            ]

        now = datetime.now(timezone.utc)
        orphans = []

        for vm in self.list_vms():
            hostname = vm.get("hostname", "")
            vm_id = vm.get("id")
            status = vm.get("service_status", "")

            if status in ("canceled", "suspended"):
                continue

            if hostname in exclude_hostnames:
                log.debug(f"reap: skipping excluded hostname {hostname}")
                continue

            is_test_vm = any(hostname.startswith(p) for p in hostname_prefixes)
            if not is_test_vm:
                log.debug(f"reap: skipping non-test hostname {hostname}")
                continue

            created_str = vm.get("date_created", "")
            try:
                created = datetime.fromisoformat(
                    created_str.replace("Z", "+00:00").replace(" ", "T")
                )
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                log.warning(f"reap: cannot parse date_created='{created_str}' for VM {vm_id}")
                continue

            age_hours = (now - created).total_seconds() / 3600
            if age_hours < max_age_hours:
                log.debug(f"reap: {hostname} is {age_hours:.1f}h old (< {max_age_hours}h threshold)")
                continue

            orphan = {
                "id": vm_id,
                "hostname": hostname,
                "age_hours": round(age_hours, 1),
                "status": status,
                "package": vm.get("package", "?"),
            }
            orphans.append(orphan)

            if dry_run:
                log.info(f"reap [dry-run]: would destroy {hostname} (ID={vm_id}, {age_hours:.1f}h old)")
            else:
                try:
                    self.cancel_vm(vm_id, immediate=True)
                    log.info(f"reap: destroyed {hostname} (ID={vm_id}, {age_hours:.1f}h old)")
                except Exception as e:
                    log.error(f"reap: failed to destroy {hostname} (ID={vm_id}): {e}")
                    orphan["error"] = str(e)

        return orphans

    def reinstall_vm(self, service_id: int, *, confirm: bool = True, **kwargs) -> dict:
        return self._confirmed_request(
            "PATCH", f"/vm/{service_id}/reinstall", confirm=confirm, json=kwargs
        )

    def rekey_zk_backup(
        self,
        service_id: int,
        zk_backup: dict[str, Any],
        *,
        confirm: bool = True,
    ) -> dict:
        """Rekey (rotate) a VM's zero-knowledge backup registration.

        DESTRUCTIVE: installs a NEW ZK backup key generation; prior-generation
        encrypted backups become UNRECOVERABLE by design. Requires a two-step
        confirmation (handled automatically when ``confirm=True``): the first
        call returns a 409 with a ``confirmation_id``, the second resubmits
        with the ``X-User-Api-Confirm`` header.

        Args:
            service_id: SHC service ID of the VM.
            zk_backup: ``ZkBackupRegistration`` payload — client-derived X25519
                pubkeys + immutable KDF config (see openapi.json schema).
            confirm: Auto-handle the confirmation_required 409 flow (default True).
        """
        return self._confirmed_request(
            "POST",
            f"/vm/{service_id}/zk-backup/rekey",
            confirm=confirm,
            json={"destroy_ack": "DESTROY-MY-BACKUPS", "zk_backup": zk_backup},
        )

    def get_vm_detail(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/detail")

    def get_vm_activity(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/activity")

    def get_vm_metrics(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/metrics")

    def get_vm_bandwidth(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/bandwidth")

    def get_vm_network(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/network")

    def list_upgrade_options(self, service_id: int) -> list[dict]:
        result = self._get(f"/vm/{service_id}/upgrade-options")
        return result.get("upgradable", result.get("items", []))

    def preview_upgrade(self, service_id: int, pricing_ref: int) -> dict:
        return self._post(f"/vm/{service_id}/upgrade/preview", {"pricing_ref": pricing_ref})

    def upgrade_vm(self, service_id: int, pricing_ref: int, *, confirm: bool = True) -> dict:
        import uuid
        return self._confirmed_request(
            "PATCH", f"/vm/{service_id}/upgrade", confirm=confirm,
            json={"pricing_ref": pricing_ref, "idempotency_key": f"upgrade-{uuid.uuid4().hex[:24]}"},
        )

    def get_vm_payments(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/payments")

    def get_vm_renewal_quote(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/renew")

    # ── VM term + addons (v2.4.3) ─────────────────────────────

    def list_vm_addons(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/addons")

    def get_vm_addon_options(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/addons/options")

    def create_vm_addon(self, service_id: int, *, confirm: bool = True, **kwargs) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/addons", confirm=confirm, json=kwargs,
        )

    def preview_vm_addon(self, service_id: int, **kwargs) -> dict:
        return self._post(f"/vm/{service_id}/addons/preview", kwargs)

    def get_vm_term_options(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/term-options")

    def change_vm_term(self, service_id: int, *, confirm: bool = True, **kwargs) -> dict:
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/term", confirm=confirm, json=kwargs,
        )

    def preview_vm_term_change(self, service_id: int, **kwargs) -> dict:
        return self._post(f"/vm/{service_id}/term/preview", kwargs)

    # ── Orders (v2.4.3) ───────────────────────────────────────

    def list_orders(self, **params) -> list[dict]:
        return self._get_items("/orders", params=params or None)

    def get_order(self, order_id: int) -> dict:
        return self._get(f"/orders/{order_id}")

    def cancel_pending_order(self, order_id: int, *, confirm: bool = True) -> dict:
        return self._confirmed_request(
            "POST", f"/orders/{order_id}/cancel", confirm=confirm,
        )

    # ── Agent sessions + events (v2.4.6) ─────────────────────

    def list_agent_sessions(self, **params) -> list[dict]:
        return self._get_items("/agent-sessions", params=params or None)

    def create_agent_session(self, **kwargs) -> dict:
        return self._post("/agent-sessions", kwargs)

    def get_agent_session(self, session_id: str) -> dict:
        return self._get(f"/agent-sessions/{session_id}")

    def delete_agent_session(self, session_id: str) -> dict:
        return self._delete(f"/agent-sessions/{session_id}")

    def get_agent_session_audit(self, session_id: str) -> dict:
        return self._get(f"/agent-sessions/{session_id}/audit")

    def list_events(self, **params) -> list[dict]:
        return self._get_items("/events", params=params or None)

    # ── Snapshots ────────────────────────────────────────────

    def list_snapshots(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/snapshots")

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

    def verify_snapshot(self, service_id: int, snapshot_id: str) -> dict:
        return self._post(f"/vm/{service_id}/snapshots/verify", {"snapshot_id": snapshot_id})

    def set_snapshot_protection(self, service_id: int, snapshot_id: str, protected: bool) -> dict:
        return self._patch(f"/vm/{service_id}/snapshots/protection", {"snapshot_id": snapshot_id, "protected": protected})

    def get_snapshot_restore_hints(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/snapshots/restore-hints")

    # ── Backups ──────────────────────────────────────────────

    def list_backups(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/backups")

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

    def verify_backup(self, service_id: int, backup_id: str) -> dict:
        return self._post(f"/vm/{service_id}/backups/verify", {"backup_id": backup_id})

    def get_backup_restore_hints(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/backups/restore-hints")

    def list_file_restore_sources(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/file-restore/sources")

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
        items = self._get_items("/ssh-key")
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
        return self._confirmed_request(
            "POST", f"/vm/{service_id}/ssh-keys/apply-live",
            json={"ssh_key": public_key},
        )

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
        return self._get_items(f"/vm/{service_id}/iso")

    def mount_iso(self, service_id: int, iso_id: str) -> dict:
        return self._post(f"/vm/{service_id}/iso/mount", {"iso_id": iso_id})

    def unmount_iso(self, service_id: int) -> dict:
        return self._post(f"/vm/{service_id}/iso/unmount")

    # ── Reverse DNS ──────────────────────────────────────────

    def list_rdns(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/rdns")

    def set_rdns(self, service_id: int, ip: str, ptr: str) -> dict:
        return self._post(f"/vm/{service_id}/rdns", {"ip": ip, "ptr": ptr})

    def clear_rdns(self, service_id: int, ip: str) -> dict:
        return self._delete(f"/vm/{service_id}/rdns", params={"ip": ip})

    # ── Console ──────────────────────────────────────────────

    def get_console_availability(self, service_id: int) -> dict:
        return self._get(f"/vm/{service_id}/console")

    def create_console_session(self, service_id: int, *, ttl: int | None = None) -> dict:
        body: dict[str, Any] = {}
        if ttl is not None:
            body["ttl"] = ttl
        return self._post(f"/vm/{service_id}/console/session", body)

    # ── Templates ────────────────────────────────────────────

    def list_templates(self) -> list[dict]:
        cached = self._cache_get("templates")
        if cached is not None:
            return cached
        return self._cache_set("templates", self._get("/vm/templates").get("items", []))

    def list_images(self) -> list[dict]:
        return self._get_items("/image")

    # ── Jobs ─────────────────────────────────────────────────

    def list_jobs(self, service_id: int) -> list[dict]:
        return self._get_items(f"/vm/{service_id}/jobs")

    def get_job(self, service_id: int, job_id: str) -> dict:
        return self._get(f"/vm/{service_id}/jobs/{job_id}")

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

        Gathers data from /vm, /vm/summary (includes runtime since v2.4.0),
        /firewall, /activity, and /bandwidth, probes TCP port 22, and
        classifies the VM's state into a diagnosis_code.
        """
        vm = self.get_vm(service_id)
        summary = self.get_vm_summary(service_id)
        firewall = self.get_firewall(service_id)
        activity = self.get_vm_activity(service_id)
        bandwidth = self.get_vm_bandwidth(service_id)

        hostname = vm.get("hostname", "")
        service_status = vm.get("service_status", "unknown")
        provisioning_state = vm.get("provisioning_state", "unknown")
        bootstrap_completed_at = vm.get("bootstrap_completed_at")

        rt = summary.get("runtime") or {}
        runtime_status = rt.get("raw_status") or rt.get("state") or summary.get("runtime_status")

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
            ip_assigned=ip_assigned,
            port_22_reachable=port_22_reachable,
            runtime_status=runtime_status,
            activity_count=activity_count,
        )

        return {
            "service_id": service_id,
            "hostname": hostname,
            "age_seconds": age_seconds,
            "service_status": service_status,
            "provisioning_state": provisioning_state,
            "bootstrap_completed_at": bootstrap_completed_at,
            "runtime_status": runtime_status,
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
        ip_assigned: str | None,
        port_22_reachable: bool,
        runtime_status: str | None,
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
        if (
            ip_assigned
            and not port_22_reachable
            and runtime_status == "running"
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
