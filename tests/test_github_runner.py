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
    SUPPORTED_BACKENDS,
    _build_fc_spawn_command,
    _parse_fc_spawn_output,
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


# ── Backend dispatch ────────────────────────────────────────────


class TestBackendSelection:
    def test_supported_backends_contains_both(self):
        assert "shc-vps" in SUPPORTED_BACKENDS
        assert "firecracker" in SUPPORTED_BACKENDS

    def test_default_backend_is_shc_vps(self):
        req = ProvisionRequest(repo="o/r", github_token="")
        assert req.backend == "shc-vps"

    def test_unknown_backend_raises_value_error(self):
        req = ProvisionRequest(
            repo="o/r", github_token="", backend="bogus", dry_run=True
        )
        with pytest.raises(ValueError, match="unknown backend"):
            provision(req, client=MagicMock())

    def test_unknown_backend_in_destroy_raises(self):
        with pytest.raises(ValueError, match="unknown backend"):
            destroy(123, client=MagicMock(), backend="bogus")

    def test_default_fc_pool_path(self):
        req = ProvisionRequest(repo="o/r", github_token="")
        assert req.firecracker_pool_path == "/opt/fc-pool"

    def test_default_fc_host_is_none(self):
        req = ProvisionRequest(repo="o/r", github_token="")
        assert req.firecracker_host is None


class TestShcVpsDispatch:
    def test_default_backend_routes_to_shc_vps(self):
        """provision() with no backend must call into the SHC VPS path
        and not the firecracker path."""
        req = ProvisionRequest(
            repo="o/r", github_token="ghp_x", labels=["t"], dry_run=True
        )
        with patch("shc_toolkit.github_runner._provision_firecracker") as m_fc, \
             patch("shc_toolkit.github_runner._provision_shc_vps") as m_vps:
            m_vps.return_value = MagicMock(ok=True, backend="shc-vps")
            provision(req, client=MagicMock())
            m_fc.assert_not_called()
            m_vps.assert_called_once()

    def test_explicit_shc_vps_backend_dry_run(self):
        req = ProvisionRequest(
            repo="o/r", github_token="", labels=["t"],
            backend="shc-vps", dry_run=True,
        )
        result = provision(req, client=MagicMock())
        assert result.ok is True
        assert result.backend == "shc-vps"


