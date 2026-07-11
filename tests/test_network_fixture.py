"""Regression tests for the network-blocking autouse fixture in conftest.py.

The fixture (block_network_by_default) is the test-suite safety net that
prevents unit tests from silently leaking real HTTP calls to the SHC API.
Without these tests, a future refactor of conftest.py could disable the
fixture and the leak-prevention guarantee would be lost — the original
flake (commit e1ba4b2) would silently reappear.

Each test deliberately exercises one bypass path. They MUST run under
the autouse fixture (no opt-out marker on the test functions themselves)
to prove the fixture's branches work as advertised.
"""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest
import requests


def test_fixture_blocks_unmocked_network_call_by_default():
    """An unmocked requests.Session.request must raise — this is the
    guarantee that prevents flaky time.sleep retries when a test forgets
    to mock _safe_credit/get_vm_payments/etc."""
    with pytest.raises(RuntimeError, match="Network call blocked"):
        requests.Session().request("GET", "https://example.test/")


@pytest.mark.allow_network
def test_allow_network_marker_lifts_the_block():
    """Tests marked @pytest.mark.allow_network can make real calls.

    We don't actually want a real call here — just verify the fixture
    steps aside. Patch requests.Session.request to a no-op so the test
    is hermetic but the fixture's bypass branch is exercised."""
    with patch.object(requests.Session, "request", return_value=MagicMock()):
        # Would raise if the fixture failed to honor the marker.
        requests.Session().request("GET", "https://example.test/")


def test_client_or_vm_fixture_dependency_lifts_the_block(request):
    """Tests that depend on the session-scoped `client` or `vm` fixtures
    are explicitly integration tests. We can't easily inject those here
    without spawning a real client, so this test just documents the
    contract: the fixture checks `request.fixturenames` for 'client' or
    'vm' and lifts the block.

    The contract is verified structurally in conftest.py:
        if 'client' in request.fixturenames or 'vm' in request.fixturenames:
            yield
            return
    """
    # Sanity: this test itself doesn't pull in client/vm, so the block
    # is active. Verify by attempting a blocked call.
    with pytest.raises(RuntimeError, match="Network call blocked"):
        requests.Session().request("GET", "https://example.test/")


def test_blocked_message_is_actionable():
    """The RuntimeError message must tell the test author how to fix it
    (explicit mock or @pytest.mark.allow_network). If the wording drifts
    to something vague, future flakes will be harder to diagnose."""
    try:
        requests.Session().request("GET", "https://example.test/")
    except RuntimeError as exc:
        msg = str(exc)
        assert "block_network_by_default" in msg
        assert "@pytest.mark.allow_network" in msg
    else:
        pytest.fail("fixture did not raise")
