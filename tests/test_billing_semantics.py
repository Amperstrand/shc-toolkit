"""Billing-semantics tests: stop/shutdown are pauses, not cleanup.

SHC bills by service existence — a stopped VM accrues its full daily
price. These tests pin the client-side warning that meets agents at the
exact moment they call stop/shutdown, plus the list/info visibility that
makes stopped-but-billable zombies visible at a glance (issue #38).
"""

import io
from contextlib import redirect_stderr, redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from shc_toolkit import cli
from shc_toolkit.client import SHCClient


class TestStopWarning:
    def _stderr_of(self, fn) -> str:
        buf = io.StringIO()
        with redirect_stderr(buf):
            fn()
        return buf.getvalue()

    def test_stop_vm_warns(self):
        c = SHCClient(api_key="test-key")
        with patch.object(SHCClient, "_patch", return_value={"ok": True}):
            err = self._stderr_of(lambda: c.stop_vm(42))
        assert "still bills while stopped" in err
        assert "cancel" in err

    def test_shutdown_vm_warns(self):
        c = SHCClient(api_key="test-key")
        with patch.object(SHCClient, "_patch", return_value={"ok": True}):
            err = self._stderr_of(lambda: c.shutdown_vm(42))
        assert "still bills while stopped" in err

    def test_cancel_vm_does_not_warn(self):
        c = SHCClient(api_key="test-key")
        with patch.object(SHCClient, "cancel_vm", return_value={"ok": True}):
            err = self._stderr_of(lambda: c.cancel_vm(42, immediate=True))
        assert "still bills" not in err


def _text_args(**extra) -> SimpleNamespace:
    base = {"format": "table", "api_key": "test-key", "context": None, "profile": None}
    base.update(extra)
    return SimpleNamespace(**base)


class TestListBillingVisibility:
    def _run_list(self, vms, summaries=None) -> str:
        buf = io.StringIO()
        with (
            patch.object(SHCClient, "list_vms", return_value=vms),
            patch.object(SHCClient, "get_vm_summary", side_effect=summaries or []),
            redirect_stdout(buf),
        ):
            cli.cmd_list(_text_args())
        return buf.getvalue()

    def test_stopped_vm_marked_still_billing(self):
        vms = [
            {"id": 1, "hostname": "zombie", "service_status": "active", "ips": []},
            {"id": 2, "hostname": "alive", "service_status": "active", "ips": []},
        ]
        summaries = [
            {"runtime": {"raw_status": "stopped"}},
            {"runtime": {"raw_status": "running"}},
        ]
        out = self._run_list(vms, summaries)
        assert "zombie" in out
        assert "STILL BILLING" in out
        assert (
            out.count("← STILL BILLING") == 1
        )  # row marker only (footer also mentions it)
        assert "1 stopped VM(s) STILL BILLING" in out
        assert "billing stops only at cancel" in out

    def test_footer_counts_all_billable(self):
        vms = [
            {"id": 1, "hostname": "a", "service_status": "active", "ips": []},
            {"id": 2, "hostname": "b", "service_status": "active", "ips": []},
            {"id": 3, "hostname": "c", "service_status": "canceled", "ips": []},
        ]
        summaries = [
            {"runtime": {"raw_status": "running"}},
            {"runtime": {"state": "shutdown"}},
        ]
        out = self._run_list(vms, summaries)
        assert "2 of 3 VMs accruing charges" in out
        assert "1 stopped VM(s) STILL BILLING" in out
        assert "shc cancel" in out

    def test_runtime_probe_failure_is_soft(self):
        vms = [{"id": 1, "hostname": "x", "service_status": "active", "ips": []}]
        out = self._run_list(vms, summaries=[RuntimeError("boom")])
        assert "STILL BILLING" not in out
        assert "1 of 1 VMs accruing charges" in out

    def test_shutdown_keyword_also_flags(self):
        vms = [{"id": 1, "hostname": "s", "service_status": "active", "ips": []}]
        out = self._run_list(vms, [{"runtime": {"state": "Shutdown"}}])
        assert "STILL BILLING" in out

    def test_json_format_skips_probes(self):
        buf = io.StringIO()
        vms = [{"id": 1, "hostname": "x", "service_status": "active", "ips": []}]
        with (
            patch.object(SHCClient, "list_vms", return_value=vms) as m_list,
            patch.object(SHCClient, "get_vm_summary") as m_sum,
            redirect_stdout(buf),
        ):
            cli.cmd_list(_text_args(format="json"))
        assert m_list.called
        assert not m_sum.called  # machine output: no per-VM enrichment


class TestInfoCostBlock:
    def _run_info(self, summary) -> str:
        buf = io.StringIO()
        with (
            patch.object(SHCClient, "get_vm_summary", return_value=summary),
            redirect_stdout(buf),
        ):
            cli.cmd_info(_text_args(service_id=7))
        return buf.getvalue()

    def test_cost_block_rendered_with_pricing(self):
        summary = {
            "id": 7,
            "hostname": "h",
            "date_created": "2026-08-24T00:00:00Z",
            "pricing": {"price": "0.24", "currency": "USD", "period": "day"},
        }
        out = self._run_info(summary)
        assert "billing:" in out
        assert "0.24 USD/day" in out
        assert "FULL rate while stopped" in out
        assert "estimate" in out
        assert "shc cancel <id>" in out

    def test_no_cost_block_without_pricing(self):
        out = self._run_info({"id": 7, "hostname": "h"})
        assert "billing:" not in out

    def test_bad_price_string_is_skipped(self):
        summary = {"id": 7, "pricing": {"price": "free-ish"}}
        out = self._run_info(summary)
        assert "billing:" not in out
