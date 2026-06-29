"""Unit tests for shc_toolkit — no live API required.

Tests the transport abstraction, factory selection, MCP JSON-RPC protocol
layer, confirmation flow, and client bug fixes using mocks.
"""

from __future__ import annotations

import json
import os
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