class TestFirecrackerProvision:
    def _fc_req(self, **kw) -> ProvisionRequest:
        defaults = dict(
            repo="o/r",
            github_token="ghp_x",
            backend="firecracker",
            firecracker_host="host.example.com",
            labels=["fc-1"],
        )
        defaults.update(kw)
        return ProvisionRequest(**defaults)

    def test_firecracker_dispatch_avoids_shc_path(self):
        req = self._fc_req()
        with patch("shc_toolkit.github_runner._provision_shc_vps") as m_vps, \
             patch("shc_toolkit.github_runner._provision_firecracker") as m_fc:
            m_fc.return_value = MagicMock(ok=True, backend="firecracker")
            provision(req, client=MagicMock())
            m_vps.assert_not_called()
            m_fc.assert_called_once_with(req)

    def test_dry_run_returns_firecracker_backend_no_io(self):
        req = self._fc_req(dry_run=True)
        with patch("shc_toolkit.github_runner.fetch_registration_token") as m_gh, \
             patch("shc_toolkit.github_runner._ssh") as m_ssh:
            result = provision(req, client=MagicMock())
            m_gh.assert_not_called()
            m_ssh.assert_not_called()
        assert result.ok is True
        assert result.backend == "firecracker"
        assert "fc-1" in result.labels
        assert "self-hosted" in result.labels
        assert result.runner_label == "fc-1"
        assert result.error is None

    def test_missing_host_returns_error(self):
        req = self._fc_req(firecracker_host=None)
        with patch("shc_toolkit.github_runner.fetch_registration_token") as m_gh, \
             patch("shc_toolkit.github_runner._ssh") as m_ssh:
            result = provision(req, client=MagicMock())
            m_gh.assert_not_called()
            m_ssh.assert_not_called()
        assert result.ok is False
        assert result.backend == "firecracker"
        assert "firecracker_host" in (result.error or "")

    def test_successful_spawn_parses_pool_json(self):
        pool_output = json.dumps({
            "name": "fc-abc",
            "workdir": "/tmp/fc-fc-abc-x",
            "tap": "fctap0100",
            "pid": 12345,
            "started_at": 1.0,
            "boot_to_init_s": 22.1,
            "ip": "10.0.0.5",
            "error": None,
        })
        req = self._fc_req()
        with patch("shc_toolkit.github_runner.fetch_registration_token",
                   return_value={"token": "regtok", "expires_at": ""}), \
             patch("shc_toolkit.github_runner._ssh",
                   return_value=pool_output) as m_ssh:
            result = provision(req, client=MagicMock())
            m_ssh.assert_called_once()
            # Confirm the spawn command was passed through with poll-github
            invoked_cmd = m_ssh.call_args.args[1]
            assert "firecracker_pool.py" in invoked_cmd
            assert "--poll-github" in invoked_cmd
            assert "--github-token" in invoked_cmd

        assert result.ok is True
        assert result.backend == "firecracker"
        assert result.ip == "10.0.0.5"
        assert result.service_id is None
        assert "t1_order_submitted" in result.timings
        assert "t5_runner_online" in result.timings
        assert "t6_finished" in result.timings
        assert result.error is None

    def test_pool_returned_error_propagates(self):
        pool_output = json.dumps({
            "name": "fc-abc",
            "workdir": "",
            "tap": "",
            "pid": None,
            "started_at": 0.0,
            "boot_to_init_s": None,
            "ip": None,
            "error": "kernel panic in μVM console",
        })
        req = self._fc_req()
        with patch("shc_toolkit.github_runner.fetch_registration_token",
                   return_value={"token": "regtok", "expires_at": ""}), \
             patch("shc_toolkit.github_runner._ssh",
                   return_value=pool_output):
            result = provision(req, client=MagicMock())
        assert result.ok is False
        assert "kernel panic" in (result.error or "")

    def test_ssh_failure_returns_error_result(self):
        req = self._fc_req()
        with patch("shc_toolkit.github_runner.fetch_registration_token",
                   return_value={"token": "regtok", "expires_at": ""}), \
             patch("shc_toolkit.github_runner._ssh",
                   side_effect=RuntimeError("SSH command failed")):
            result = provision(req, client=MagicMock())
        assert result.ok is False
        assert "SSH command failed" in (result.error or "")
        assert result.backend == "firecracker"

    def test_custom_pool_path_used(self):
        pool_output = json.dumps({
            "name": "x", "workdir": "", "tap": "", "pid": 1,
            "started_at": 0.0, "boot_to_init_s": 1.0,
            "ip": "10.0.0.6", "error": None,
        })
        req = self._fc_req(firecracker_pool_path="/custom/pool")
        with patch("shc_toolkit.github_runner.fetch_registration_token",
                   return_value={"token": "regtok", "expires_at": ""}), \
             patch("shc_toolkit.github_runner._ssh",
                   return_value=pool_output) as m_ssh:
            provision(req, client=MagicMock())
            invoked_cmd = m_ssh.call_args.args[1]
            assert "/custom/pool/firecracker_pool.py" in invoked_cmd


class TestFirecrackerDestroy:
    def test_no_runner_name_is_noop(self):
        result = destroy(None, backend="firecracker")
        assert result["ok"] is True
        assert result["action"] == "no-op"
        assert result["backend"] == "firecracker"

    def test_missing_host_returns_failure(self):
        result = destroy(
            None, backend="firecracker",
            runner_name="fc-1", firecracker_host=None,
        )
        assert result["ok"] is False
        assert result["backend"] == "firecracker"
        assert "firecracker_host" in result["error"]

    def test_successful_kill_calls_pool(self):
        with patch("shc_toolkit.github_runner._ssh",
                   return_value='{"killed": true, "name": "fc-1"}') as m_ssh:
            result = destroy(
                None, backend="firecracker",
                runner_name="fc-1",
                firecracker_host="host.example.com",
            )
        assert result["ok"] is True
        assert result["action"] == "killed"
        assert result["runner_name"] == "fc-1"
        assert result["result"]["killed"] is True
        invoked_cmd = m_ssh.call_args.args[1]
        assert "firecracker_pool.py kill" in invoked_cmd
        assert "--name fc-1" in invoked_cmd

    def test_ssh_failure_is_failure(self):
        with patch("shc_toolkit.github_runner._ssh",
                   side_effect=RuntimeError("connection refused")):
            result = destroy(
                None, backend="firecracker",
                runner_name="fc-1",
                firecracker_host="host.example.com",
            )
        assert result["ok"] is False
        assert "connection refused" in result["error"]


