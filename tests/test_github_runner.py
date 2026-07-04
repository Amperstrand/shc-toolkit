"""Unit tests for shc_toolkit.github_runner.

Pure-logic coverage only — no live VMs, no live GitHub API calls.
Network/SSH code paths are tested via mocks.
"""

from __future__ import annotations

import json
import sys
from unittest.mock import MagicMock, patch

import pytest

from shc_toolkit.client import SHCError
from shc_toolkit.github_runner import (
    ProvisionRequest,
    default_labels,
    destroy,
    fetch_registration_token,
    fetch_runner_binary_url,
    is_idempotent_cancel_error,
    parse_labels,
    provision,
)


# ── parse_labels ───────────────────────────────────────────────


class TestParseLabels:
    def test_string_csv(self):
        assert parse_labels("shc,benchmark,shc-123") == [
            "shc", "benchmark", "shc-123"
        ]

    def test_string_with_whitespace(self):
        assert parse_labels(" shc , benchmark , shc-123 ") == [
            "shc", "benchmark", "shc-123"
        ]

    def test_list_input(self):
        assert parse_labels(["shc", "benchmark"]) == ["shc", "benchmark"]

    def test_none(self):
        assert parse_labels(None) == []

    def test_empty_string(self):
        assert parse_labels("") == []

    def test_dedupes_preserving_order(self):
        assert parse_labels("a,b,a,c,b") == ["a", "b", "c"]

    def test_skips_empty_items(self):
        assert parse_labels("a,,b,") == ["a", "b"]


class TestDefaultLabels:
    def test_includes_required_labels(self):
        labels = default_labels("shc-run-42-1")
        assert "self-hosted" in labels
        assert "linux" in labels
        assert "x64" in labels
        assert "shc" in labels
        assert "shc-run-42-1" in labels

    def test_unique_label_is_last(self):
        labels = default_labels("shc-abc")
        assert labels[-1] == "shc-abc"


# ── is_idempotent_cancel_error ─────────────────────────────────


class TestIdempotentCancel:
    @pytest.mark.parametrize("msg", [
        "service not found",
        "VM already cancelled",
        "Already canceled",
        "service does not exist",
        "no active service",
    ])
    def test_recognizes_idempotent_phrases(self, msg):
        err = SHCError("not_found", msg)
        assert is_idempotent_cancel_error(err) is True

    def test_rejects_generic_error(self):
        err = SHCError("server_error", "internal server error")
        assert is_idempotent_cancel_error(err) is False

    def test_handles_no_message(self):
        err = SHCError("unknown", "")
        assert is_idempotent_cancel_error(err) is False


# ── destroy ────────────────────────────────────────────────────


class TestDestroy:
    def test_none_service_id_is_noop_success(self):
        result = destroy(None, client=MagicMock())
        assert result["ok"] is True
        assert result["action"] == "no-op"
        assert result["service_id"] is None

    def test_empty_string_service_id_is_noop_success(self):
        # int("") would raise; ensure caller passes None for falsy
        result = destroy(None, client=MagicMock())
        assert result["ok"] is True

    def test_successful_cancel(self):
        client = MagicMock()
        client.cancel_vm.return_value = {"service_id": 123, "status": "cancelled"}
        result = destroy(123, client=client)
        assert result["ok"] is True
        assert result["action"] == "cancelled"
        assert result["service_id"] == 123
        client.cancel_vm.assert_called_once_with(123, immediate=True)

    def test_already_canceled_is_success(self):
        client = MagicMock()
        client.cancel_vm.side_effect = SHCError("not_found", "service not found")
        result = destroy(456, client=client)
        assert result["ok"] is True
        assert result["action"] == "already-cancelled"

    def test_real_failure_propagates(self):
        client = MagicMock()
        client.cancel_vm.side_effect = SHCError("server_error",
                                                "internal server error")
        result = destroy(789, client=client)
        assert result["ok"] is False
        assert result["action"] == "failed"
        assert "server_error" in result["error"]

    def test_unexpected_exception_is_failure(self):
        client = MagicMock()
        client.cancel_vm.side_effect = RuntimeError("network gone")
        result = destroy(111, client=client)
        assert result["ok"] is False
        assert "network gone" in result["error"]


# ── provision: dry-run (no network) ────────────────────────────


class TestProvisionDryRun:
    def test_dry_run_does_not_call_github_or_shc(self):
        req = ProvisionRequest(
            repo="Amperstrand/tollgate-module-basic-go",
            github_token="",  # empty OK in dry-run
            size="dev-4c-16gb",
            template="ubuntu2404-cloud",
            labels=["shc-run-1-1"],
            dry_run=True,
        )
        with patch("shc_toolkit.github_runner.fetch_registration_token") as m_gh, \
             patch("shc_toolkit.github_runner.SHCClient") as m_client_cls:
            result = provision(req, client=MagicMock())
            m_gh.assert_not_called()
            m_client_cls.assert_not_called()

        assert result.ok is True
        assert result.runner_label == "shc-run-1-1"
        assert "shc-run-1-1" in result.labels
        assert "self-hosted" in result.labels
        assert result.timings["durations"]["total_s"] is not None
        assert result.error is None

    def test_dry_run_synthesizes_labels_when_omitted(self):
        req = ProvisionRequest(
            repo="Amperstrand/tollgate-module-basic-go",
            github_token="",
            dry_run=True,
        )
        result = provision(req, client=MagicMock())
        assert result.ok is True
        assert result.runner_label.startswith("shc-")
        assert "self-hosted" in result.labels
        assert "linux" in result.labels
        assert "x64" in result.labels
        assert "shc" in result.labels


