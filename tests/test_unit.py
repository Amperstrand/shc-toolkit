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

    def test_get_catalog_accepts_view(self):
        import inspect
        sig = inspect.signature(SHCClient.get_catalog)
        assert "view" in sig.parameters
        assert sig.parameters["view"].default == "full"


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
        assert len(TOOL_MAP) == 23

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
        catalog = {"items": [{"package_id": 81, "name": "Dev VPS"}]}
        client.session.post = MagicMock(return_value=_jsonrpc_result(catalog))
        result = client.get_catalog()
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


class TestCaching:
    def test_cache_get_returns_none_on_empty(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            assert c._cache_get("nothing") is None

    def test_cache_set_and_get(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("key1", {"data": 42})
            assert c._cache_get("key1") == {"data": 42}

    def test_cache_expires(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient(cache_ttl=0)
            c._cache_set("key1", "val")
            assert c._cache_get("key1") is None

    def test_invalidate_cache_all(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("a", 1)
            c._cache_set("b", 2)
            c.invalidate_cache()
            assert len(c._cache) == 0

    def test_invalidate_cache_prefix(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("credit", 1.0)
            c._cache_set("catalog:full", [])
            c.invalidate_cache("credit")
            assert "credit" not in c._cache
            assert "catalog:full" in c._cache


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
            c._cache_set("credit", 0.10)
            with pytest.raises(InsufficientCreditError):
                c.check_credit(0.50)

    def test_check_credit_passes_when_sufficient(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("credit", 5.00)
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
        assert pkg == 58  # SSD Pro is cheapest across all lines at 4c/16gb

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
    def _mock_catalog(self):
        return [{
            "package_id": 26,
            "name": "NVMe VPS - Standard",
            "cpu": 2, "memory_mb": 8192, "disk_gb": 16,
            "pricing": [{"pricing_id": 56, "period": "day", "price": "0.26"}],
            "available_config_options": [{
                "pricing_id": 56, "term": 1, "period": "day", "currency": "USD",
                "options": [
                    {"option_id": 110, "name": "ram", "label": "Total RAM",
                     "values": [
                        {"value": "8192", "name": "8 GB (Base)", "default": True},
                        {"value": "16384", "name": "16 GB", "default": False},
                     ]},
                    {"option_id": 111, "name": "cpu", "label": "vCPU Cores",
                     "values": [
                        {"value": "2", "name": "2 Cores (Base)", "default": True},
                        {"value": "4", "name": "4 Cores", "default": False},
                     ]},
                    {"option_id": 112, "name": "disk", "label": "Disk Space",
                     "values": [
                        {"value": "16", "name": "16 GB (Base)", "default": True},
                        {"value": "50", "name": "50 GB", "default": False},
                     ]},
                ],
            }],
        }]

    def test_get_config_options_returns_option_ids(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("catalog:full", self._mock_catalog())
            opts = c.get_config_options(26)
            assert opts["ram"]["option_id"] == 110
            assert opts["cpu"]["option_id"] == 111
            assert opts["disk"]["option_id"] == 112
            assert "16384" in opts["ram"]["values"]

    def test_get_config_options_empty_for_unknown_package(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("catalog:full", self._mock_catalog())
            assert c.get_config_options(999) == {}

    def test_resolve_addons_translates_specs(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("catalog:full", self._mock_catalog())
            result = c.resolve_addons(26, ram_mb=16384, cpu=4, disk_gb=50)
            assert result == {"110": "16384", "111": "4", "112": "50"}

    def test_resolve_addons_rejects_invalid_value(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("catalog:full", self._mock_catalog())
            with pytest.raises(ValueError, match="not available"):
                c.resolve_addons(26, ram_mb=999999)

    def test_resolve_addons_partial(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            c._cache_set("catalog:full", self._mock_catalog())
            result = c.resolve_addons(26, disk_gb=50)
            assert result == {"112": "50"}

    def test_resolve_addons_template(self):
        from shc_toolkit.client import SHCClient
        with patch.dict(os.environ, {"SHC_API_KEY": "shc_live_test"}):
            c = SHCClient()
            catalog = self._mock_catalog()
            catalog[0]["available_config_options"][0]["options"].append({
                "option_id": 126, "name": "template",
                "values": [{"value": "debian12-cloud", "name": "Debian 12"}],
            })
            c._cache_set("catalog:full", catalog)
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
            c._cache_set("credit", 100.0)
            c._cache_set("catalog:full", self._mock_catalog())
            c.submit_order = MagicMock(return_value={"invoice_id": 42})
            c.pay_invoice = MagicMock()
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
            c._cache_set("credit", 100.0)
            c._cache_set("catalog:full", self._mock_catalog())
            c.submit_order = MagicMock(return_value={"invoice_id": 42})
            c.pay_invoice = MagicMock()
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
            c = SHCClient()
        c._cache_set("catalog:full", [{
            "package_id": 26,
            "name": "NVMe VPS - Standard",
            "cpu": 2, "memory_mb": 8192, "disk_gb": 16,
            "pricing": [{"pricing_id": 56, "period": "day", "price": "0.49"}],
        }])
        return c

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
        c._cache_set("credit", 100.0)
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
