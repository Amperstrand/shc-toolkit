"""Provision ephemeral GitHub Actions runners on SHC VPSs.

MVP backend: full SHC VPS per job (order → wait → SSH bootstrap → runner
online → cancel after job).

Future backend: Firecracker microVM. The interface in this module
(``provision()`` / ``destroy()`` and the JSON it returns) is intentionally
backend-agnostic. The key cold-start metric we instrument is::

    t1 order/clone submitted  →  t5 runner online

For full VPS that is dominated by VM provisioning (~3–5 min on SHC).
For Firecracker the equivalent segment becomes microVM clone time,
which is the wedge we want to measure against. Do not rename these
timing keys without also updating the dogfood benchmark workflow and
``docs/github-ephemeral-runners.md``.

Reference bootstrap idiom: ``scripts/test-cloudinit-timing-hostkeys.py``
and ``shc_toolkit/bootstrap.py``.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .client import SHCClient, SHCError

# GitHub API constants
GITHUB_API = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"

# Polling defaults
DEFAULT_ORDER_TIMEOUT_S = 600       # VM provisioning
DEFAULT_ORDER_INTERVAL_S = 10
DEFAULT_SSH_TIMEOUT_S = 300         # SSH to come up after VM ready
DEFAULT_SSH_INTERVAL_S = 5
DEFAULT_RUNNER_ONLINE_TIMEOUT_S = 180  # runner to register after install
DEFAULT_RUNNER_ONLINE_INTERVAL_S = 5

# Cancellation idempotency: messages that mean "already gone, treat as success"
IDEMPOTENT_CANCEL_SUBSTRINGS = (
    "not found",
    "already cancel",
    "cancelled",
    "no active",
    "does not exist",
    "not active",
)


# ── Data classes ───────────────────────────────────────────────


@dataclass
class ProvisionRequest:
    """Inputs for a single ephemeral runner provision call."""

    repo: str                          # "owner/repo"
    github_token: str                  # PAT with repo admin / runners:write
    size: str = "dev-4c-16gb"
    template: str = "ubuntu2404-cloud"
    labels: list[str] = field(default_factory=list)
    runner_name: str | None = None
    ssh_public_key: str | None = None  # path or raw key
    ssh_private_key: str | None = None  # path (optional escape hatch)
    ssh_user: str | None = None        # auto-detected from VM if None
    max_wait_seconds: int = DEFAULT_ORDER_TIMEOUT_S
    install_docker: bool = True
    install_go: bool = False
    dry_run: bool = False


@dataclass
class ProvisionResult:
    """Machine-readable result of a provision call."""

    ok: bool
    service_id: int | None = None
    ip: str | None = None
    runner_name: str | None = None
    runner_label: str | None = None
    labels: list[str] = field(default_factory=list)
    backend: str = "shc-vps"
    backend_note: str = (
        "Full SHC VPS. Future backend may use Firecracker microVM "
        "to reduce cold-start."
    )
    created_at: str | None = None
    timings: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "service_id": self.service_id,
            "ip": self.ip,
            "runner_name": self.runner_name,
            "runner_label": self.runner_label,
            "labels": list(self.labels),
            "backend": self.backend,
            "backend_note": self.backend_note,
            "created_at": self.created_at,
            "timings": dict(self.timings),
            "error": self.error,
        }


# ── Pure helpers (unit-testable, no I/O) ───────────────────────


def parse_labels(raw: str | list[str] | None) -> list[str]:
    """Accept "a,b,c", ["a","b","c"], or None. Returns de-duplicated list."""
    if raw is None:
        return []
    if isinstance(raw, str):
        items = [s.strip() for s in raw.split(",")]
    else:
        items = [str(s).strip() for s in raw]
    seen: dict[str, None] = {}
    for item in items:
        if item and item not in seen:
            seen[item] = None
    return list(seen.keys())


def default_labels(runner_label: str) -> list[str]:
    """Labels attached to every SHC runner (per spec)."""
    return ["self-hosted", "linux", "x64", "shc", runner_label]


def is_idempotent_cancel_error(err: SHCError) -> bool:
    """Return True when ``err`` represents an already-canceled/not-found VM.

    The destroy command must be idempotent: re-running it on a VM that was
    already canceled (or never existed) must not fail. We match on the
    error code and message against a known set of phrases.
    """
    msg = (str(err) + " " + str(getattr(err, "code", ""))).lower()
    return any(sub in msg for sub in IDEMPOTENT_CANCEL_SUBSTRINGS)


def _iso_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _mark(timings: dict[str, Any], key: str) -> None:
    """Record an ISO timestamp + epoch seconds under ``key``."""
    timings[key] = {"iso": _iso_now(), "epoch": time.time()}


def _finalize_durations(timings: dict[str, Any]) -> None:
    """Compute ``durations`` (seconds) between consecutive t# markers."""
    keys = ["t0_started", "t1_order_submitted", "t2_vm_ready",
            "t3_ssh_reachable", "t4_runner_configured", "t5_runner_online",
            "t6_finished"]
    durations: dict[str, float] = {}
    for a, b in zip(keys, keys[1:]):
        if a in timings and b in timings:
            durations[f"{a}_to_{b}_s"] = round(
                timings[b]["epoch"] - timings[a]["epoch"], 2
            )
    # Convenience roll-ups used by the workflow summary
    if "t1_order_submitted" in timings and "t2_vm_ready" in timings:
        durations["order_to_ready_s"] = durations.get(
            "t1_order_submitted_to_t2_vm_ready_s", 0.0
        )
    if "t2_vm_ready" in timings and "t3_ssh_reachable" in timings:
        durations["ready_to_ssh_s"] = durations.get(
            "t2_vm_ready_to_t3_ssh_reachable_s", 0.0
        )
    if "t3_ssh_reachable" in timings and "t5_runner_online" in timings:
        durations["ssh_to_online_s"] = durations.get(
            "t3_ssh_reachable_to_t5_runner_online_s", 0.0
        )
    if "t0_started" in timings and "t6_finished" in timings:
        durations["total_s"] = round(
            timings["t6_finished"]["epoch"] - timings["t0_started"]["epoch"], 2
        )
    timings["durations"] = durations


