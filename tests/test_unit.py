"""Unit tests for shc_toolkit — no live API required.

Tests the transport abstraction, factory selection, MCP JSON-RPC protocol
layer, confirmation flow, and client bug fixes using mocks.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

import httpx

from shc_toolkit.transport import SHCTransport, resolve_transport
from shc_toolkit.client import SHCClient, SHCError


# ── Transport Selection ────────────────────────────────────


class TestResolveTransport:
    def test_explicit_rest(self):
        assert resolve_transport("rest") == "rest"

    def test_explicit_mcp(self):
        assert resolve_transport("mcp") == "mcp"

    def test_env_var(self):
        with patch.dict(os.environ, {"SHC_TRANSPORT": "mcp"}):
            assert resolve_transport() == "mcp"

    def test_default_is_rest(self):
        env = {k: v for k, v in os.environ.items() if k != "SHC_TRANSPORT"}
        with patch.dict(os.environ, env, clear=True):
            assert resolve_transport() == "rest"

    def test_auto_falls_back_to_rest_without_mcp_dep(self):
        assert resolve_transport("auto") == "rest"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="Invalid transport"):
            resolve_transport("grpc")


class TestCreateClient:
    def test_rest_returns_shcclient(self):
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            from shc_toolkit import create_client
            c = create_client(transport="rest")
            assert isinstance(c, SHCClient)

    def test_mcp_transport_creates_mcp_client(self):
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            from shc_toolkit import create_client
            c = create_client(transport="mcp")
            from shc_toolkit.mcp_client import SHCMCPClient
            assert isinstance(c, SHCMCPClient)

    def test_no_api_key_raises(self):
        env = {k: v for k, v in os.environ.items() if k != "SHC_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            from shc_toolkit import create_client
            with pytest.raises(ValueError, match="SHC_API_KEY not set"):
                create_client(transport="rest")


class TestProtocolCompliance:
    def test_shcclient_is_transport(self):
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            assert isinstance(c, SHCTransport)

    def test_protocol_has_core_methods(self):
        expected = [
            "list_vms", "get_vm", "get_vm_summary", "start_vm",
            "stop_vm", "restart_vm", "cancel_vm", "get_catalog",
            "submit_order", "list_backups", "list_jobs", "get_account",
        ]
        for method in expected:
            assert hasattr(SHCTransport, method), f"Protocol missing {method}"


# ── Client Bug Fixes ───────────────────────────────────────


class TestClientBugFixes:
    def test_no_duplicate_billing_methods(self):
        import inspect
        src = inspect.getsource(SHCClient)
        assert src.count("def list_invoices(") == 1
        assert src.count("def get_invoice(") == 1
        assert src.count("def pay_invoice(") == 1

    def test_get_catalog_has_no_view_param(self):
        """get_catalog() uses the static model — no view parameter needed."""
        import inspect
        sig = inspect.signature(SHCClient.get_catalog)
        assert "view" not in sig.parameters
        assert "self" in sig.parameters


# ── MCP Client (mocked HTTP) ───────────────────────────────


def _mock_response(status_code=200, content_type="application/json", text="", headers=None):
    """Build a mock requests.Response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.headers = {"Content-Type": content_type}
    if headers:
        resp.headers.update(headers)
    resp.text = text
    return resp


def _jsonrpc_result(data, rpc_id=1):
    """Build a mock MCP tools/call success response."""
    inner = {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps(data)}],
            "isError": False,
            "structuredContent": {"data": data},
        },
    }
    return _mock_response(text=json.dumps(inner))


def _jsonrpc_error(code, message, rpc_id=1, structured=None):
    """Build a mock MCP tools/call error response."""
    sc = structured or {"http_status": 500, "error": {"code": code, "message": message}}
    inner = {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": {
            "content": [{"type": "text", "text": f"Error: {message}"}],
            "isError": True,
            "structuredContent": sc,
        },
    }
    return _mock_response(text=json.dumps(inner))