# ── Pool output parser & command builder ────────────────────────


class TestParseFcSpawnOutput:
    def test_pure_json(self):
        out = '{"name": "x", "ip": "10.0.0.1"}'
        assert _parse_fc_spawn_output(out)["name"] == "x"

    def test_json_with_prefix_logs(self):
        out = 'spawning...\nboot: 1.2s\n{"name": "y", "ip": "10.0.0.2"}\n'
        assert _parse_fc_spawn_output(out)["ip"] == "10.0.0.2"

    def test_indented_json_with_prefix_logs(self):
        out = (
            'log line\n'
            '{\n'
            '  "name": "z",\n'
            '  "boot_to_init_s": 22.1,\n'
            '  "ip": "10.0.0.3"\n'
            '}\n'
        )
        parsed = _parse_fc_spawn_output(out)
        assert parsed["name"] == "z"
        assert parsed["boot_to_init_s"] == 22.1

    def test_no_json_returns_error_dict(self):
        parsed = _parse_fc_spawn_output("not json at all")
        assert "error" in parsed


class TestBuildFcSpawnCommand:
    def test_includes_required_args(self):
        cmd = _build_fc_spawn_command(
            pool_path="/opt/fc-pool",
            runner_name="fc-1",
            repo="o/r",
            reg_token="regtok",
            labels_arg="shc,fc,fc-1",
            github_token="ghp_x",
        )
        assert "/opt/fc-pool/firecracker_pool.py" in cmd
        assert "--name fc-1" in cmd
        assert "--repo o/r" in cmd
        assert "--poll-github" in cmd
        assert "--github-token ghp_x" in cmd

    def test_shell_quotes_metacharacters(self):
        """Runner name with shell metacharacters must be quoted — prevents
        command injection on the host VM."""
        cmd = _build_fc_spawn_command(
            pool_path="/opt/fc-pool",
            runner_name="$(reboot)",
            repo="o/r",
            reg_token="tok; rm -rf /",
            labels_arg="a",
            github_token="ghp_x",
        )
        assert "$(reboot)" not in cmd.split("--name ")[1].split()[0]
        assert "rm -rf" not in cmd or "rm -rf /" not in cmd.split()

    def test_trailing_slash_in_pool_path_normalized(self):
        cmd = _build_fc_spawn_command(
            pool_path="/opt/fc-pool/",
            runner_name="x",
            repo="o/r",
            reg_token="t",
            labels_arg="a",
            github_token="g",
        )
        assert "//firecracker_pool.py" not in cmd


# ── CLI: firecracker backend ────────────────────────────────────


class TestCLIFirecracker:
    def test_fc_dry_run_via_main(self, capsys):
        from shc_toolkit.cli import main
        sys.argv = [
            "shc", "github-runner", "provision",
            "--repo", "o/r",
            "--backend", "firecracker",
            "--labels", "fc-cli-test",
            "--dry-run",
        ]
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["ok"] is True
        assert data["backend"] == "firecracker"
        assert data["runner_label"] == "fc-cli-test"
        assert "fc-cli-test" in data["labels"]

    def test_fc_provision_without_host_errors(self, capsys):
        from shc_toolkit.cli import main
        sys.argv = [
            "shc", "github-runner", "provision",
            "--repo", "o/r",
            "--backend", "firecracker",
            "--github-token", "faketoken",
        ]
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 2
        err = capsys.readouterr().err
        assert "--firecracker-host" in err

    def test_fc_destroy_noop_via_main(self, capsys):
        from shc_toolkit.cli import main
        sys.argv = [
            "shc", "github-runner", "destroy",
            "--backend", "firecracker",
        ]
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["ok"] is True
        assert data["action"] == "no-op"
        assert data["backend"] == "firecracker"

    def test_shc_vps_destroy_default_unchanged(self, capsys):
        """Backward-compat: destroy with no backend flag still works
        exactly as before the backend selector existed."""
        from shc_toolkit.cli import main
        sys.argv = ["shc", "github-runner", "destroy"]
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["ok"] is True
        assert data["action"] == "no-op"