# ── GitHub API ─────────────────────────────────────────────────


def _github_headers(github_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }


def _ssl_context() -> "ssl.SSLContext":
    """Return a TLS context that trusts system + certifi CAs.

    macOS Python from python.org does not always pick up the system trust
    store automatically; prefer certifi if installed, fall back to the
    default context (which still uses the OS trust on Linux/Windows).
    """
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def fetch_registration_token(repo: str, github_token: str) -> dict[str, str]:
    """Create a repo-level self-hosted runner registration token.

    POST /repos/{owner}/{repo}/actions/runners/registration-token

    Returns ``{"token": "...", "expires_at": "..."}``.

    Uses urllib from the stdlib so we add no new dependency.
    """
    import urllib.request
    import urllib.error

    url = f"{GITHUB_API}/repos/{repo}/actions/runners/registration-token"
    req = urllib.request.Request(
        url,
        method="POST",
        headers=_github_headers(github_token),
    )
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_context()) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(
            f"GitHub registration-token request failed: "
            f"HTTP {e.code} for {url}: {detail[:300]}"
        ) from e
    data = json.loads(body)
    if "token" not in data:
        raise RuntimeError(f"GitHub response missing 'token': {body[:300]}")
    return {"token": data["token"], "expires_at": data.get("expires_at", "")}


def fetch_runner_binary_url() -> str:
    """Return the download URL for the latest linux-x64 actions runner tarball.

    GET /repos/actions/runner/releases/latest → pick the
    ``actions-runner-linux-x64-*.tar.gz`` asset.
    """
    import urllib.request
    import urllib.error

    url = f"{GITHUB_API}/repos/actions/runner/releases/latest"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "User-Agent": "shc-toolkit",
        },
    )
    with urllib.request.urlopen(req, context=_ssl_context(), timeout=30) as resp:
        data = json.loads(resp.read().decode())
    for asset in data.get("assets", []):
        name = asset.get("name", "")
        if name.startswith("actions-runner-linux-x64-") and name.endswith(".tar.gz"):
            return asset["browser_download_url"]
    raise RuntimeError(
        f"No actions-runner-linux-x64-*.tar.gz asset in release "
        f"{data.get('tag_name', '?')}"
    )


def fetch_runners(repo: str, github_token: str) -> list[dict[str, Any]]:
    """List self-hosted runners for a repo. GET /repos/{o}/{r}/actions/runners."""
    import urllib.request

    url = f"{GITHUB_API}/repos/{repo}/actions/runners"
    req = urllib.request.Request(
        url, headers=_github_headers(github_token)
    )
    with urllib.request.urlopen(req, context=_ssl_context(), timeout=30) as resp:
        return json.loads(resp.read().decode()).get("runners", [])