class TestMcpResponseParser:
    def test_parses_plain_json(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = _mock_response(
            content_type="application/json",
            text='{"jsonrpc":"2.0","id":1,"result":{}}',
        )
        body = SHCMCPClient._parse_mcp_response(resp)
        assert body["jsonrpc"] == "2.0"

    def test_parses_json_with_log_prefix(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = _mock_response(
            content_type="application/json",
            text='Authorized access only.\n{"jsonrpc":"2.0","id":1,"result":{}}',
        )
        body = SHCMCPClient._parse_mcp_response(resp)
        assert body["jsonrpc"] == "2.0"

    def test_returns_empty_for_non_json_content_type(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = _mock_response(
            status_code=202,
            content_type="text/html",
            text="Accepted\n",
        )
        body = SHCMCPClient._parse_mcp_response(resp)
        assert body == {}

    def test_parses_sse(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        sse_text = 'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"tools":[]}}\n\n'
        resp = _mock_response(content_type="text/event-stream", text=sse_text)
        body = SHCMCPClient._parse_mcp_response(resp)
        assert body["jsonrpc"] == "2.0"


class TestMcpUnwrapResult:
    def test_extracts_structured_content_data(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {"isError": False, "structuredContent": {"data": {"credit": []}}}}
        data = SHCMCPClient._unwrap_tool_result(resp)
        assert data == {"credit": []}

    def test_unwraps_double_wrapped_data(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {"isError": False, "structuredContent": {
            "data": {"data": {"service_ids": [123], "order": {"id": 1}}}
        }}}
        data = SHCMCPClient._unwrap_tool_result(resp)
        assert data == {"service_ids": [123], "order": {"id": 1}}

    def test_extracts_text_content_fallback(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {"content": [{"type": "text", "text": '{"key": "val"}'}]}}
        data = SHCMCPClient._unwrap_tool_result(resp)
        assert data == {"key": "val"}

    def test_raises_on_is_error(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {
            "result": {
                "isError": True,
                "structuredContent": {
                    "http_status": 401,
                    "error": {"code": "unauthorized", "message": "Auth failed"},
                },
            }
        }
        with pytest.raises(SHCError, match="Auth failed"):
            SHCMCPClient._unwrap_tool_result(resp)

    def test_returns_result_dict_for_empty_content(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {}}
        data = SHCMCPClient._unwrap_tool_result(resp)
        assert data == {}


class TestMcpConvertArgs:
    def test_snake_to_camel(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        result = SHCMCPClient._convert_args({"service_id": 123, "package_id": 456})
        assert result == {"serviceId": 123, "packageId": 456}

    def test_passthrough_no_underscore(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        result = SHCMCPClient._convert_args({"name": "test", "limit": 10})
        assert result == {"name": "test", "limit": 10}

    def test_empty_kwargs(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        assert SHCMCPClient._convert_args({}) == {}


class TestMcpToolMap:
    def test_core_tool_count(self):
        from shc_toolkit.mcp_client import TOOL_MAP
        assert len(TOOL_MAP) == 157

    def test_key_mappings(self):
        from shc_toolkit.mcp_client import TOOL_MAP
        assert TOOL_MAP["list_vms"] == "listVirtualMachines"
        assert TOOL_MAP["get_account"] == "getAccount"
        assert TOOL_MAP["cancel_vm"] == "cancelVirtualMachine"
        assert TOOL_MAP["get_catalog"] == "getOrderingCatalog"

    def test_reverse_map(self):
        from shc_toolkit.mcp_client import METHOD_MAP
        assert METHOD_MAP["listVirtualMachines"] == "list_vms"
        assert METHOD_MAP["getAccount"] == "get_account"

    def test_v243_tool_map_entries(self):
        """All 25 new v2.4.3 MCP tools must be in TOOL_MAP."""
        from shc_toolkit.mcp_client import TOOL_MAP
        v243_entries = {
            "list_vm_addons", "get_vm_addon_options", "create_vm_addon",
            "preview_vm_addon", "get_vm_term_options", "change_vm_term",
            "preview_vm_term_change", "list_orders", "get_order",
            "cancel_pending_order", "list_quotations", "get_quotation",
            "approve_quotation", "list_quotation_invoices",
            "list_documents", "download_document", "list_downloads",
            "download_file", "get_support_ticket_attachment",
            "submit_support_ticket_feedback", "get_invoice_electronic",
        }
        missing = v243_entries - set(TOOL_MAP.keys())
        assert not missing, f"Missing v2.4.3 TOOL_MAP entries: {missing}"

    def test_v243_mcp_methods_exist(self):
        """Every TOOL_MAP entry must have a corresponding SHCMCPClient method."""
        from shc_toolkit.mcp_client import TOOL_MAP, SHCMCPClient
        missing = [name for name in TOOL_MAP if not hasattr(SHCMCPClient, name)]
        assert not missing, f"SHCMCPClient missing methods for TOOL_MAP entries: {missing}"

    def test_v243_rest_methods_exist(self):
        """Tier 1+2 new endpoints must have REST methods on SHCClient."""
        from shc_toolkit.client import SHCClient
        v243_methods = [
            "list_vm_addons", "get_vm_addon_options", "create_vm_addon",
            "preview_vm_addon", "get_vm_term_options", "change_vm_term",
            "preview_vm_term_change", "list_orders", "get_order",
            "cancel_pending_order",
        ]
        missing = [m for m in v243_methods if not hasattr(SHCClient, m)]
        assert not missing, f"SHCClient missing v2.4.3 methods: {missing}"


class TestMcpClientMocked:
    """Test SHCMCPClient with mocked HTTP layer."""

    def _make_client(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            client = SHCMCPClient()
        client._initialized = True
        return client

    def test_list_vms_returns_list_from_structured_content(self):
        client = self._make_client()
        vm_data = {"items": [{"id": 123, "hostname": "test-vm"}]}
        client.session.post = MagicMock(return_value=_jsonrpc_result(vm_data))
        vms = client.list_vms()
        assert isinstance(vms, list)
        assert vms[0]["hostname"] == "test-vm"

    def test_get_account_returns_dict(self):
        client = self._make_client()
        account = {"email": "test@example.com", "id": 1}
        client.session.post = MagicMock(return_value=_jsonrpc_result(account))
        result = client.get_account()
        assert result["email"] == "test@example.com"

    def test_get_catalog_returns_list(self):
        client = self._make_client()
        result = client.get_catalog()
        assert isinstance(result, list)
        assert len(result) == 20
        assert result[0]["package_id"] == 23  # nvme Starter

    def test_get_catalog_live_calls_mcp(self):
        client = self._make_client()
        catalog = {"items": [{"package_id": 81, "name": "Dev VPS"}]}
        client.session.post = MagicMock(return_value=_jsonrpc_result(catalog))
        result = client.get_catalog_live()
        assert isinstance(result, list)
        assert result[0]["package_id"] == 81

    def test_tool_call_raises_on_error(self):
        client = self._make_client()
        client.session.post = MagicMock(return_value=_jsonrpc_error(
            "unauthorized", "Authentication failed",
            structured={"http_status": 401, "error": {"code": "unauthorized", "message": "Authentication failed"}},
        ))
        with pytest.raises(SHCError, match="Authentication failed"):
            client.get_account()

    def test_confirmation_flow_auto_resubmits(self):
        client = self._make_client()
        confirmation_sc = {
            "http_status": 409,
            "error": {
                "code": "confirmation_required",
                "message": "Confirmation required for this action",
            },
            "confirmation": {"confirmation_id": "conf-123"},
        }
        error_resp = _jsonrpc_error(
            "confirmation_required", "Confirmation required for this action",
            structured=confirmation_sc,
        )
        success_resp = _jsonrpc_result({"id": 123, "hostname": "test", "service_status": "canceled"})
        client.session.post = MagicMock(side_effect=[error_resp, success_resp])
        result = client.call_tool("cancelVirtualMachine", {"serviceId": 123})
        assert client.session.post.call_count == 2

    def test_sse_response_parsed(self):
        client = self._make_client()
        sse_data = {"items": [{"id": 1}]}
        sse_text = f'event: message\ndata: {json.dumps({"jsonrpc":"2.0","id":1,"result":{"isError":False,"structuredContent":{"data":sse_data}}})}\n\n'
        client.session.post = MagicMock(return_value=_mock_response(
            content_type="text/event-stream", text=sse_text,
        ))
        result = client.list_vms()
        assert isinstance(result, list)


# ── CLI Argument Parsing ───────────────────────────────────


class TestCliParsers:
    def test_reset_command_exists(self):
        import shc_toolkit.cli as cli
        import inspect
        assert "cmd_reset" in inspect.getsource(cli)

    def test_new_commands_exist(self):
        import shc_toolkit.cli as cli
        import inspect
        src = inspect.getsource(cli)
        for cmd in [
            "cmd_upgrade", "cmd_jobs", "cmd_ssh_keys",
            "cmd_iso", "cmd_rdns", "cmd_console", "cmd_templates",
        ]:
            assert cmd in src, f"Missing {cmd}"

    def test_cli_imports_clean(self):
        from shc_toolkit.cli import main
        assert callable(main)


class TestComputeWiring:
    def test_compute_uses_create_client(self):
        import inspect
        from shc_toolkit import compute
        src = inspect.getsource(compute)
        assert "_create_client" in src or "create_client" in src


class TestCatalogModel:
    def test_get_catalog_returns_20_packages(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            catalog = c.get_catalog()
            assert len(catalog) == 20

    def test_get_catalog_no_network(self):
        """get_catalog() must not make any network calls."""
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._get = MagicMock(side_effect=AssertionError("get_catalog must not call _get"))
            catalog = c.get_catalog()
            assert len(catalog) == 20

    def test_get_catalog_has_all_four_lines(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            lines = {p["line"] for p in c.get_catalog()}
            assert lines == {"nvme", "ssd", "hdd", "dev"}

    def test_get_catalog_daily_price_matches_formula(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            for pkg in c.get_catalog():
                daily = next(p for p in pkg["pricing"] if p["period"] == "day")
                expected = 0.22 * pkg["cpu"] + 0.02
                if pkg["line"] == "nvme":
                    expected += 0.002 * pkg["disk_gb"]
                assert abs(float(daily["price"]) - expected) < 0.02

    def test_invalidate_cache_is_noop(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c.invalidate_cache()
            c.invalidate_cache("credit")


class TestCreditCheck:
    def test_insufficient_credit_error_message(self):
        from shc_toolkit.client import InsufficientCreditError
        err = InsufficientCreditError(required=0.50, available=0.12)
        assert err.required == 0.50
        assert err.available == 0.12
        assert "0.50" in str(err)
        assert "0.12" in str(err)

    def test_check_credit_raises_when_low(self):
        from shc_toolkit.client import SHCClient, InsufficientCreditError
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c.get_available_credit = MagicMock(return_value=0.10)
            with pytest.raises(InsufficientCreditError):
                c.check_credit(0.50)

    def test_check_credit_passes_when_sufficient(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c.get_available_credit = MagicMock(return_value=5.00)
            c.check_credit(0.50)


# ── Sizes (spec-encoding names) ─────────────────────────────


class TestSizes:
    def test_size_map_has_20_entries(self):
        from shc_toolkit.sizes import SIZE_MAP
        assert len(SIZE_MAP) == 20

    def test_size_map_covers_all_four_lines(self):
        from shc_toolkit.sizes import SIZE_MAP
        lines = {e["line"] for e in SIZE_MAP.values()}
        assert lines == {"nvme", "ssd", "hdd", "dev"}

    def test_resolve_size_nvme(self):
        from shc_toolkit.sizes import resolve_size
        assert resolve_size("nvme-2c-8gb") == (26, 56)

    def test_resolve_size_hdd(self):
        from shc_toolkit.sizes import resolve_size
        assert resolve_size("hdd-1c-4gb") == (36, 67)

    def test_resolve_size_dev(self):
        from shc_toolkit.sizes import resolve_size
        assert resolve_size("dev-4c-16gb") == (82, 249)

    def test_resolve_size_case_insensitive(self):
        from shc_toolkit.sizes import resolve_size
        assert resolve_size("NVME-2C-8GB") == (26, 56)

    def test_resolve_size_rejects_legacy_alias(self):
        from shc_toolkit.sizes import resolve_size
        with pytest.raises(ValueError, match="Unknown size"):
            resolve_size("standard")

    def test_resolve_size_rejects_unknown(self):
        from shc_toolkit.sizes import resolve_size
        with pytest.raises(ValueError, match="Unknown size"):
            resolve_size("nvme-99c-999gb")

    def test_resolve_specs_finds_cheapest_across_all_lines(self):
        from shc_toolkit.sizes import resolve_specs
        pkg, _ = resolve_specs(cpu=4, ram_mb=16384)
        assert pkg in (38, 58)  # HDD/SSD Pro tie at $0.90/day

    def test_resolve_specs_line_filter_nvme(self):
        from shc_toolkit.sizes import resolve_specs
        pkg, _ = resolve_specs(cpu=4, ram_mb=16384, line="nvme")
        assert pkg == 29  # NVMe Pro

    def test_resolve_specs_line_filter(self):
        from shc_toolkit.sizes import resolve_specs
        pkg, _ = resolve_specs(cpu=2, line="ssd")
        assert pkg == 57  # SSD Standard

    def test_resolve_specs_no_match(self):
        from shc_toolkit.sizes import resolve_specs
        with pytest.raises(ValueError, match="No plan matches"):
            resolve_specs(cpu=999)

    def test_spec_name(self):
        from shc_toolkit.sizes import spec_name
        assert spec_name("nvme", 2, 8192) == "nvme-2c-8gb"
        assert spec_name("hdd", 16, 65536) == "hdd-16c-64gb"

    def test_list_sizes_all(self):
        from shc_toolkit.sizes import list_sizes
        all_sizes = list_sizes()
        assert len(all_sizes) == 20

    def test_list_sizes_filter_line(self):
        from shc_toolkit.sizes import list_sizes
        hdd = list_sizes("hdd")
        assert len(hdd) == 5
        assert all(s["line"] == "hdd" for s in hdd)


# ── Config Options (resolve_addons + order_vm) ──────────────


class TestConfigOptions:
    def test_get_config_options_returns_option_ids(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            opts = c.get_config_options(26)
            assert opts["ram"]["option_id"] == 110
            assert opts["cpu"]["option_id"] == 111
            assert opts["disk"]["option_id"] == 112
            assert "16384" in opts["ram"]["values"]

    def test_get_config_options_empty_for_unknown_package(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            assert c.get_config_options(999) == {}

    def test_resolve_addons_translates_specs(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            result = c.resolve_addons(26, ram_mb=16384, cpu=4, disk_gb=50)
            assert result == {"110": "16384", "111": "4", "112": "50"}

    def test_resolve_addons_rejects_invalid_value(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            with pytest.raises(ValueError, match="not available"):
                c.resolve_addons(26, ram_mb=999999)

    def test_resolve_addons_rejects_unknown_package(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            with pytest.raises(ValueError, match="not found in catalog"):
                c.resolve_addons(99999, ram_mb=16384)

    def test_resolve_addons_partial(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            result = c.resolve_addons(26, disk_gb=50)
            assert result == {"112": "50"}

    def test_resolve_addons_template(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            result = c.resolve_addons(26, template="debian12-cloud")
            assert result == {"126": "debian12-cloud"}

    def test_order_vm_requires_size_or_package_id(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            with pytest.raises(ValueError, match="size.*package_id"):
                c.order_vm(hostname="test")

    def test_order_vm_translates_size_to_ids(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c.submit_order = MagicMock(return_value={"invoice_id": 42})
            c.pay_invoice = MagicMock()
            c._safe_credit = MagicMock(return_value=100.0)
            c.order_vm(hostname="my-vm", size="nvme-2c-8gb", disk_gb=50)
            args, kwargs = c.submit_order.call_args
            assert kwargs["package_id"] == 26
            assert kwargs["pricing_id"] == 56
            assert kwargs["config_options"] == {"112": "50"}
            assert kwargs["hostname"] == "my-vm"

    def test_order_vm_passes_raw_config_options(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c.submit_order = MagicMock(return_value={"invoice_id": 42})
            c.pay_invoice = MagicMock()
            c._safe_credit = MagicMock(return_value=100.0)
            c.order_vm(
                hostname="raw",
                package_id=26, pricing_id=56,
                config_options={"999": "custom"},
            )
            _, kwargs = c.submit_order.call_args
            assert kwargs["config_options"] == {"999": "custom"}


# ── Cost Audit (balance-diff based) ─────────────────────────


class TestCostAudit:
    def _client_with_catalog(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            return SHCClient()

    def test_track_order_records_session(self):
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        assert session.service_id == 123
        assert session.package_id == 26
        assert session.daily_price == 0.49
        assert session.actual_charge == 0.49
        assert 123 in c.cost_tracker._sessions

    def test_track_order_verifies_matching_charge(self):
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        assert session.charge_verified is True

    def test_track_order_warns_on_charge_mismatch(self):
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.99)
        assert session.charge_verified is False
        assert session.actual_charge == 0.99

    def test_track_order_without_charge_data(self):
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=None)
        assert session.charge_verified is False
        assert session.actual_charge is None

    def test_current_burn_computes_prorated_cost(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=3)
        burn = c.cost_tracker.current_burn(123)
        assert burn == 0.06

    def test_current_burn_enforces_min_charge(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(minutes=5)
        burn = c.cost_tracker.current_burn(123)
        assert burn == 0.02

    def test_audit_cancel_computes_expected_refund(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=6)
        report = c.cost_tracker.audit_cancel(123, actual_refund=None)
        assert report is not None
        assert report.duration_hours == 6.0
        assert report.expected_cost == 0.12
        assert report.expected_refund == 0.37
        assert report.actual_charge == 0.49

    def test_audit_cancel_matches_actual_refund(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=6)
        report = c.cost_tracker.audit_cancel(123, actual_refund=0.37)
        assert report.actual_refund == 0.37
        assert report.mismatch is False

    def test_audit_cancel_flags_refund_mismatch(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=6)
        c.get_vm_payments = MagicMock(return_value=[{"total": "0.49"}])
        report = c.cost_tracker.audit_cancel(123, actual_refund=0.01)
        assert report.mismatch is True
        assert report.actual_refund == 0.01

    def test_audit_cancel_disambiguates_concurrent_activity(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=6)
        c.get_vm_payments = MagicMock(return_value=[
            {"total": "0.49"},
            {"total": "-0.37"},
        ])
        report = c.cost_tracker.audit_cancel(123, actual_refund=0.01)
        assert report.mismatch is False
        assert report.ledger_refund == 0.37
        assert "balance_diff_noisy_concurrent_activity" in report.notes

    def test_audit_cancel_ledger_confirms_real_mismatch(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=6)
        c.get_vm_payments = MagicMock(return_value=[
            {"total": "0.49"},
            {"total": "-0.01"},
        ])
        report = c.cost_tracker.audit_cancel(123, actual_refund=0.01)
        assert report.mismatch is True
        assert "ledger_confirms_mismatch" in report.notes

    def test_audit_cancel_ledger_unavailable_keeps_warning(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=6)
        c.get_vm_payments = MagicMock(side_effect=Exception("API down"))
        report = c.cost_tracker.audit_cancel(123, actual_refund=0.01)
        assert report.mismatch is True
        assert any("refund_diff" in n for n in report.notes)

    def test_audit_cancel_returns_none_for_untracked(self):
        c = self._client_with_catalog()
        assert c.cost_tracker.audit_cancel(999) is None

    def test_session_report_for_running_vm(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=2)
        report = c.cost_tracker.session_report(123)
        assert report["service_id"] == 123
        assert report["daily_price"] == 0.49
        assert report["elapsed_hours"] == 2.0
        assert report["actual_charge"] == 0.49

    def test_order_vm_captures_balance_diff(self):
        c = self._client_with_catalog()
        c.check_credit = MagicMock()
        c._safe_credit = MagicMock(side_effect=[100.0, 100.0, 99.51, 99.51])
        c._confirmed_request = MagicMock(return_value={
            "invoice_id": 42, "service_id": 777,
        })
        c.pay_invoice = MagicMock()
        c.order_vm(hostname="test", size="nvme-2c-8gb")
        session = c.cost_tracker._sessions.get(777)
        assert session is not None
        assert session.daily_price == 0.49

    def test_cancel_vm_captures_refund_diff(self):
        from datetime import timedelta
        c = self._client_with_catalog()
        session = c.cost_tracker.track_order(777, 26, actual_charge=0.49)
        session.ordered_at = datetime.now(timezone.utc) - timedelta(hours=1)
        c._confirmed_request = MagicMock(return_value={})
        # cost_tracker._ledger_refund() calls get_vm_payments() to disambiguate
        # this VM's refund from concurrent activity. Without this mock the test
        # makes a real HTTP call to /vm/777/payments, gets 401, retries, and
        # eventually triggers SHC's rate-limiter (429) — flaking the whole
        # suite once enough 401s accumulate.
        c.get_vm_payments = MagicMock(return_value=[])
        credit_values = iter([99.51, 99.90])
        c._safe_credit = MagicMock(side_effect=lambda: next(credit_values))
        c.cancel_vm(777, immediate=True, confirm=False)
        report = c.cost_tracker.session_report(777)
        assert report is not None

    def test_no_absolute_balance_logged(self):
        import io, logging as pylog
        buf = io.StringIO()
        handler = pylog.StreamHandler(buf)
        handler.setLevel(pylog.DEBUG)
        logger = pylog.getLogger("shc.cost")
        logger.addHandler(handler)
        logger.setLevel(pylog.DEBUG)
        c = self._client_with_catalog()
        c.cost_tracker.track_order(123, 26, actual_charge=0.49)
        output = buf.getvalue()
        logger.removeHandler(handler)
        assert "0.49" in output
        assert "100.0" not in output or "99.51" not in output


# ── MCP Argument Format Tests ──────────────────────────────


class TestMcpArgumentFormat:
    """Verify MCP client sends correct argument structure for destructive ops."""

    def _mock_mcp_client(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCMCPClient()
        c._ensure_initialized = MagicMock()
        c._send_jsonrpc = MagicMock(return_value={"result": {}})
        return c

    def test_delete_snapshot_uses_body_wrapper(self):
        c = self._mock_mcp_client()
        c.delete_snapshot(123, "snap-456")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "deleteVirtualMachineSnapshot"
        args = params["arguments"]
        assert "body" in args
        assert args["body"]["snapshot_id"] == "snap-456"

    def test_restore_snapshot_uses_body_wrapper(self):
        c = self._mock_mcp_client()
        c.restore_snapshot(123, "snap-456")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "restoreVirtualMachineSnapshot"
        args = params["arguments"]
        assert "body" in args
        assert args["body"]["snapshot_id"] == "snap-456"

    def test_delete_backup_uses_body_wrapper(self):
        c = self._mock_mcp_client()
        c.delete_backup(123, "bak-456")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "deleteVirtualMachineBackup"
        args = params["arguments"]
        assert "body" in args
        assert args["body"]["backup_id"] == "bak-456"

    def test_create_firewall_rule_uses_snake_case_body(self):
        c = self._mock_mcp_client()
        c.create_firewall_rule(123, action="ACCEPT", dest_port="443", protocol="tcp")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "addVirtualMachineFirewallRule"
        args = params["arguments"]
        assert "body" in args
        assert args["body"]["dest_port"] == "443"
        assert "destPort" not in args["body"]

    def test_delete_firewall_rule_uses_body_wrapper(self):
        c = self._mock_mcp_client()
        c.delete_firewall_rule(123, 5)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "deleteVirtualMachineFirewallRule"
        args = params["arguments"]
        assert "body" in args
        assert args["body"]["position"] == 5

    def test_edit_firewall_rule_uses_correct_tool_and_body(self):
        c = self._mock_mcp_client()
        c.edit_firewall_rule(123, 3, action="DROP", dest_port="22")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "updateVirtualMachineFirewallRule"
        args = params["arguments"]
        assert "body" in args
        assert args["body"]["position"] == 3
        assert args["body"]["action"] == "DROP"
        assert args["body"]["dest_port"] == "22"

    def test_list_ssh_keys_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c._send_jsonrpc.return_value = {"result": {"structuredContent": {"result": {"items": []}}}}
        c.list_ssh_keys(123)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "listServiceSshKeys"

    def test_add_ssh_key_uses_correct_tool_and_body(self):
        c = self._mock_mcp_client()
        c.add_ssh_key(123, "ssh-rsa AAA...", label="test")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "setServiceSshKey"
        args = params["arguments"]
        assert "body" in args

    def test_get_vm_credentials_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c._send_jsonrpc.return_value = {"result": {"structuredContent": {"result": {}}}}
        c.get_vm_credentials(123)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "getVirtualMachineCredentials"

    def test_get_vm_payments_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c._send_jsonrpc.return_value = {"result": {"structuredContent": {"result": {"items": []}}}}
        c.get_vm_payments(123)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "listVirtualMachinePayments"

    def test_unwrap_prefers_structuredContent_result(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {"structuredContent": {"result": {"key": "value"}}}}
        unwrapped = SHCMCPClient._unwrap_tool_result(resp)
        assert unwrapped == {"key": "value"}

    def test_unwrap_falls_back_to_data(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {"structuredContent": {"data": {"key": "value"}}}}
        unwrapped = SHCMCPClient._unwrap_tool_result(resp)
        assert unwrapped == {"key": "value"}

    def test_unwrap_double_nested_data(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        resp = {"result": {"structuredContent": {"data": {"data": {"key": "value"}}}}}
        unwrapped = SHCMCPClient._unwrap_tool_result(resp)
        assert unwrapped == {"key": "value"}

    def test_verify_backup_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c.verify_backup(123, "bak-456")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "verifyVirtualMachineBackup"
        assert params["arguments"]["body"]["backup_id"] == "bak-456"

    def test_verify_snapshot_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c.verify_snapshot(123, "snap-456")
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "verifyVirtualMachineSnapshot"
        assert params["arguments"]["body"]["snapshot_id"] == "snap-456"

    def test_set_backup_protection_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c.set_backup_protection(123, "bak-456", True)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "setVirtualMachineBackupProtection"
        body = params["arguments"]["body"]
        assert body["backup_id"] == "bak-456"
        assert body["protected"] is True

    def test_set_snapshot_protection_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c.set_snapshot_protection(123, "snap-456", False)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "setVirtualMachineSnapshotProtection"
        body = params["arguments"]["body"]
        assert body["snapshot_id"] == "snap-456"
        assert body["protected"] is False

    def test_get_backup_restore_hints_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c._send_jsonrpc.return_value = {"result": {"structuredContent": {"result": {}}}}
        c.get_backup_restore_hints(123)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "getVirtualMachineBackupRestoreHints"

    def test_get_snapshot_restore_hints_calls_correct_tool(self):
        c = self._mock_mcp_client()
        c._send_jsonrpc.return_value = {"result": {"structuredContent": {"result": {}}}}
        c.get_snapshot_restore_hints(123)
        call_args = c._send_jsonrpc.call_args
        params = call_args.kwargs.get("params") or call_args[0][1]
        assert params["name"] == "getVirtualMachineSnapshotRestoreHints"


# ── Backoff / Retry Logic ───────────────────────────────────


class TestBackoffRetry:
    def _client(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            return SHCClient()

    def test_backoff_scales_exponentially(self):
        c = self._client()
        d0 = c._backoff_delay(0)
        d1 = c._backoff_delay(1)
        d2 = c._backoff_delay(2)
        assert 0.5 <= d0 <= 1.5
        assert d1 > d0
        assert d2 > d1

    def test_backoff_respects_cap(self):
        c = self._client()
        for i in range(30):
            d = c._backoff_delay(i)
            assert d <= 60.0, f"attempt {i}: {d} > 60 cap"

    def test_backoff_never_negative(self):
        c = self._client()
        for i in range(30):
            d = c._backoff_delay(i)
            assert d >= 0

    def test_custom_backoff_config(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient(max_retries=5, backoff_base=0.5, backoff_cap=10.0)
        for i in range(10):
            d = c._backoff_delay(i)
            assert d <= 10.0, f"attempt {i}: {d} > 10 custom cap"

    def test_parse_retry_after_header(self):
        c = self._client()
        mock_resp = MagicMock()
        mock_resp.headers = {"Retry-After": "15"}
        mock_resp.text = "{}"
        result = c._parse_retry_after(mock_resp, 0)
        assert result == 15.0

    def test_parse_retry_after_json_field(self):
        c = self._client()
        mock_resp = MagicMock()
        mock_resp.headers = {}
        mock_resp.text = '{"error":{"retry_after_seconds":30}}'
        result = c._parse_retry_after(mock_resp, 0)
        assert result == 30.0

    def test_parse_retry_after_falls_back_to_backoff(self):
        c = self._client()
        mock_resp = MagicMock()
        mock_resp.headers = {}
        mock_resp.text = '{}'
        result = c._parse_retry_after(mock_resp, 0)
        assert 0 < result <= 60.0

    def test_408_is_retried(self):
        """408 Request Timeout must be retried (2026 resilience reference)."""
        c = self._client()
        mock_408 = MagicMock()
        mock_408.status_code = 408
        mock_408.headers = {}
        mock_408.text = '{}'
        mock_408.ok = False
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.headers = {}
        mock_200.text = '{"data": {"ok": true}}'
        mock_200.ok = True
        c.session.request = MagicMock(side_effect=[mock_408, mock_200])
        result = c._get("/test")
        assert result == {"ok": True}
        assert c.session.request.call_count == 2

    def test_idempotency_key_on_writes(self):
        """Confirmed requests must send an Idempotency-Key header that
        persists across the original + confirmation re-send."""
        c = self._client()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {}
        mock_resp.text = '{"data": {"ok": true}}'
        mock_resp.ok = True
        captured_headers = []
        def capture_request(*args, **kwargs):
            captured_headers.append(dict(kwargs.get("headers", {})))
            return mock_resp
        c.session.request = MagicMock(side_effect=capture_request)
        c._confirmed_request("POST", "/test", json={"key": "value"})
        assert len(captured_headers) == 1
        assert "Idempotency-Key" in captured_headers[0]
        assert captured_headers[0]["Idempotency-Key"].startswith("shc-")

    def test_idempotency_key_persists_across_confirmation(self):
        """When _confirmed_request retries with X-User-Api-Confirm,
        the Idempotency-Key must be the SAME as the original request."""
        c = self._client()
        mock_409 = MagicMock()
        mock_409.status_code = 409
        mock_409.headers = {}
        mock_409.text = '{"error":{"code":"confirmation_required"}, "confirmation":{"structuredContent":{"confirmation_id":"test-cid-123"}}}'
        mock_409.ok = False
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.headers = {}
        mock_200.text = '{"data": {"ok": true}}'
        mock_200.ok = True
        captured_headers = []
        def capture_request(*args, **kwargs):
            captured_headers.append(dict(kwargs.get("headers", {})))
            if len(captured_headers) == 1:
                return mock_409
            return mock_200
        c.session.request = MagicMock(side_effect=capture_request)
        c._confirmed_request("POST", "/test", json={"key": "value"})
        assert len(captured_headers) == 2
        key1 = captured_headers[0].get("Idempotency-Key")
        key2 = captured_headers[1].get("Idempotency-Key")
        assert key1 is not None, "First request missing Idempotency-Key"
        assert key2 is not None, "Confirmation request missing Idempotency-Key"
        assert key1 == key2, f"Keys differ: {key1} vs {key2}"
        assert captured_headers[1].get("X-User-Api-Confirm") == "test-cid-123"

    def test_no_idempotency_key_on_reads(self):
        """GET requests must not carry an Idempotency-Key header."""
        c = self._client()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {}
        mock_resp.text = '{"data": {"ok": true}}'
        mock_resp.ok = True
        captured_headers = []
        def capture_request(*args, **kwargs):
            captured_headers.append(dict(kwargs.get("headers", {})))
            return mock_resp
        c.session.request = MagicMock(side_effect=capture_request)
        c._get("/test")
        assert len(captured_headers) == 1
        assert "Idempotency-Key" not in captured_headers[0]


class TestExceptionHierarchy:
    """Tests for the SHCError exception hierarchy."""

    def test_not_found_error(self):
        from shc_toolkit.client import SHCNotFoundError, SHCError
        exc = SHCNotFoundError("not_found", "VM not found")
        assert isinstance(exc, SHCError)
        assert exc.error_code is None
        assert "not_found" in str(exc)

    def test_auth_error(self):
        from shc_toolkit.client import SHCAuthError, SHCError
        exc = SHCAuthError("unauthorized", "Invalid token")
        assert isinstance(exc, SHCError)

    def test_rate_limit_error(self):
        from shc_toolkit.client import SHCRateLimitError, SHCError
        exc = SHCRateLimitError("rate_limited", "Too many requests",
                                retry_after_seconds=30)
        assert isinstance(exc, SHCError)
        assert exc.retry_after_seconds == 30

    def test_confirmation_required_error(self):
        from shc_toolkit.client import SHCConfirmationRequiredError, SHCError
        exc = SHCConfirmationRequiredError("confirmation_required", "Confirm needed")
        assert isinstance(exc, SHCError)

    def test_server_error(self):
        from shc_toolkit.client import SHCServerError, SHCError
        exc = SHCServerError("upstream_failure", "Internal error")
        assert isinstance(exc, SHCError)

    def test_catch_specific_vs_base(self):
        """Users can catch specific errors OR the base SHCError."""
        from shc_toolkit.client import SHCNotFoundError, SHCError
        exc = SHCNotFoundError("not_found", "Not found")
        # Catching base works
        try:
            raise exc
        except SHCError:
            pass
        # Catching specific works
        try:
            raise exc
        except SHCNotFoundError:
            pass

    def test_generic_fallback(self):
        """Unknown error codes still produce a plain SHCError."""
        from shc_toolkit.client import SHCError, _ERROR_CODE_MAP
        cls = _ERROR_CODE_MAP.get("unknown_error_code", SHCError)
        assert cls is SHCError

class TestOrderTagging:
    """SSH-key comment tagging for VM-order attribution."""

    KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM/CoI0Wtest macbook@old-host"

    def test_tag_appended_to_existing_comment(self):
        out = SHCClient.augment_key_comment(self.KEY, "opencode:ses_123")
        assert out.startswith("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM/CoI0Wtest ")
        assert out.endswith("macbook@old-host #shc-order=opencode:ses_123")

    def test_tag_added_to_bare_key(self):
        bare = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM/CoI0Wtest"
        out = SHCClient.augment_key_comment(bare, "ci")
        assert out == f"{bare} #shc-order=ci"

    def test_retag_replaces_previous_tag(self):
        once = SHCClient.augment_key_comment(self.KEY, "first")
        twice = SHCClient.augment_key_comment(once, "second")
        assert "#shc-order=first" not in twice
        assert twice.endswith("macbook@old-host #shc-order=second")

    def test_garbage_returned_unchanged(self):
        assert SHCClient.augment_key_comment("not a key", "t") == "not a key"

    def test_default_tag_prefers_env(self):
        from unittest.mock import patch
        with patch.dict(os.environ, {"SHC_ORDER_TAG": "opencode:ses_abc"}):
            assert SHCClient.default_order_tag() == "opencode:ses_abc"

    def test_order_vm_raw_string_key_is_sent_and_tagged(self):
        """Regression: raw string ssh_key was silently dropped (only file
        paths were honored), ordering VMs keyless without warning."""
        from unittest.mock import patch
        client = SHCClient(api_key="test-key")
        raw_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM/CoI0Wtest macbook@mbp"
        with patch.object(SHCClient, "submit_order", return_value={"service_id": 1}) as so, \
             patch.object(SHCClient, "_safe_credit", return_value=10.0):
            client.order_vm(hostname="t", package_id=80, pricing_id=241,
                            ssh_key=raw_key, pay=False)
        sent = so.call_args.kwargs.get("ssh_key", "")
        assert sent.startswith("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM/CoI0Wtest")
        assert "#shc-order=" in sent


class TestReapOrphans:
    """Unit tests for reap_orphans method."""

    def test_reap_dry_run_returns_list(self):
        """reap_orphans with dry_run returns a list."""
        from unittest.mock import MagicMock, patch
        from shc_toolkit.client import SHCClient

        with patch.object(SHCClient, 'list_vms', return_value=[]):
            client = SHCClient(api_key="test-key")
            orphans = client.reap_orphans(dry_run=True)
            assert isinstance(orphans, list)
            assert len(orphans) == 0

    def test_reap_excludes_production(self):
        """reap_orphans never destroys production VMs."""
        from unittest.mock import MagicMock, patch
        from shc_toolkit.client import SHCClient

        fake_vms = [
            {"id": 1, "hostname": "europa-vpn-vps", "service_status": "active",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "prod"},
        ]
        with patch.object(SHCClient, 'list_vms', return_value=fake_vms):
            client = SHCClient(api_key="test-key")
            orphans = client.reap_orphans(max_age_hours=0.0, dry_run=True)
            assert len(orphans) == 0  # europa-vpn-vps excluded

    def test_reap_matches_test_prefixes(self):
        """reap_orphans matches VMs with test prefixes."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        fake_vms = [
            {"id": 1, "hostname": "tf-acc-basic", "service_status": "active",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "dev"},
            {"id": 2, "hostname": "tollgate-test-vm", "service_status": "active",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "dev"},
            {"id": 4, "hostname": "devprobe-6f9cea97", "service_status": "active",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "dev"},
            {"id": 3, "hostname": "production-server", "service_status": "active",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "prod"},
        ]
        with patch.object(SHCClient, 'list_vms', return_value=fake_vms):
            client = SHCClient(api_key="test-key")
            orphans = client.reap_orphans(max_age_hours=0.0, dry_run=True)
            hostnames = [o["hostname"] for o in orphans]
            assert "tf-acc-basic" in hostnames
            assert "tollgate-test-vm" in hostnames
            assert "devprobe-6f9cea97" in hostnames
            assert "production-server" not in hostnames

    def test_reap_respects_age_threshold(self):
        """reap_orphans respects max_age_hours."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        recent = (now - timedelta(minutes=30)).isoformat()
        old = (now - timedelta(hours=5)).isoformat()

        fake_vms = [
            {"id": 1, "hostname": "tf-acc-recent", "service_status": "active",
             "date_created": recent, "package": "dev"},
            {"id": 2, "hostname": "tf-acc-old", "service_status": "active",
             "date_created": old, "package": "dev"},
        ]
        with patch.object(SHCClient, 'list_vms', return_value=fake_vms):
            client = SHCClient(api_key="test-key")
            orphans = client.reap_orphans(max_age_hours=2.0, dry_run=True)
            hostnames = [o["hostname"] for o in orphans]
            assert "tf-acc-old" in hostnames
            assert "tf-acc-recent" not in hostnames

    def test_reap_skips_canceled_vms(self):
        """reap_orphans skips already-canceled VMs."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        fake_vms = [
            {"id": 1, "hostname": "tf-acc-dead", "service_status": "canceled",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "dev"},
        ]
        with patch.object(SHCClient, 'list_vms', return_value=fake_vms):
            client = SHCClient(api_key="test-key")
            orphans = client.reap_orphans(max_age_hours=0.0, dry_run=True)
            assert len(orphans) == 0

    def test_reap_custom_exclusions(self):
        """reap_orphans respects custom exclude_hostnames."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        fake_vms = [
            {"id": 1, "hostname": "tf-acc-keep", "service_status": "active",
             "date_created": "2020-01-01T00:00:00+00:00", "package": "dev"},
        ]
        with patch.object(SHCClient, 'list_vms', return_value=fake_vms):
            client = SHCClient(api_key="test-key")
            orphans = client.reap_orphans(
                max_age_hours=0.0,
                dry_run=True,
                exclude_hostnames=["tf-acc-keep"],
            )
            assert len(orphans) == 0


class TestCloudInitRestWrappers:
    """Unit tests for the SHCClient cloud-init REST wrappers.

    SHC shipped customer cloud-init in v2.4.7 (validate / update / delete).
    The MCP transport already wraps all three (TOOL_MAP entries); these
    tests pin the REST surface that ships in v2.4.24.0 to close the parity
    gap surfaced during the ticket-#2211883 audit.
    """

    def test_validate_vm_cloud_init_posts_to_correct_path(self):
        """validate_vm_cloud_init POSTs to /virtual-machines/{id}/cloud-init/validate
        with the {cloudInit: ...} body shape. Read-only, no confirmation."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        with patch.object(client, "_post", return_value={"accepted": True}) as mock:
            result = client.validate_vm_cloud_init(1077, cloud_init="#cloud-config\npackages: [nginx]\n")
            assert result == {"accepted": True}
            mock.assert_called_once()
            args, kwargs = mock.call_args
            assert args[0] == "/virtual-machines/1077/cloud-init/validate"
            assert args[1] == {"cloudInit": "#cloud-config\npackages: [nginx]\n"}

    def test_update_vm_cloud_init_uses_confirmation_flow(self):
        """update_vm_cloud_init is confirm-gated via _confirmed_request (PATCH)."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            result = client.update_vm_cloud_init(1077, cloud_init="#cloud-config\nruncmd: []\n")
            assert result == {"ok": True}
            mock.assert_called_once()
            args, kwargs = mock.call_args
            assert args[0] == "PATCH"
            assert args[1] == "/virtual-machines/1077/cloud-init"
            assert kwargs["json"] == {"cloudInit": "#cloud-config\nruncmd: []\n"}
            assert kwargs["confirm"] is True

    def test_update_vm_cloud_init_probe_mode(self):
        """update_vm_cloud_init(confirm=False) probes — raises on 409 instead of auto-confirming."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            client.update_vm_cloud_init(1077, cloud_init="#cloud-config\n", confirm=False)
            kwargs = mock.call_args.kwargs
            assert kwargs["confirm"] is False

    def test_delete_vm_cloud_init_uses_confirmation_flow(self):
        """delete_vm_cloud_init is confirm-gated via _confirmed_request (DELETE)."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            result = client.delete_vm_cloud_init(1077)
            assert result == {"ok": True}
            mock.assert_called_once()
            args, kwargs = mock.call_args
            assert args[0] == "DELETE"
            assert args[1] == "/virtual-machines/1077/cloud-init"
            assert kwargs["confirm"] is True


class TestCloseSupportTicketConfirmationFlow:
    """Regression coverage: close_support_ticket must use the confirmation flow.

    The v2.4.24 spec documented that closeSupportTicket returns 409
    confirmation_required (it always did server-side; the spec just caught up).
    The wrapper previously called _post directly and surfaced the 409 as
    SHCConfirmationRequiredError instead of completing the confirmation
    re-send automatically. This test pins the fix.
    """

    def test_close_support_ticket_uses_confirmation_flow(self):
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            client.close_support_ticket(221)
            mock.assert_called_once()
            args, kwargs = mock.call_args
            assert args[0] == "POST"
            assert args[1] == "/support/tickets/221/close"
            assert kwargs["confirm"] is True

    def test_close_support_ticket_probe_mode(self):
        """confirm=False surfaces the 409 instead of auto-confirming."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            client.close_support_ticket(221, confirm=False)
            kwargs = mock.call_args.kwargs
            assert kwargs["confirm"] is False


class TestIssue22ConfirmationFlowWiring:
    """Regression coverage for issue #22: 11 ops that newly declare 409 in
    v2.4.24 (and have always required confirmation server-side) must route
    through _confirmed_request, not _post / _patch / _delete / _get / _put.
    Each test pins one method's HTTP verb, path, and confirm default.
    """

    def _mock_and_call(self, method_name, *args, **kwargs):
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient
        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            getattr(client, method_name)(*args, **kwargs)
            return mock

    def test_update_preferences_uses_confirmed_request(self):
        mock = self._mock_and_call("update_preferences", theme="dark")
        assert mock.call_args.args[0] == "PATCH"
        assert mock.call_args.args[1] == "/account/preferences"
        assert mock.call_args.kwargs["json"] == {"theme": "dark"}
        assert mock.call_args.kwargs["confirm"] is True

    def test_set_credit_handling_uses_confirmed_request(self):
        mock = self._mock_and_call("set_credit_handling", auto_top_up=True)
        assert mock.call_args.args[0] == "PUT"
        assert mock.call_args.args[1] == "/account/credit-handling"
        assert mock.call_args.kwargs["json"] == {"auto_top_up": True}
        assert mock.call_args.kwargs["confirm"] is True

    def test_revoke_api_key_uses_confirmed_request(self):
        mock = self._mock_and_call("revoke_api_key", "shc_live_abc")
        assert mock.call_args.args[0] == "DELETE"
        assert mock.call_args.args[1] == "/account/api-keys/shc_live_abc"
        assert mock.call_args.kwargs["confirm"] is True

    def test_create_contact_uses_confirmed_request(self):
        mock = self._mock_and_call("create_contact", email="x@y.com")
        assert mock.call_args.args[0] == "POST"
        assert mock.call_args.args[1] == "/contacts"
        assert mock.call_args.kwargs["json"] == {"email": "x@y.com"}
        assert mock.call_args.kwargs["confirm"] is True

    def test_set_affiliate_payout_destination_uses_confirmed_request(self):
        mock = self._mock_and_call("set_affiliate_payout_destination", method="btc")
        assert mock.call_args.args[0] == "PUT"
        assert mock.call_args.args[1] == "/affiliate/payout-destination"
        assert mock.call_args.kwargs["json"] == {"method": "btc"}
        assert mock.call_args.kwargs["confirm"] is True

    def test_set_snapshot_protection_uses_confirmed_request(self):
        mock = self._mock_and_call("set_snapshot_protection", 1077, "snap-1", True)
        assert mock.call_args.args[0] == "PATCH"
        assert mock.call_args.args[1] == "/vm/1077/snapshots/protection"
        assert mock.call_args.kwargs["json"] == {"snapshot_id": "snap-1", "protected": True}
        assert mock.call_args.kwargs["confirm"] is True

    def test_set_backup_protection_uses_confirmed_request(self):
        mock = self._mock_and_call("set_backup_protection", 1077, "bk-1", False)
        assert mock.call_args.args[0] == "PATCH"
        assert mock.call_args.args[1] == "/vm/1077/backups/protection"
        assert mock.call_args.kwargs["json"] == {"backup_id": "bk-1", "protected": False}
        assert mock.call_args.kwargs["confirm"] is True

    def test_get_vm_credentials_uses_confirmed_request(self):
        mock = self._mock_and_call("get_vm_credentials", 1077)
        assert mock.call_args.args[0] == "GET"
        assert mock.call_args.args[1] == "/vm/1077/credentials"
        assert mock.call_args.kwargs["confirm"] is True

    def test_set_stored_ssh_key_uses_confirmed_request(self):
        mock = self._mock_and_call("set_stored_ssh_key", 1077, "ssh-ed25519 AAAA...")
        assert mock.call_args.args[0] == "POST"
        assert mock.call_args.args[1] == "/ssh-key"
        assert mock.call_args.kwargs["json"] == {"service_id": 1077, "public_key": "ssh-ed25519 AAAA..."}
        assert mock.call_args.kwargs["confirm"] is True

    def test_delete_stored_ssh_key_uses_confirmed_request(self):
        mock = self._mock_and_call("delete_stored_ssh_key", 1077)
        assert mock.call_args.args[0] == "DELETE"
        assert mock.call_args.args[1] == "/ssh-key"
        assert mock.call_args.kwargs["params"] == {"service_id": 1077}
        assert mock.call_args.kwargs["confirm"] is True

    def test_unmount_iso_uses_confirmed_request(self):
        mock = self._mock_and_call("unmount_iso", 1077)
        assert mock.call_args.args[0] == "POST"
        assert mock.call_args.args[1] == "/vm/1077/iso/unmount"
        assert mock.call_args.kwargs["confirm"] is True

    def test_probe_mode_surfaces_409_for_get_vm_credentials(self):
        """confirm=False probes — the 409 propagates instead of auto-confirming."""
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient
        client = SHCClient(api_key="test-key")
        with patch.object(client, "_confirmed_request", return_value={"ok": True}) as mock:
            client.get_vm_credentials(1077, confirm=False)
            assert mock.call_args.kwargs["confirm"] is False


class TestMcpProbeMode:
    """MCP confirm=False probe mode — call_tool honors the confirm parameter."""

    def test_confirm_false_passed_through_to_call_tool(self):
        from unittest.mock import patch
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        with patch.object(mc, "call_tool", return_value={"ok": True}) as mock:
            mc.update_preferences(theme="dark", confirm=False)
            assert mock.call_args.kwargs.get("confirm") is False

    def test_call_tool_probe_mode_raises_on_confirmation_required(self):
        from unittest.mock import patch
        from shc_toolkit.mcp_client import SHCMCPClient
        from shc_toolkit.client import SHCConfirmationRequiredError

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        confirmation_response = {
            "result": {
                "structuredContent": {
                    "status": "confirmation_required",
                    "how_to_proceed": {"arguments": {"_confirmation_id": "cnf_test"}},
                    "request_id": "req_test",
                }
            }
        }
        with patch.object(mc, "_send_jsonrpc", return_value=confirmation_response):
            with pytest.raises(SHCConfirmationRequiredError):
                mc.call_tool("cancelVirtualMachine", {"serviceId": 123}, confirm=False)

    def test_call_tool_default_auto_confirms(self):
        from unittest.mock import patch
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        confirmation_response = {
            "result": {
                "structuredContent": {
                    "status": "confirmation_required",
                    "how_to_proceed": {"arguments": {"_confirmation_id": "cnf_test"}},
                }
            }
        }
        success_response = {
            "result": {"structuredContent": {"data": {"ok": True}}},
        }
        with patch.object(
            mc, "_send_jsonrpc", side_effect=[confirmation_response, success_response]
        ):
            result = mc.call_tool("cancelVirtualMachine", {"serviceId": 123})
            assert result == {"ok": True}


class TestBatchHelper:
    """SHCClient.batch() convenience wrapper for POST /batch."""

    def test_batch_single_request(self):
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        fake = {"items": [{"id": "r1", "status": 200, "body": {"data": {"ok": True}}}]}
        with patch.object(client, "_request", return_value=fake):
            results = client.batch([{"method": "GET", "path": "/account", "id": "r1"}])
            assert len(results) == 1
            assert results[0]["status"] == 200

    def test_batch_preserves_order(self):
        from unittest.mock import patch
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        fake = {
            "items": [
                {"id": "a", "status": 200, "body": {}},
                {"id": "b", "status": 200, "body": {}},
            ]
        }
        with patch.object(client, "_request", return_value=fake):
            results = client.batch(
                [
                    {"method": "GET", "path": "/account", "id": "a"},
                    {"method": "GET", "path": "/vms", "id": "b"},
                ]
            )
            assert results[0]["id"] == "a"
            assert results[1]["id"] == "b"

    def test_batch_rejects_over_25(self):
        from shc_toolkit.client import SHCClient

        client = SHCClient(api_key="test-key")
        too_many = [{"method": "GET", "path": f"/x/{i}"} for i in range(26)]
        with pytest.raises(ValueError, match="25"):
            client.batch(too_many)


def _run_cli(argv):
    """Run a CLI command with a mocked client. Returns the mock."""
    mock_client = MagicMock()
    mock_client.reap_orphans.return_value = []
    with patch("shc_toolkit.cli._client", return_value=mock_client), patch(
        "shc_toolkit.cli._print"
    ), patch("shc_toolkit.cli._get_fmt", return_value="json"), patch("builtins.print"):
        with patch("sys.argv", argv):
            try:
                from shc_toolkit.cli import main
                main()
            except SystemExit:
                pass
    return mock_client


class TestCliCommandCoverage:
    """Comprehensive CLI command coverage — verifies each command dispatches
    to the correct SHCClient/SHCMCPClient method. Uses a mocked client so no
    real API calls are made."""

    # ── No-arg read commands ─────────────────────────────────
    @pytest.mark.parametrize("cmd,method", [
        ("account", "get_account"),
        ("balance", "get_billing_balance"),
        ("catalog", "get_catalog"),
        ("templates", "list_templates"),
        ("sizes", None),
        ("contacts", "list_contacts"),
        ("quotations", "list_quotations"),
        ("downloads", "list_downloads"),
        ("transactions", "list_transactions"),
        ("emails", "list_emails"),
        ("events", "list_events"),
    ])
    def test_cli_no_arg_read(self, cmd, method):
        mock = _run_cli(["shc", cmd])
        if method:
            getattr(mock, method).assert_called_once()

    # ── VM-specific read commands (service_id) ───────────────
    @pytest.mark.parametrize("cmd,method", [
        ("info", "get_vm_summary"),
        ("detail", "get_vm_detail"),
        ("metrics", "get_vm_metrics"),
        ("bandwidth", "get_vm_bandwidth"),
        ("health", "check_vm_health"),
        ("snapshots", "list_snapshots"),
        ("backups", "list_backups"),
        ("jobs", "list_jobs"),
        ("network", "get_vm_network"),
        ("payments", "get_vm_payments"),
        ("console", "get_console_availability"),
        ("iso", "list_isos"),
        ("rdns", "list_rdns"),
        ("ssh-keys", "list_ssh_keys"),
        ("upgrade-options", "list_upgrade_options"),
        ("addons", "list_vm_addons"),
        ("term-options", "get_vm_term_options"),
    ])
    def test_cli_vm_read(self, cmd, method):
        mock = _run_cli(["shc", cmd, "1077"])
        getattr(mock, method).assert_called_once()

    # ── VM action commands (service_id, confirm-gated) ───────
    @pytest.mark.parametrize("cmd,method", [
        ("start", "start_vm"),
        ("stop", "stop_vm"),
        ("shutdown", "shutdown_vm"),
        ("reset", "reset_vm"),
        ("restart", "restart_vm"),
        ("cancel", "cancel_vm"),
        ("reinstall", "reinstall_vm"),
    ])
    def test_cli_vm_action(self, cmd, method):
        mock = _run_cli(["shc", cmd, "1077"])
        getattr(mock, method).assert_called_once()

    # ── Invoice/billing commands ─────────────────────────────
    def test_cli_invoices_list(self):
        mock = _run_cli(["shc", "invoices"])
        mock.list_invoices.assert_called_once()

    def test_cli_invoice_get(self):
        mock = _run_cli(["shc", "invoices", "123"])
        mock.get_invoice.assert_called_once()

    def test_cli_activity_account(self):
        mock = _run_cli(["shc", "activity"])
        mock.get_account_activity.assert_called_once()

    # ── Snapshot/backup action commands ──────────────────────
    def test_cli_snapshot_create(self):
        mock = _run_cli(["shc", "snapshot-create", "1077", "--name", "pre"])
        mock.create_snapshot.assert_called_once()

    def test_cli_backup_create(self):
        mock = _run_cli(["shc", "backup-create", "1077", "--name", "bk"])
        mock.create_backup.assert_called_once()

    # ── Firewall commands ────────────────────────────────────
    def test_cli_firewall_show(self):
        mock = _run_cli(["shc", "firewall", "1077", "show"])
        mock.get_firewall.assert_called_once()

    # ── Tickets command ──────────────────────────────────────
    def test_cli_tickets_list(self):
        mock = _run_cli(["shc", "tickets", "list"])
        mock.list_support_tickets.assert_called_once()

    def test_cli_tickets_departments(self):
        mock = _run_cli(["shc", "tickets", "departments"])
        mock.list_support_departments.assert_called_once()

    # ── Reap dry-run ─────────────────────────────────────────
    def test_cli_reap_dry_run(self):
        mock = _run_cli(["shc", "reap", "--dry-run"])
        mock.reap_orphans.assert_called_once_with(max_age_hours=2.0, dry_run=True)

    # ── Upgrade commands ─────────────────────────────────────
    def test_cli_upgrade_preview(self):
        mock = _run_cli(["shc", "upgrade-preview", "1077", "--package-id", "26"])
        mock.preview_upgrade.assert_called_once()

    # ── SSH key commands ─────────────────────────────────────
    def test_cli_ssh_key_add(self):
        mock = _run_cli(["shc", "ssh-key-add", "1077", "--key", "ssh-ed25519 AAAA"])
        mock.add_ssh_key.assert_called_once()

    # ── ISO mount/unmount ────────────────────────────────────
    def test_cli_iso_mount(self):
        mock = _run_cli(["shc", "iso-mount", "1077", "debian-13.iso"])
        mock.mount_iso.assert_called_once()

    # ── rDNS set/clear ───────────────────────────────────────
    def test_cli_rdns_set(self):
        mock = _run_cli(["shc", "rdns-set", "1077", "--ip", "1.2.3.4", "--ptr", "host.example.com"])
        mock.set_rdns.assert_called_once()

    def test_cli_rdns_clear(self):
        mock = _run_cli(["shc", "rdns-clear", "1077", "--ip", "1.2.3.4"])
        mock.clear_rdns.assert_called_once()

    # ── Console session ──────────────────────────────────────
    def test_cli_console_session(self):
        mock = _run_cli(["shc", "console-session", "1077"])
        mock.create_console_session.assert_called_once()

    def test_cli_console_session_ttl(self):
        mock = _run_cli(["shc", "console-session", "1077", "--ttl", "300"])
        mock.create_console_session.assert_called_once_with(1077, ttl=300)

    # ── Job detail ───────────────────────────────────────────
    def test_cli_job_get(self):
        mock = _run_cli(["shc", "job", "1077", "job-abc123"])
        mock.get_job.assert_called_once()


class TestRetryBackoff:
    """Comprehensive retry/backoff tests for SHCClient._request.

    The retry layer handles:
    - Network errors (httpx.HTTPError) → retry with exponential backoff
    - 408/429 → retry with Retry-After header or backoff fallback
    - 500+ → retry with backoff
    - Max retries exhausted → raise last error
    - Non-retryable (400/401/403/404) → raise immediately, no retry
    """

    def _make_resp(self, status, body=None, headers=None):
        r = MagicMock()
        r.status_code = status
        r.text = json.dumps(body) if body else ""
        r.headers = headers or {}
        return r

    def test_retry_on_network_error_then_success(self):
        client = SHCClient(api_key="test-key")
        with patch.object(client.session, "request", side_effect=[
            httpx.ConnectError("refused"),
            self._make_resp(200, {"data": {"ok": True}}),
        ]), patch("time.sleep"):
            result = client._get("/test")
        assert result == {"ok": True}

    def test_retry_on_500_then_success(self):
        client = SHCClient(api_key="test-key")
        with patch.object(client.session, "request", side_effect=[
            self._make_resp(500, {"error": {"code": "upstream_failure"}}),
            self._make_resp(200, {"data": {"ok": True}}),
        ]), patch("time.sleep"):
            result = client._get("/test")
        assert result == {"ok": True}

    def test_retry_on_408_then_success(self):
        client = SHCClient(api_key="test-key")
        with patch.object(client.session, "request", side_effect=[
            self._make_resp(408, {"error": {"code": "timeout"}}),
            self._make_resp(200, {"data": {"ok": True}}),
        ]), patch("time.sleep"):
            result = client._get("/test")
        assert result == {"ok": True}

    def test_retry_on_429_with_retry_after_header(self):
        client = SHCClient(api_key="test-key")
        with patch.object(client.session, "request", side_effect=[
            self._make_resp(429, {"error": {"code": "rate_limited"}},
                            headers={"Retry-After": "1"}),
            self._make_resp(200, {"data": {"ok": True}}),
        ]), patch("time.sleep"):
            result = client._get("/test")
        assert result == {"ok": True}

    def test_max_retries_exhausted_on_network_error(self):
        client = SHCClient(api_key="test-key")
        client._max_retries = 3
        with patch.object(client.session, "request",
                          side_effect=httpx.ConnectError("refused")), patch("time.sleep"):
            with pytest.raises(httpx.ConnectError):
                client._get("/test")

    def test_max_retries_exhausted_on_500(self):
        client = SHCClient(api_key="test-key")
        client._max_retries = 3
        with patch.object(client.session, "request", return_value=self._make_resp(
            500, {"error": {"code": "upstream_failure"}}
        )), patch("time.sleep"):
            with pytest.raises(SHCError):
                client._get("/test")

    def test_no_retry_on_404(self):
        client = SHCClient(api_key="test-key")
        call_count = 0
        resp = self._make_resp(404, {"error": {"code": "not_found", "message": "gone"}})
        with patch.object(client.session, "request", return_value=resp) as mock_req:
            with pytest.raises(SHCError):
                client._get("/test")
        assert mock_req.call_count == 1

    def test_no_retry_on_401(self):
        client = SHCClient(api_key="test-key")
        resp = self._make_resp(401, {"error": {"code": "invalid_token"}})
        with patch.object(client.session, "request", return_value=resp) as mock_req:
            with pytest.raises(SHCError):
                client._get("/test")
        assert mock_req.call_count == 1

    def test_no_retry_on_400(self):
        client = SHCClient(api_key="test-key")
        resp = self._make_resp(400, {"error": {"code": "validation_failed"}})
        with patch.object(client.session, "request", return_value=resp) as mock_req:
            with pytest.raises(SHCError):
                client._get("/test")
        assert mock_req.call_count == 1

    def test_backoff_is_exponential_with_jitter(self):
        client = SHCClient(api_key="test-key")
        client._backoff_base = 1.0
        client._backoff_cap = 60.0
        for attempt in range(5):
            delay = client._backoff_delay(attempt)
            expected = min(60.0, 1.0 * (2**attempt))
            assert expected * 0.8 <= delay <= expected * 1.2, (
                f"attempt {attempt}: expected ~{expected:.1f}s, got {delay:.1f}s"
            )

    def test_backoff_cap_respected(self):
        client = SHCClient(api_key="test-key")
        client._backoff_base = 100.0
        client._backoff_cap = 5.0
        for attempt in range(10):
            delay = client._backoff_delay(attempt)
            assert delay <= client._backoff_cap

    def test_rate_limit_error_has_retry_after(self):
        client = SHCClient(api_key="test-key")
        resp = self._make_resp(429, {
            "error": {"code": "rate_limited", "retry_after_seconds": 30}
        })
        with patch.object(client.session, "request", return_value=resp), patch("time.sleep"):
            with pytest.raises(SHCError) as exc_info:
                client._request("GET", "/test")
            assert hasattr(exc_info.value, "retry_after_seconds")

    def test_409_confirmation_error_has_confirmation_id(self):
        client = SHCClient(api_key="test-key")
        client._max_retries = 1
        resp = self._make_resp(409, {
            "error": {"code": "confirmation_required"},
            "confirmation": {"confirmation_id": "cnf_test123"},
        })
        with patch.object(client.session, "request", return_value=resp):
            with pytest.raises(Exception) as exc_info:
                client._request("GET", "/test")
            assert hasattr(exc_info.value, "confirmation_id") or \
                   hasattr(exc_info.value, "details")


class TestMcpErrorHandling:
    """SHCMCPClient error handling — isError responses, malformed data, edge cases."""

    def test_iserror_response_raises_shc_error(self):
        from shc_toolkit.mcp_client import SHCMCPClient
        from shc_toolkit.client import SHCError

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        error_response = {
            "result": {
                "isError": True,
                "structuredContent": {
                    "error": {
                        "code": "not_found",
                        "message": "VM not found",
                        "error_code": "not_found",
                    },
                    "request_id": "req_test",
                },
            }
        }
        with patch.object(mc, "_send_jsonrpc", return_value=error_response):
            with pytest.raises(SHCError) as exc_info:
                mc.call_tool("getVirtualMachine", {"serviceId": 999})
            assert "not_found" in str(exc_info.value)

    def test_empty_result_returns_empty(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        empty_response = {"result": {}}
        with patch.object(mc, "_send_jsonrpc", return_value=empty_response):
            result = mc.call_tool("listVirtualMachines")
        assert result == {}

    def test_text_content_returned_as_string(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        text_response = {
            "result": {
                "content": [{"type": "text", "text": "hello world"}],
            }
        }
        with patch.object(mc, "_send_jsonrpc", return_value=text_response):
            result = mc.call_tool("someTool")
        assert result == "hello world"

    def test_text_content_json_parsed(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        json_response = {
            "result": {
                "content": [{"type": "text", "text": '{"data": {"count": 42}}'}],
            }
        }
        with patch.object(mc, "_send_jsonrpc", return_value=json_response):
            result = mc.call_tool("someTool")
        assert result == {"data": {"count": 42}}

    def test_structured_content_data_extracted(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        nested_response = {
            "result": {
                "structuredContent": {"data": {"vms": [{"id": 1}]}},
            }
        }
        with patch.object(mc, "_send_jsonrpc", return_value=nested_response):
            result = mc.call_tool("listVirtualMachines")
        assert result == {"vms": [{"id": 1}]}

    def test_doubly_nested_data_extracted(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        mc._initialized = True
        nested_response = {
            "result": {
                "structuredContent": {"data": {"data": {"deep": True}}},
            }
        }
        with patch.object(mc, "_send_jsonrpc", return_value=nested_response):
            result = mc.call_tool("someTool")
        assert result == {"deep": True}

    def test_extract_items_from_dict_with_items(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        result = mc._extract_items({"items": [1, 2, 3]})
        assert result == [1, 2, 3]

    def test_extract_items_from_list(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        result = mc._extract_items([1, 2, 3])
        assert result == [1, 2, 3]

    def test_extract_items_from_empty(self):
        from shc_toolkit.mcp_client import SHCMCPClient

        mc = SHCMCPClient.__new__(SHCMCPClient)
        result = mc._extract_items(None)
        assert result == []


# ── llms-full.txt corpus audit: jit_pay + BIP21 + nostr operate-lane ──────


class TestJitPayInvoicePolling:
    """Corpus audit: poll_shc_invoice must hit /payment/{id} and unwrap data."""

    def _client(self):
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            return SHCClient()

    def test_poll_shc_invoice_hits_payment_path(self):
        from shc_toolkit.jit_pay import poll_shc_invoice

        c = self._client()
        calls = []

        def fake_get(path):
            calls.append(path)
            return {"data": {"status": "paid"}}

        c._get = fake_get
        assert poll_shc_invoice(c, 42, timeout=5) is True
        assert calls == ["/payment/42"], f"polled wrong path: {calls}"

    def test_poll_shc_invoice_unwraps_data_envelope(self):
        from shc_toolkit.jit_pay import poll_shc_invoice

        c = self._client()
        c._get = lambda path: {"data": {"status": "confirmed"}}
        assert poll_shc_invoice(c, 7, timeout=5) is True

    def test_poll_shc_invoice_stale_when_unpaid(self):
        from shc_toolkit.jit_pay import poll_shc_invoice

        c = self._client()
        c._get = lambda path: {"data": {"status": "processing"}}
        assert poll_shc_invoice(c, 7, timeout=0.2) is False


class TestBip21Stitch:
    """Corpus shc-pay skill: BIP21 stitch table for credit responses."""

    def test_both_rails(self):
        from shc_toolkit.jit_pay import bip21_stitch

        assert (
            bip21_stitch("bc1qxyz", "lnbcabc")
            == "bitcoin:bc1qxyz?lightning=lnbcabc"
        )

    def test_onchain_only(self):
        from shc_toolkit.jit_pay import bip21_stitch

        assert bip21_stitch("bc1qxyz", None) == "bitcoin:bc1qxyz"

    def test_lightning_only(self):
        from shc_toolkit.jit_pay import bip21_stitch

        assert bip21_stitch(None, "lnbcabc") == "lightning:lnbcabc"

    def test_no_rail(self):
        from shc_toolkit.jit_pay import bip21_stitch

        assert bip21_stitch(None, None) is None

    def test_payment_uri_prefers_server_payment_link(self):
        from shc_toolkit.jit_pay import payment_uri

        data = {
            "payment_link": "lightning:lnbcserver",
            "bolt11": "lnbcabc",
            "onchain_address": "bc1qxyz",
        }
        assert payment_uri(data) == "lightning:lnbcserver"

    def test_payment_uri_falls_back_to_stitch(self):
        from shc_toolkit.jit_pay import payment_uri

        assert payment_uri(
            {"payment_link": None, "bolt11": "lnbcabc", "onchain_address": "bc1qxyz"}
        ) == "bitcoin:bc1qxyz?lightning=lnbcabc"

    def test_payment_uri_none_when_no_rail(self):
        from shc_toolkit.jit_pay import payment_uri

        assert payment_uri({"checkout_url": "https://x"}) is None


class TestNostrOperateGrant:
    """Corpus nostr-operate-lane: exchange a kind:30078 grant for a
    short-TTL vm-scoped operate Bearer via the plugin endpoint."""

    def _client(self):
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            return SHCClient()

    def _good_grant(self):
        import time

        now = int(time.time())
        return {
            "id": "a" * 64,
            "pubkey": "b" * 64,
            "sig": "c" * 64,
            "kind": 30078,
            "created_at": now,
            "content": "",
            "tags": [
                ["d", "shc:agent:" + "d" * 64],
                ["scope", "operate"],
                ["area", "vm:456"],
                ["aud", "shc:https://blesta.sovereignhybridcompute.com"],
                ["nbf", str(now)],
                ["exp", str(now + 900)],
            ],
        }

    def test_signer_builds_nip98_event(self):
        from nostr_sdk import Keys

        from shc_toolkit.client import _sign_nip98_operate_request

        nsec = Keys.generate().secret_key().to_bech32()
        event = _sign_nip98_operate_request(
            nsec,
            "https://blesta.sovereignhybridcompute.com/plugin/nostr_auth/main/operate_token",
        )
        assert event["kind"] == 27235
        tags = {t[0]: t[1] for t in event["tags"]}
        assert tags["u"].startswith("https://blesta.sovereignhybridcompute.com/plugin/")
        assert tags["method"] == "POST"
        assert tags.get("nonce")
        assert event["sig"] and event["id"]

    def test_standalone_exchange_posts_nostr_auth_to_plugin_url(
        self, monkeypatch
    ):
        import base64
        import json as _json

        import httpx
        from nostr_sdk import Keys

        from shc_toolkit.client import exchange_nostr_operate_grant

        nsec = Keys.generate().secret_key().to_bech32()
        captured = {}

        def fake_request(_self, method, url=None, **kwargs):
            captured["method"] = method
            captured["url"] = url
            captured["headers"] = dict(kwargs.get("headers") or {})
            captured["json"] = kwargs.get("json")
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = _json.dumps(
                {"data": {"success": True, "token": "a" * 64, "expires_in": 900}}
            )
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)

        grant = self._good_grant()
        result = exchange_nostr_operate_grant(grant, nsec=nsec)

        assert captured["method"] == "POST"
        assert (
            captured["url"]
            == "https://blesta.sovereignhybridcompute.com/plugin/nostr_auth/main/operate_token"
        )
        auth = captured["headers"]["Authorization"]
        assert auth.startswith("Nostr ")
        decoded = _json.loads(base64.b64decode(auth[len("Nostr ") :]))
        assert decoded["kind"] == 27235
        tags = {t[0]: t[1] for t in decoded["tags"]}
        assert tags["u"] == captured["url"]
        assert tags["method"] == "POST"
        assert captured["json"] == {"grant": grant}
        assert result["success"] is True
        assert result["token"] == "a" * 64

    def test_validate_operate_grant_reports_problems(self):
        from shc_toolkit.client import validate_operate_grant

        good = self._good_grant()
        assert (
            validate_operate_grant(
                good, expected_aud="shc:https://blesta.sovereignhybridcompute.com"
            )
            == []
        )

        def problems_for(**mutate):
            grant = self._good_grant()
            for key, value in mutate.items():
                if key == "drop_tag":
                    grant["tags"] = [t for t in grant["tags"] if t[0] != value]
                elif key == "tag":
                    name, val = value
                    grant["tags"] = [
                        [name, val] if t[0] == name else t for t in grant["tags"]
                    ]
                else:
                    grant[key] = value
            return " ".join(validate_operate_grant(grant, expected_aud="shc:https://x"))

        assert "kind" in problems_for(kind=1)
        g = self._good_grant()
        del g["sig"]
        assert "sig" in " ".join(validate_operate_grant(g))
        assert "tag d " in problems_for(drop_tag="d")
        assert "tag scope" in problems_for(tag=("scope", "read"))
        assert "tag area" in problems_for(drop_tag="area")
        assert "tag aud" in problems_for(tag=("aud", "shc:https://evil.example"))
        assert "expired" in problems_for(tag=("exp", str(1)))
        assert "not yet valid" in problems_for(tag=("nbf", str(2**40)))

    def test_exchange_rejects_invalid_grant_locally(self, monkeypatch):
        import httpx
        from nostr_sdk import Keys

        from shc_toolkit.client import exchange_nostr_operate_grant

        def explode(*a, **k):
            raise AssertionError("HTTP must not be called for an invalid grant")

        monkeypatch.setattr(httpx.Client, "request", explode)
        bad = self._good_grant()
        bad["kind"] = 7
        with pytest.raises(SHCError, match="invalid_grant"):
            exchange_nostr_operate_grant(
                bad, nsec=Keys.generate().secret_key().to_bech32()
            )

    def test_exchange_maps_server_error(self, monkeypatch):
        import json as _json

        import httpx
        from nostr_sdk import Keys

        from shc_toolkit.client import exchange_nostr_operate_grant

        def fake_request(*a, **k):
            m = MagicMock()
            m.status_code = 403
            m.headers = {}
            m.text = _json.dumps(
                {"error": {"code": "forbidden", "message": "Invalid grant"}}
            )
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)
        with pytest.raises(SHCError, match="Invalid grant"):
            exchange_nostr_operate_grant(
                self._good_grant(), nsec=Keys.generate().secret_key().to_bech32()
            )

    def test_method_delegates_and_leaves_session_alone(self, monkeypatch):
        import json as _json

        import httpx
        from nostr_sdk import Keys

        c = self._client()
        nsec = Keys.generate().secret_key().to_bech32()

        def fake_request(*a, **k):
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = _json.dumps({"data": {"success": True}})
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)
        result = c.exchange_nostr_operate_grant(self._good_grant(), nsec=nsec)
        assert result == {"success": True}
        assert c.session.headers["Authorization"] == "Bearer shc_live_test"


class TestUserAgent:
    def test_client_sends_toolkit_ua(self):
        c = self._mk()
        captured = {}

        def cap(method, url, **kw):
            captured.update({k.lower(): v for k, v in (kw.get("headers") or {}).items()})
            captured.update({k.lower(): v for k, v in dict(c.session.headers).items()})
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = '{"data": {}}'
            return m

        c.session.request = MagicMock(side_effect=cap)
        c._get("/test")
        assert captured.get("user-agent", "").startswith("shc-toolkit/")

    def test_ua_carries_installed_version(self):
        from importlib.metadata import PackageNotFoundError, version

        c = self._mk()
        ua = dict(c.session.headers).get("user-agent") or next(
            v for k, v in c.session.headers.items() if k.lower() == "user-agent"
        )
        try:
            expected = f"shc-toolkit/{version('shc-toolkit')}"
        except PackageNotFoundError:
            expected = "shc-toolkit/dev"
        assert ua == expected

    def test_standalone_exchange_sends_ua(self, monkeypatch):
        import json as _json

        import httpx
        from nostr_sdk import Keys

        from shc_toolkit.client import exchange_nostr_operate_grant

        seen = {}

        def fake_request(_self, method, url=None, **kwargs):
            seen["ua"] = dict(kwargs.get("headers") or {}).get("User-Agent", "")
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = _json.dumps({"data": {"success": True}})
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)
        now = __import__("time").time()
        grant = {
            "id": "a" * 64, "pubkey": "b" * 64, "sig": "c" * 64,
            "kind": 30078, "created_at": int(now), "content": "",
            "tags": [["d", "shc:agent:" + "d" * 64], ["scope", "operate"],
                     ["area", "vm:1"], ["aud", "shc:https://blesta.sovereignhybridcompute.com"],
                     ["nbf", str(int(now))], ["exp", str(int(now) + 900)]],
        }
        exchange_nostr_operate_grant(
            grant, nsec=Keys.generate().secret_key().to_bech32()
        )
        assert seen["ua"].startswith("shc-toolkit/")

    @staticmethod
    def _mk():
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            return SHCClient()


class TestNostrOperateGrantExtras:
    def test_nonce_and_id_unique_per_request(self):
        from nostr_sdk import Keys

        from shc_toolkit.client import _sign_nip98_operate_request

        nsec = Keys.generate().secret_key().to_bech32()
        e1 = _sign_nip98_operate_request(nsec, "https://x.example/t")
        e2 = _sign_nip98_operate_request(nsec, "https://x.example/t")
        t1 = {t[0]: t[1] for t in e1["tags"]}
        t2 = {t[0]: t[1] for t in e2["tags"]}
        assert t1["nonce"] != t2["nonce"]
        assert e1["id"] != e2["id"]

    def test_method_delegation_uses_client_base_url(self, monkeypatch):
        import json as _json

        import httpx
        from nostr_sdk import Keys

        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient(base_url="https://api.example.test/user-api/v2")
        seen = {}

        def fake_request(_self, method, url=None, **kwargs):
            seen["url"] = url
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = _json.dumps({"data": {"success": True}})
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)
        now = __import__("time").time()
        grant = {
            "id": "a" * 64, "pubkey": "b" * 64, "sig": "c" * 64,
            "kind": 30078, "created_at": int(now), "content": "",
            "tags": [["d", "shc:agent:" + "d" * 64], ["scope", "operate"],
                     ["area", "vm:1"], ["aud", "shc:https://api.example.test"],
                     ["nbf", str(int(now))], ["exp", str(int(now) + 900)]],
        }
        c.exchange_nostr_operate_grant(grant, nsec=Keys.generate().secret_key().to_bech32())
        assert seen["url"] == "https://api.example.test/plugin/nostr_auth/main/operate_token"

    def test_default_base_url_targets_production_plugin(self, monkeypatch):
        import json as _json

        import httpx
        from nostr_sdk import Keys

        from shc_toolkit.client import exchange_nostr_operate_grant

        seen = {}

        def fake_request(_self, method, url=None, **kwargs):
            seen["url"] = url
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = _json.dumps({"data": {"success": True}})
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)
        now = __import__("time").time()
        grant = {
            "id": "a" * 64, "pubkey": "b" * 64, "sig": "c" * 64,
            "kind": 30078, "created_at": int(now), "content": "",
            "tags": [["d", "shc:agent:" + "d" * 64], ["scope", "operate"],
                     ["area", "vm:1"], ["aud", "shc:https://blesta.sovereignhybridcompute.com"],
                     ["nbf", str(int(now))], ["exp", str(int(now) + 900)]],
        }
        exchange_nostr_operate_grant(
            grant, nsec=Keys.generate().secret_key().to_bech32()
        )
        assert seen["url"] == (
            "https://blesta.sovereignhybridcompute.com/plugin/nostr_auth/main/operate_token"
        )

    def test_validate_rejects_non_dict(self):
        from shc_toolkit.client import validate_operate_grant

        assert validate_operate_grant("not-a-grant") == ["grant is not a JSON object"]

    def test_validate_requires_aud_when_not_expected(self):
        import time

        from shc_toolkit.client import validate_operate_grant

        now = int(time.time())
        grant = {
            "id": "a" * 64, "pubkey": "b" * 64, "sig": "c" * 64,
            "kind": 30078, "created_at": now, "content": "",
            "tags": [["d", "shc:agent:" + "d" * 64], ["scope", "operate"],
                     ["area", "vm:1"],
                     ["nbf", str(now)], ["exp", str(now + 900)]],
        }
        assert any("aud" in p for p in validate_operate_grant(grant))


class TestPollInvoiceErrorPath:
    def test_poll_survives_transient_errors(self, monkeypatch):
        from shc_toolkit.jit_pay import poll_shc_invoice

        monkeypatch.setattr("time.sleep", lambda *_: None)
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
        state = {"n": 0}

        def flaky(path):
            state["n"] += 1
            if state["n"] < 3:
                raise RuntimeError("transient")
            return {"data": {"status": "paid"}}

        c._get = flaky
        assert poll_shc_invoice(c, 9, timeout=5) is True
        assert state["n"] == 3


class TestPaymentUriEdges:
    def test_empty_payment_link_falls_back_to_stitch(self):
        from shc_toolkit.jit_pay import payment_uri

        assert (
            payment_uri({"payment_link": "", "onchain_address": "bc1qx", "bolt11": "lnbcz"})
            == "bitcoin:bc1qx?lightning=lnbcz"
        )

    def test_non_dict_returns_none(self):
        from shc_toolkit.jit_pay import payment_uri

        assert payment_uri(None) is None
        assert payment_uri("lightning:x") is None


class TestTopupUsesResponseRails:
    def _grant_paid_after(self, fake_client_cls, monkeypatch):
        from shc_toolkit import register as reg

        rendered = []
        monkeypatch.setattr(reg, "_POLL_SECONDS", 0)
        monkeypatch.setattr("shc_toolkit.jit_pay.render_qr", lambda uri: rendered.append(uri))
        reg._topup(
            fake_client_cls(), 5.0, browser=False, timeout=2, log=lambda m: None
        )
        return rendered

    def test_prefers_payment_link_without_scraping(self, monkeypatch):
        from shc_toolkit import register as reg

        def explode(url):
            raise AssertionError("checkout HTML must not be scraped when rails present")

        monkeypatch.setattr("shc_toolkit.jit_pay.fetch_bolt11", explode)

        class FakeClient:
            def topup_credit(self, amount):
                return {
                    "invoice_id": 5,
                    "checkout_url": "https://btcpay.example/i/x",
                    "payment_link": "lightning:lnbcfromresp",
                }

            def _get(self, path):
                return {"data": {"status": "paid"}}

        rendered = self._grant_paid_after(FakeClient, monkeypatch)
        assert rendered == ["lightning:lnbcfromresp"]

    def test_falls_back_to_checkout_scrape(self, monkeypatch):
        from shc_toolkit import register as reg

        monkeypatch.setattr("shc_toolkit.jit_pay.fetch_bolt11", lambda url: "lnbcscraped")

        class FakeClient:
            def topup_credit(self, amount):
                return {"invoice_id": 5, "checkout_url": "https://btcpay.example/i/x"}

            def _get(self, path):
                return {"data": {"status": "paid"}}

        rendered = self._grant_paid_after(FakeClient, monkeypatch)
        assert rendered == ["lightning:lnbcscraped"]


class TestErrorFromBodyStringShape:
    """The operate_token plugin route returns a FLAT string error
    ({"error": "Grant is not bound to this agent key"}), not the nested
    {"error": {code, message}} shape of /user-api/v2. Found live."""

    def test_string_error_403_maps_to_auth_error(self):
        from shc_toolkit.client import SHCAuthError, _error_from_body

        exc = _error_from_body({"error": "Grant is not bound to this agent key"}, "", 403)
        assert isinstance(exc, SHCAuthError)
        assert "not bound to this agent key" in exc.message

    def test_string_error_other_status_is_generic(self):
        from shc_toolkit.client import SHCError, _error_from_body

        exc = _error_from_body({"error": "boom"}, "", 500)
        assert type(exc) is SHCError
        assert exc.message == "boom"

    def test_nested_shape_unaffected(self):
        from shc_toolkit.client import SHCNotFoundError, _error_from_body

        exc = _error_from_body(
            {"error": {"code": "not_found", "message": "gone"}}, "", 404
        )
        assert isinstance(exc, SHCNotFoundError)
        assert exc.message == "gone"


class TestSignOperateGrant:
    """Customer side of the lane: sign a kind:30078 grant for one agent+VM."""

    def _sign(self, **kw):
        from shc_toolkit.client import sign_operate_grant

        defaults = dict(
            nsec=None, service_id=456, agent_pubkey=None, ttl=900
        )
        return defaults, kw

    def test_grant_shape_and_tags(self):
        import json as _json
        import time

        from nostr_sdk import Event, Keys

        from shc_toolkit.client import sign_operate_grant

        customer = Keys.generate()
        agent_hex = Keys.generate().public_key().to_hex()
        before = int(time.time())
        grant = sign_operate_grant(
            customer.secret_key().to_bech32(),
            service_id=456,
            agent_pubkey=agent_hex,
            ttl=600,
        )
        assert grant["kind"] == 30078
        assert Event.from_json(_json.dumps(grant)).verify()
        tags = {t[0]: t[1] for t in grant["tags"]}
        assert tags["d"] == f"shc:agent:{agent_hex}"
        assert tags["scope"] == "operate"
        assert tags["area"] == "vm:456"
        assert tags["aud"] == "shc:https://blesta.sovereignhybridcompute.com"
        assert before <= int(tags["nbf"]) <= int(tags["exp"]) <= before + 601

    def test_accepts_npub_agent_key(self):
        from nostr_sdk import Keys

        from shc_toolkit.client import sign_operate_grant

        agent = Keys.generate()
        grant = sign_operate_grant(
            Keys.generate().secret_key().to_bech32(),
            service_id=1,
            agent_pubkey=agent.public_key().to_bech32(),
        )
        tags = {t[0]: t[1] for t in grant["tags"]}
        assert tags["d"] == f"shc:agent:{agent.public_key().to_hex()}"

    def test_signed_grant_round_trips_through_validator(self):
        from nostr_sdk import Keys

        from shc_toolkit.client import sign_operate_grant, validate_operate_grant

        agent = Keys.generate()
        grant = sign_operate_grant(
            Keys.generate().secret_key().to_bech32(),
            service_id=789,
            agent_pubkey=agent.public_key().to_hex(),
        )
        assert (
            validate_operate_grant(
                grant, expected_aud="shc:https://blesta.sovereignhybridcompute.com"
            )
            == []
        )


class TestFromOperateGrant:
    def test_returns_operating_client(self, monkeypatch):
        from nostr_sdk import Keys

        token = "e" * 64
        monkeypatch.setattr(
            "shc_toolkit.client.exchange_nostr_operate_grant",
            lambda grant, *, nsec, base_url="x": {
                "token": token, "scope": "operate", "area": "vm:42",
                "service_id": 42, "expires_in": 900,
            },
        )
        c = SHCClient.from_operate_grant(
            {"kind": 30078}, nsec=Keys.generate().secret_key().to_bech32()
        )
        assert isinstance(c, SHCClient)
        assert c.api_key == token

    def test_forwards_base_url_to_exchange(self, monkeypatch):
        seen = {}

        def fake_exchange(grant, *, nsec, base_url="x"):
            seen["base_url"] = base_url
            return {"token": "f" * 64}

        monkeypatch.setattr(
            "shc_toolkit.client.exchange_nostr_operate_grant", fake_exchange
        )
        SHCClient.from_operate_grant(
            {"kind": 30078}, nsec="nsec", base_url="https://alt.example/v2"
        )
        assert seen["base_url"] == "https://alt.example/v2"


class TestGrantOperateCLI:
    def test_prints_valid_grant_json(self, capsys, monkeypatch):
        import json as _json

        from nostr_sdk import Keys

        from shc_toolkit.cli import cmd_grant_operate

        customer = Keys.generate()
        agent = Keys.generate()
        monkeypatch.setattr(
            "shc_toolkit.register.load_context",
            lambda name: {"nsec": customer.secret_key().to_bech32()},
        )

        class Args:
            context = "default"
            service_id = 321
            agent_npub = agent.public_key().to_bech32()
            ttl = 300

        cmd_grant_operate(Args())
        grant = _json.loads(capsys.readouterr().out)
        assert grant["kind"] == 30078
        tags = {t[0]: t[1] for t in grant["tags"]}
        assert tags["area"] == "vm:321"
        assert tags["d"] == f"shc:agent:{agent.public_key().to_hex()}"
        assert int(tags["exp"]) - int(tags["nbf"]) == 300

    def test_exits_without_nsec(self, monkeypatch):
        import pytest as _pytest

        from shc_toolkit.cli import cmd_grant_operate

        monkeypatch.setattr("shc_toolkit.register.load_context", lambda name: None)

        class Args:
            context = "default"
            service_id = 1
            agent_npub = "npub1x"
            ttl = 900

        with _pytest.raises(SystemExit):
            cmd_grant_operate(Args())


class TestSelfDestruct:
    """VM-side self-destruct: minted full-scope key + systemd timer."""

    def _script(self, sid=42):
        from shc_toolkit.selfdestruct import selfdestruct_script

        return selfdestruct_script(sid, "https://blesta.sovereignhybridcompute.com/user-api/v2")

    def test_script_hits_cancel_with_confirm_dance(self):
        s = self._script()
        assert "SID = 42" in s
        assert "/cancel" in s
        assert '"immediate": True' in s
        assert "X-User-Api-Confirm" in s
        assert "confirmation_id" in s
        assert "Idempotency-Key" in s
        assert "IDEM" in s  # one constant shared by the original + confirm re-send

    def test_script_reads_key_from_file_not_env(self):
        s = self._script()
        assert "/etc/shc/self-destruct.key" in s
        assert "SHC_API_KEY" not in s and "environ" not in s

    def test_timer_fires_from_boot(self):
        from shc_toolkit.selfdestruct import selfdestruct_units

        units = selfdestruct_units(37)
        assert "OnBootSec=37min" in units["timer"]
        assert "shc-self-destruct.service" in units["timer"]
        assert "WantedBy=timers.target" in units["timer"]
        assert "python3 /usr/local/sbin/shc-self-destruct.py" in units["service"]

    def test_installer_is_base64_shebang_safe(self):
        from shc_toolkit.selfdestruct import build_installer

        installer = build_installer(
            service_id=7, minutes=5, key="shc_live_testkey", base_url="https://x/v2"
        )
        assert installer.startswith("echo ") and "base64 -d" in installer
        assert "shc_live_testkey" not in installer  # key only inside the b64 blob
        import base64

        blob = installer.split("echo ", 1)[1].split(" ", 1)[0]
        decoded = base64.b64decode(blob).decode()
        assert "/etc/shc/self-destruct.key" in decoded

    def test_mint_posts_basic_with_full_scope_1day(self, monkeypatch):
        import json as _json

        import httpx

        from shc_toolkit.selfdestruct import mint_suicide_key

        seen = {}

        def fake_request(_self, method, url=None, **kwargs):
            seen["method"] = method
            seen["url"] = url
            seen["json"] = kwargs.get("json")
            seen["auth"] = kwargs.get("auth")
            m = MagicMock()
            m.status_code = 200
            m.headers = {}
            m.text = _json.dumps({"data": {"api_key": "shc_live_minted"}})
            return m

        monkeypatch.setattr(httpx.Client, "request", fake_request)
        key = mint_suicide_key("a@b.c", "pw", 9, base_url="https://x/v2")
        assert key == "shc_live_minted"
        assert seen["url"] == "https://x/v2/account/api-keys"
        assert seen["json"] == {
            "name": "selfdestruct-9",
            "scope": "full",
            "expires_in_days": 1,
        }
        assert seen["auth"] == ("a@b.c", "pw")

    def test_arm_resolves_key_env_over_mint(self, monkeypatch):
        from shc_toolkit.selfdestruct import arm_self_destruct

        monkeypatch.setenv("SHC_SUICIDE_KEY", "shc_live_fromenv")
        ran = []

        arm_self_destruct(
            lambda cmd: ran.append(cmd) or "SELF_DESTRUCT_ARMED", 5, 30
        )
        assert len(ran) == 1 and "base64 -d" in ran[0]

    def test_arm_errors_without_any_key_source(self, monkeypatch):
        import pytest as _pytest

        from shc_toolkit.selfdestruct import arm_self_destruct

        monkeypatch.delenv("SHC_SUICIDE_KEY", raising=False)
        monkeypatch.delenv("SHC_ACCOUNT_EMAIL", raising=False)
        monkeypatch.delenv("SHC_ACCOUNT_PASSWORD", raising=False)
        with _pytest.raises(RuntimeError, match="SHC_SUICIDE_KEY"):
            arm_self_destruct(lambda cmd: "x", 5, 30)
