"""Regression test for the console screenshot temp-file hardening.

Bandit B306 (pre-existing on main, reintroduced by the console
productization commit d8bbf23): tempfile.mktemp() only GENERATES a
predictable-ish name without creating the file — a symlink/TOCTOU vector
in shared /tmp, the same class as the cloudflared /tmp finding on PR #33.
mkstemp() creates the file atomically 0600.
"""

import os
import stat
import types

from shc_toolkit import console_client


def test_console_command_uses_mkstemp_screenshots(monkeypatch):
    fake_shot = types.SimpleNamespace(save=lambda path: open(path, "wb").write(b"png"))

    class FakeVNC:
        keyboard = types.SimpleNamespace(press=lambda *a: None, write=lambda *a: None)
        video = types.SimpleNamespace(refresh=lambda: None, get_frame=lambda: fake_shot)

        async def screenshot(self):
            return fake_shot

    class FakeCtx:
        async def __aenter__(self):
            return FakeVNC()

        async def __aexit__(self, *a):
            return None

    async def fake_open(*a, **kw):
        return FakeCtx()

    monkeypatch.setattr(console_client, "open_console", fake_open)
    pre, post = console_client.console_command(None, 1077, "uptime", settle=0)

    for p in (pre, post):
        assert os.path.exists(p), f"screenshot {p} must exist (mkstemp creates it)"
        mode = stat.S_IMODE(os.stat(p).st_mode)
        assert mode == 0o600, f"screenshot {p} must be 0600, got {oct(mode)}"