def wait_runner_online(
    repo: str,
    github_token: str,
    runner_name: str,
    timeout: int = DEFAULT_RUNNER_ONLINE_TIMEOUT_S,
    interval: int = DEFAULT_RUNNER_ONLINE_INTERVAL_S,
) -> bool:
    """Poll the GitHub runners list until ``runner_name`` shows ``online``."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            for r in fetch_runners(repo, github_token):
                if r.get("name") == runner_name:
                    status = (r.get("status") or "").lower()
                    if status == "online":
                        return True
                    # If it's "offline" but was busy, it may already be
                    # ephemeral-removed after one job. Treat as online-ish
                    # because GitHub's status is eventually consistent here.
                    if status in ("offline", "queued"):
                        # Keep polling briefly
                        pass
        except Exception as e:  # noqa: BLE001
            # Transient API errors should not abort the wait
            print(f"  warn: runners list poll failed: {e}", file=sys.stderr)
        time.sleep(interval)
    return False


# ── SSH helpers (accept an identity file) ──────────────────────


def _ssh(
    host: str,
    cmd: str,
    *,
    user: str,
    identity: str | None,
    timeout: int = 60,
    port: int = 22,
) -> str:
    """Run a command on the VM via SSH using an optional identity file."""
    argv = [
        "ssh", "-p", str(port),
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "LogLevel=ERROR",
        "-o", "BatchMode=yes",
        "-o", f"ConnectTimeout={min(timeout, 15)}",
    ]
    if identity:
        argv += ["-i", identity]
    argv += [f"{user}@{host}", cmd]
    result = subprocess.run(
        argv, capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"SSH command failed (rc={result.returncode}): {cmd}\n"
            f"stderr: {result.stderr.strip()}\nstdout: {result.stdout.strip()}"
        )
    return result.stdout.strip()


def wait_ssh(
    host: str, *, user: str, identity: str | None,
    timeout: int = DEFAULT_SSH_TIMEOUT_S,
    interval: int = DEFAULT_SSH_INTERVAL_S,
) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            out = _ssh(host, "echo SSH_READY", user=user, identity=identity,
                       timeout=15)
            if "SSH_READY" in out:
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(interval)
    return False


# ── Bootstrap script ───────────────────────────────────────────


def _bootstrap_script(
    *,
    repo: str,
    token: str,
    runner_name: str,
    labels: list[str],
    runner_url: str,
    install_docker: bool,
    install_go: bool,
) -> str:
    """Render the bash script that installs + registers the runner.

    Designed for a single SSH invocation to minimize round-trips. Idempotent
    enough that re-running is safe (config.sh --replace handles re-register).
    """
    label_arg = ",".join(labels)
    docker_block = ""
    if install_docker:
        docker_block = '''if ! command -v docker >/dev/null 2>&1; then
  echo "[$(date -u +%FT%TZ)] installing docker"
  curl -fsSL https://get.docker.com | sudo sh || echo "warn: docker install failed (non-fatal)"
  sudo usermod -aG docker runner 2>/dev/null || true
fi
'''
    go_block = ""
    if install_go:
        go_block = '''if ! command -v go >/dev/null 2>&1; then
  echo "[$(date -u +%FT%TZ)] installing go"
  GO_VERSION=1.24.2
  curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" \\
    | sudo tar -C /usr/local -xz
  sudo ln -sf /usr/local/go/bin/go /usr/local/bin/go
fi
'''
    return f"""#!/usr/bin/env bash
set -euo pipefail

# t4 marker: bootstrap script start
echo "[$(date -u +%FT%TZ)] shc-bootstrap: start"

export DEBIAN_FRONTEND=noninteractive

# 1. Required packages
sudo apt-get update -y
sudo apt-get install -y curl tar jq git ca-certificates sudo

# 2. Docker (best-effort; many CI workflows need it)
{docker_block}
# 3. Go (optional, off by default)
{go_block}
# 4. runner user
if ! id runner >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash runner || true
  echo "runner ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/runner >/dev/null
fi

# 5. Download runner tarball
RUNNER_DIR=/home/runner/actions-runner
sudo -u runner mkdir -p "$RUNNER_DIR"

if [ ! -x "$RUNNER_DIR/run.sh" ]; then
  echo "[$(date -u +%FT%TZ)] downloading runner"
  sudo -u runner bash -c "cd '$RUNNER_DIR' && \\
    curl -fsSL -o runner.tar.gz '{runner_url}' && \\
    tar xzf runner.tar.gz && \\
    rm -f runner.tar.gz"
fi

# 6. Configure (idempotent via --replace)
echo "[$(date -u +%FT%TZ)] configuring runner"
sudo -u runner bash -c "cd '$RUNNER_DIR' && ./config.sh --unattended \\
  --url 'https://github.com/{repo}' \\
  --token '{token}' \\
  --name '{runner_name}' \\
  --labels '{label_arg}' \\
  --ephemeral \\
  --replace"