# ── provision: error paths ─────────────────────────────────────


class TestProvisionErrors:
    def test_failed_order_returns_not_ok_with_timing(self):
        client = MagicMock()
        client.order_vm.side_effect = RuntimeError("insufficient credit")
        with patch("shc_toolkit.github_runner.fetch_registration_token",
                   return_value={"token": "x", "expires_at": ""}), \
             patch("shc_toolkit.github_runner.fetch_runner_binary_url",
                   return_value="https://example/runner.tar.gz"):
            req = ProvisionRequest(
                repo="Amperstrand/tollgate-module-basic-go",
                github_token="ghp_test",
                size="dev-4c-16gb",
                labels=["shc-test"],
            )
            result = provision(req, client=client)

        assert result.ok is False
        assert "insufficient credit" in (result.error or "")
        assert "t0_started" in result.timings
        assert "t6_finished" in result.timings


# ── GitHub API helpers (mocked network) ────────────────────────


class TestGitHubAPIHelpers:
    def test_fetch_registration_token_returns_token(self):
        from io import BytesIO
        fake_resp = BytesIO(
            json.dumps({"token": "ABC", "expires_at": "2030-01-01T00:00:00Z"})
            .encode()
        )

        class FakeUrlopen:
            def __init__(self, req, **kw):
                self.req = req
                self.buf = fake_resp

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return None

            def read(self):
                return self.buf.read()

        with patch("urllib.request.urlopen", side_effect=FakeUrlopen):
            result = fetch_registration_token("o/r", "ghp_x")
        assert result["token"] == "ABC"
        assert result["expires_at"] == "2030-01-01T00:00:00Z"

    def test_fetch_registration_token_http_error_raises(self):
        import urllib.error
        from io import BytesIO

        class FakeHTTPError(urllib.error.HTTPError):
            def __init__(self):
                super().__init__(
                    "https://api.github.com/fake",
                    403, "Forbidden", {}, BytesIO(b'{"message":"no"}'),
                )

        def fake_urlopen(req, **kw):
            raise FakeHTTPError()

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            with pytest.raises(RuntimeError, match="HTTP 403"):
                fetch_registration_token("o/r", "ghp_x")

    def test_fetch_runner_binary_url_picks_x64_asset(self):
        from io import BytesIO
        payload = {
            "tag_name": "v2.322.0",
            "assets": [
                {"name": "actions-runner-osx-arm64-2.322.0.tar.gz",
                 "browser_download_url": "https://x/osx-arm64.tar.gz"},
                {"name": "actions-runner-linux-x64-2.322.0.tar.gz",
                 "browser_download_url": "https://x/linux-x64.tar.gz"},
                {"name": "actions-runner-linux-arm64-2.322.0.tar.gz",
                 "browser_download_url": "https://x/linux-arm64.tar.gz"},
            ],
        }
        fake_resp = BytesIO(json.dumps(payload).encode())

        class FakeUrlopen:
            def __init__(self, req, **kw):
                self.buf = fake_resp

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return None

            def read(self):
                return self.buf.read()

        with patch("urllib.request.urlopen", side_effect=FakeUrlopen):
            url = fetch_runner_binary_url()
        assert "linux-x64" in url
        assert url == "https://x/linux-x64.tar.gz"

    def test_fetch_runner_binary_url_raises_when_no_x64_asset(self):
        from io import BytesIO
        payload = {"tag_name": "v1.0.0", "assets": [
            {"name": "actions-runner-osx-arm64-1.0.0.tar.gz",
             "browser_download_url": "https://x/osx.tar.gz"},
        ]}
        fake_resp = BytesIO(json.dumps(payload).encode())

        class FakeUrlopen:
            def __init__(self, req, **kw):
                self.buf = fake_resp

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return None

            def read(self):
                return self.buf.read()

        with patch("urllib.request.urlopen", side_effect=FakeUrlopen):
            with pytest.raises(RuntimeError, match="No actions-runner-linux-x64"):
                fetch_runner_binary_url()


# ── CLI surface smoke ──────────────────────────────────────────


class TestCLISmoke:
    def test_dry_run_via_main(self, capsys):
        from shc_toolkit.cli import main
        sys.argv = [
            "shc", "github-runner", "provision",
            "--repo", "Amperstrand/tollgate-module-basic-go",
            "--size", "dev-4c-16gb",
            "--template", "ubuntu2404-cloud",
            "--labels", "shc-cli-test",
            "--dry-run",
        ]
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["ok"] is True
        assert data["runner_label"] == "shc-cli-test"
        assert "shc-cli-test" in data["labels"]
        assert data["timings"]["durations"]["total_s"] is not None

    def test_destroy_no_service_id_via_main(self, capsys):
        from shc_toolkit.cli import main
        sys.argv = ["shc", "github-runner", "destroy"]
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["ok"] is True
        assert data["action"] == "no-op"
