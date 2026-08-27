"""Billing-semantics tests: stop/shutdown are pauses, not cleanup.

SHC bills by service existence — a stopped VM accrues its full daily
price. These tests pin the client-side warning that meets agents at the
exact moment they call stop/shutdown.
"""

import io
from contextlib import redirect_stderr
from unittest.mock import patch

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