# 7. Install as root-owned systemd service that runs as runner
sudo tee /etc/systemd/system/github-actions-runner.service >/dev/null <<UNIT
[Unit]
Description=GitHub Actions Runner (SHC ephemeral)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=runner
WorkingDirectory=/home/runner/actions-runner
ExecStart=/home/runner/actions-runner/run.sh
Restart=on-failure
RestartSec=5
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable --now github-actions-runner.service

echo "[$(date -u +%FT%TZ)] shc-bootstrap: done"
echo "SHC_BOOTSTRAP_DONE_OK"
"""


# ── Top-level entry points ─────────────────────────────────────


def provision(req: ProvisionRequest, client: SHCClient | None = None) -> ProvisionResult:
    """Provision an ephemeral SHC GitHub Actions runner.

    See module docstring for the timing model and future Firecracker notes.
    """
    timings: dict[str, Any] = {}
    _mark(timings, "t0_started")

    runner_label = req.labels[0] if req.labels else f"shc-{uuid.uuid4().hex[:8]}"
    # Default labels are ALWAYS present (benchmark job's runs-on depends on them).
    # Caller-provided labels are appended and de-duplicated.
    all_labels = parse_labels(
        default_labels(runner_label) + parse_labels(req.labels)
    )
    runner_name = req.runner_name or f"shc-{uuid.uuid4().hex[:8]}"
    # service_id is tracked outside the try/except so the error path can still
    # report it for orphan cleanup when provisioning fails mid-flow.
    service_id: int | None = None

    # ── Dry-run path: plan only, no VM, no GitHub API call ──
    if req.dry_run:
        _mark(timings, "t6_finished")
        _finalize_durations(timings)
        return ProvisionResult(
            ok=True,
            runner_name=runner_name,
            runner_label=runner_label,
            labels=all_labels,
            created_at=_iso_now(),
            timings=timings,
        )

    if client is None:
        client = SHCClient()

    # Resolve SSH keys: prefer caller-supplied, else ephemeral keypair
    pub_key_str, identity_path, ephemeral_key_dir = _resolve_ssh_keys(
        req.ssh_public_key, req.ssh_private_key
    )

    try:
        # ── 1. GitHub registration token ──
        reg = fetch_registration_token(req.repo, req.github_token)
        runner_url = fetch_runner_binary_url()

        # ── 2. Order VM ──
        _mark(timings, "t1_order_submitted")
        hostname = f"shc-runner-{uuid.uuid4().hex[:6]}"
        order = client.order_vm(
            hostname=hostname,
            size=req.size,
            template=req.template,
            ssh_key=pub_key_str,
            pay=True,
            check_credit=True,
        )
        service_ids = order.get("service_ids") or (
            [order["service_id"]] if order.get("service_id") else []
        )
        if not service_ids:
            raise RuntimeError(f"order returned no service_id: {order}")
        service_id = int(service_ids[0])

        # ── 3. Wait for VM ready + IP ──
        vm = client.wait_for_provisioning(
            service_id, timeout=req.max_wait_seconds, interval=DEFAULT_ORDER_INTERVAL_S
        )
        _mark(timings, "t2_vm_ready")
        ips = vm.get("ips", [])
        if not ips:
            raise RuntimeError(f"VM {service_id} ready but has no IP")
        ip = ips[0]["ip"]
        ssh_user = req.ssh_user or vm.get("os_user", "debian")

        # Re-apply SSH key live in case cloud-init hasn't picked it up yet
        try:
            client.apply_ssh_key_live(service_id, pub_key_str)
        except Exception as e:  # noqa: BLE001
            print(f"  warn: apply_ssh_key_live failed (continuing): {e}",
                  file=sys.stderr)

        # ── 4. Wait for SSH ──
        if not wait_ssh(ip, user=ssh_user, identity=identity_path):
            raise RuntimeError(
                f"SSH not reachable on {ip} after {DEFAULT_SSH_TIMEOUT_S}s"
            )
        _mark(timings, "t3_ssh_reachable")

        # ── 5. Bootstrap runner ──
        script = _bootstrap_script(
            repo=req.repo,
            token=reg["token"],
            runner_name=runner_name,
            labels=all_labels,
            runner_url=runner_url,
            install_docker=req.install_docker,
            install_go=req.install_go,
        )
        out = _ssh(
            ip, script, user=ssh_user, identity=identity_path,
            timeout=600,
        )
        if "SHC_BOOTSTRAP_DONE_OK" not in out:
            raise RuntimeError(
                f"bootstrap script did not signal completion. output tail: "
                f"{out[-500:]}"
            )
        _mark(timings, "t4_runner_configured")

        # ── 6. Wait for runner to show online in GitHub ──
        online = wait_runner_online(
            req.repo, req.github_token, runner_name,
            timeout=DEFAULT_RUNNER_ONLINE_TIMEOUT_S,
        )
        if not online:
            # GitHub status is eventually-consistent; we warn but do not fail
            # because the runner may be functional even when status lags.
            print(
                f"  warn: runner '{runner_name}' not reported online within "
                f"{DEFAULT_RUNNER_ONLINE_TIMEOUT_S}s; benchmark job may queue",
                file=sys.stderr,
            )
        _mark(timings, "t5_runner_online")
        _mark(timings, "t6_finished")
        _finalize_durations(timings)

        return ProvisionResult(
            ok=True,
            service_id=service_id,
            ip=ip,
            runner_name=runner_name,
            runner_label=runner_label,
            labels=all_labels,
            created_at=_iso_now(),
            timings=timings,
        )

    except Exception as e:  # noqa: BLE001
        _mark(timings, "t6_finished")
        _finalize_durations(timings)
        return ProvisionResult(
            ok=False,
            service_id=service_id,
            runner_name=runner_name,
            runner_label=runner_label,
            labels=all_labels,
            created_at=_iso_now(),
            timings=timings,
            error=f"{type(e).__name__}: {e}",
        )


def destroy(service_id: int | None, client: SHCClient | None = None) -> dict[str, Any]:
    """Idempotently cancel/destroy an SHC VM by service_id.

    Returns a JSON-serializable dict. Returns success for already-canceled
    or not-found VMs. Only real cleanup failures return ``ok: False``.
    """
    if not service_id:
        return {
            "ok": True,
            "service_id": None,
            "action": "no-op",
            "message": "no service_id provided; nothing to destroy",
        }
    sid = int(service_id)
    if client is None:
        client = SHCClient()
    try:
        result = client.cancel_vm(sid, immediate=True)
        return {
            "ok": True,
            "service_id": sid,
            "action": "cancelled",
            "result": result,
        }
    except SHCError as e:
        if is_idempotent_cancel_error(e):
            return {
                "ok": True,
                "service_id": sid,
                "action": "already-cancelled",
                "message": str(e),
            }
        return {
            "ok": False,
            "service_id": sid,
            "action": "failed",
            "error": f"SHCError: {e}",
            "code": getattr(e, "code", None),
        }
    except Exception as e:  # noqa: BLE001
        return {
            "ok": False,
            "service_id": sid,
            "action": "failed",
            "error": f"{type(e).__name__}: {e}",
        }


# ── SSH key resolution ─────────────────────────────────────────


def _resolve_ssh_keys(
    public: str | None, private: str | None
) -> tuple[str, str | None, Path | None]:
    """Resolve SSH keypair: caller-supplied or ephemeral per-call keypair.

    Returns ``(public_key_str, identity_path_or_None, ephemeral_dir_or_None)``.
    The ephemeral dir is created with 0700 perms and owned by the current
    user; the caller is responsible for cleanup if it persists beyond the
    process (we let the OS reap ``/tmp``).
    """
    if public:
        # Accept path or raw key
        p = Path(public).expanduser()
        if p.exists():
            pub_str = p.read_text().strip()
        else:
            pub_str = public.strip()
        identity = None
        if private:
            identity = str(Path(private).expanduser())
        return pub_str, identity, None

    # Generate ephemeral keypair
    import tempfile
    ephemeral_dir = Path(tempfile.mkdtemp(prefix="shc-runner-key-"))
    ephemeral_dir.chmod(0o700)
    key_path = ephemeral_dir / "shc_runner_key"
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "",
         "-f", str(key_path), "-C", "shc-ephemeral-runner"],
        check=True, capture_output=True,
    )
    pub_str = (key_path.with_suffix(".pub")).read_text().strip()
    # Restrictive perms on the private key (ssh refuses world-readable keys)
    key_path.chmod(0o600)
    return pub_str, str(key_path), ephemeral_dir


__all__ = [
    "ProvisionRequest",
    "ProvisionResult",
    "provision",
    "destroy",
    "parse_labels",
    "default_labels",
    "is_idempotent_cancel_error",
    "fetch_registration_token",
    "fetch_runner_binary_url",
    "fetch_runners",
    "wait_runner_online",
    "wait_ssh",
]
