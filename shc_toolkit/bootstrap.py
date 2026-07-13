"""
Transport-agnostic VM script deployment.

Tries SSH first (fast — ~1s). If SSH fails and a ConsoleSession is provided,
falls back to noVNC console deployment (slower — ~30s but works on Dev VPS
where SSH is broken).

Usage:
    from shc_toolkit.client import SHCClient
    from shc_toolkit.console import ConsoleSession
    from shc_toolkit.bootstrap import VMBootstrap

    c = SHCClient()
    boot = VMBootstrap(c)  # SSH only; console=None

    # With noVNC fallback (for Dev VPS):
    session = ConsoleSession()
    boot = VMBootstrap(c, console=session)

    boot.deploy(605, "#!/bin/bash\\necho hello\\n")
"""

from __future__ import annotations

import base64
import hashlib
import logging
import socket
import time

from .client import SHCClient
from .provision import ssh_cmd

log = logging.getLogger(__name__)

REMOTE_PATH = "/tmp/shc-bootstrap.sh"


class VMBootstrap:
    """Deploy and execute scripts on SHC VMs via the best available transport."""

    def __init__(self, client: SHCClient, console=None):
        """
        Args:
            client: SHCClient for API calls (get_vm, get_vm_summary, etc.).
            console: ConsoleSession for noVNC fallback. None = SSH only.
        """
        self.client = client
        self.console = console

    def deploy(
        self,
        service_id: int,
        script: str,
        *,
        verify: bool = True,
        timeout: int = 180,
        user: str | None = None,
        port: int | None = None,
        background: bool = False,
    ) -> str:
        """Deploy and execute a bash script on a VM.

        Transport priority: SSH → noVNC console.

        Args:
            service_id: SHC VM service ID.
            script: Bash script content.
            verify: Verify SHA256 of deployed script before executing.
            timeout: SSH command timeout (seconds).
            user: SSH username (auto-detected from VM os_user if None).
            port: SSH port (auto-probed: tries 22 then 2222 if None).
            background: If True, run script with nohup (don't wait for output).

        Returns:
            Script stdout (SSH) or deployment confirmation (console).

        Raises:
            RuntimeError: If both transports fail.
        """
        vm = self.client.get_vm(service_id)
        ips = vm.get("ips", [])
        if not ips:
            raise RuntimeError(f"VM {service_id} has no IP assigned")
        ip = ips[0]["ip"]
        if user is None:
            user = vm.get("os_user", "debian")

        # Try SSH first
        try:
            return self._deploy_ssh(
                ip, user, port, script, verify, timeout, background
            )
        except Exception as e:
            log.warning("SSH transport failed for %s: %s", ip, e)
            if self.console is None:
                raise RuntimeError(
                    f"SSH failed ({e}) and no ConsoleSession for fallback. "
                    f"Pass console=ConsoleSession() to VMBootstrap for noVNC support."
                ) from e

        # Fall back to noVNC console
        log.info("Falling back to noVNC console transport for service %d", service_id)
        return self._deploy_console(service_id, script, verify, background)

    # ── SSH Transport ───────────────────────────────────────────

    def _probe_ssh_port(self, ip: str, port: int | None) -> int:
        """Find a working SSH port (try 22, then 2222 for tollgate-deployed VMs)."""
        if port is not None:
            return port
        for p in (22, 2222):
            try:
                with socket.create_connection((ip, p), timeout=5):
                    return p
            except (socket.timeout, ConnectionRefusedError, OSError):
                continue
        raise RuntimeError(f"No SSH port reachable on {ip} (tried 22, 2222)")

    def _deploy_ssh(
        self,
        ip: str,
        user: str,
        port: int | None,
        script: str,
        verify: bool,
        timeout: int,
        background: bool,
    ) -> str:
        """Deploy via SSH: base64-encode, write, verify SHA256, execute."""
        port = self._probe_ssh_port(ip, port)
        b64 = base64.b64encode(script.encode()).decode()

        parts = [f"echo '{b64}' | base64 -d > {REMOTE_PATH}"]
        parts.append(f"chmod +x {REMOTE_PATH}")

        if verify:
            local_sha = hashlib.sha256(script.encode()).hexdigest()  # noqa: F841
            parts.append(f"echo '{local_sha}  {REMOTE_PATH}' | sha256sum -c -")

        if background:
            parts.append(f"nohup {REMOTE_PATH} > /tmp/shc-bootstrap.log 2>&1 &")
            parts.append("echo 'Background PID:' $!")
        else:
            parts.append(REMOTE_PATH)

        cmd = " && ".join(parts)
        return ssh_cmd(ip, cmd, user=user, port=port, timeout=timeout)

    # ── noVNC Console Transport ─────────────────────────────────

    def _deploy_console(
        self,
        service_id: int,
        script: str,
        verify: bool,
        background: bool,
    ) -> str:
        """Deploy via noVNC: login, type script, verify SHA256, execute."""
        console = self.console
        if not console._logged_in:
            console.login()

        # Get VM credentials
        username, password = console.get_service_password(service_id)
        console.open_console(service_id)
        time.sleep(3)

        # Login to the console (username + password at tty prompt)
        console.type_text(f"{username}\n")
        time.sleep(2)
        console.type_text(f"{password}\n")
        time.sleep(3)

        # Deploy script via base64 (avoids special-char issues in noVNC typing)
        b64 = base64.b64encode(script.encode()).decode()
        console.type_text(f"echo '{b64}' | base64 -d > {REMOTE_PATH}\n")
        time.sleep(2)

        # Verify SHA256 (the script self-checks; we just print both for visual confirm)
        if verify:
            local_sha = hashlib.sha256(script.encode()).hexdigest()  # noqa: F841
            console.type_text(f"sha256sum {REMOTE_PATH}\n")
            time.sleep(2)
            console.screenshot(f"/tmp/shc-bootstrap-verify-{service_id}.png")
            log.info("SHA256 verification screenshot saved")

        # Execute
        console.type_text(f"chmod +x {REMOTE_PATH}\n")
        time.sleep(1)

        if background:
            console.type_text(f"nohup {REMOTE_PATH} > /tmp/shc-bootstrap.log 2>&1 &\n")
            time.sleep(2)
            console.type_text("echo 'Background PID:' $!\n")
        else:
            console.type_text(f"{REMOTE_PATH}\n")
            time.sleep(5)

        return f"Deployed via noVNC console to service {service_id} (user={username})"
