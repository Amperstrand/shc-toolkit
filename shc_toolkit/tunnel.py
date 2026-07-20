"""
SHC Cloudflare Quick Tunnel — SSH access when inbound traffic is blocked.

When SHC infrastructure blocks inbound connections to VMs (a known
intermittent issue), this module establishes SSH access via Cloudflare
Quick Tunnel. The tunnel uses outbound HTTPS only — no inbound ports,
no account, no signup required.

Two classes are provided:

    CloudflareTunnel — manages the full tunnel lifecycle
    ConsoleShell     — reusable noVNC console automation

Convenience function:

    ensure_ssh_access(service_id) → (host, port)

Usage:

    from shc_toolkit import ensure_ssh_access

    host, port = ensure_ssh_access(1077)
    # → ("localhost", 2222) if tunnel was needed
    # → ("66.92.204.237", 22) if direct SSH worked

    import subprocess
    subprocess.run(["ssh", "-p", str(port), f"debian@{host}", "uptime"])

Prerequisites:

    pip install shc-toolkit[tunnel]
    # Installs: playwright, pytesseract, Pillow

    playwright install chromium
"""

from __future__ import annotations

import logging
import os
import subprocess
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mcp_client import SHCMCPClient
    from .client import SHCClient

log = logging.getLogger(__name__)

_CF_BINARY_PATHS = [
    "/tmp/cf-binary",
    "/usr/local/bin/cloudflared",
    os.path.expanduser("~/.local/bin/cloudflared"),
]


class TunnelError(Exception):
    """Tunnel establishment or connection failed."""


class ConsoleShell:
    """noVNC console automation via SHC MCP API + Playwright.

    Provides reliable text input via the hidden textarea + "Type into VM"
    button, and output reading via screenshot + OCR.

    Requires: playwright, pytesseract, Pillow
    Install:  pip install shc-toolkit[tunnel] && playwright install chromium
    """

    def __init__(
        self,
        service_id: int,
        mcp_client: SHCMCPClient | None = None,
    ):
        try:
            from playwright.sync_api import sync_playwright
            import pytesseract
            from PIL import Image
        except ImportError as e:
            raise TunnelError(
                "ConsoleShell requires playwright, pytesseract, Pillow. "
                f"Install with: pip install shc-toolkit[tunnel] ({e})"
            ) from e

        self._sync_playwright = sync_playwright
        self._pytesseract = pytesseract
        self._Image = Image
        self.service_id = service_id
        self._mcp = mcp_client
        self._browser = None
        self._page = None
        self._username: str | None = None
        self._password: str | None = None

    def _ensure_mcp(self) -> SHCMCPClient:
        if self._mcp is None:
            from .mcp_client import SHCMCPClient
            self._mcp = SHCMCPClient()
        return self._mcp

    def _ocr(self, path: str) -> str:
        return self._pytesseract.image_to_string(
            self._Image.open(path), config="--psm 6"
        ).strip().lower()

    def _send_text(self, text: str) -> None:
        """Send text to the VM via noVNC textarea + Type button."""
        self._page.evaluate(
            f"""() => {{
                document.getElementById('clipboard-textarea').value = {repr(text)};
                document.getElementById('btn-send').click();
            }}"""
        )
        self._page.wait_for_timeout(800)

    def connect(self) -> None:
        """Open a noVNC console session and connect."""
        mcp = self._ensure_mcp()
        session = mcp.create_console_session(self.service_id)
        url = session["console_url"]

        pw = self._sync_playwright().start()
        self._browser = pw.chromium.launch(headless=True)
        self._page = self._browser.new_page(viewport={"width": 1024, "height": 768})
        self._page.goto(url, wait_until="networkidle", timeout=15000)
        self._page.wait_for_timeout(5000)
        self._playwright = pw

    def login(self, username: str | None = None, password: str | None = None) -> bool:
        """Log into the VM console. Fetches credentials if not provided."""
        mcp = self._ensure_mcp()
        if username is None or password is None:
            creds = mcp.get_vm_credentials(self.service_id)
            username = username or creds["user"]
            password = password or creds["password"]
        self._username = username
        self._password = password

        self._page.keyboard.press("Enter")
        self._page.wait_for_timeout(2000)
        self._send_text(f"{username}\n")
        self._page.wait_for_timeout(3000)
        self._send_text(f"{password}\n")
        self._page.wait_for_timeout(8000)
        self._send_text("clear\n")
        self._page.wait_for_timeout(2000)

        return self.verify_shell()

    def verify_shell(self) -> bool:
        """Check if we have an active shell prompt."""
        self._send_text("echo 77777\n")
        self._page.wait_for_timeout(3000)
        path = f"/tmp/_console_verify_{self.service_id}.png"
        self._page.screenshot(path=path)
        return "77777" in self._ocr(path)

    def run_cmd(self, cmd: str, wait: float = 5.0) -> str:
        """Run a command and return OCR'd output."""
        self._send_text("clear\n")
        self._page.wait_for_timeout(1000)
        self._send_text(cmd + "\n")
        self._page.wait_for_timeout(int(wait * 1000))
        path = f"/tmp/_console_cmd_{self.service_id}_{int(time.time())}.png"
        self._page.screenshot(path=path)
        return self._ocr(path)

    def close(self) -> None:
        if self._browser:
            self._browser.close()
        if hasattr(self, "_playwright"):
            self._playwright.stop()
        self._browser = None
        self._page = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc):
        self.close()


class CloudflareTunnel:
    """Cloudflare Quick Tunnel for SSH access to SHC VMs.

    Creates an outbound-only HTTPS tunnel from the VM to Cloudflare's
    edge, then connects locally via cloudflared access tcp.

    No Cloudflare account, signup, or custom domain needed.
    The tunnel URL is ephemeral (*.trycloudflare.com).
    """

    def __init__(
        self,
        service_id: int,
        console: ConsoleShell | None = None,
        mcp_client: SHCMCPClient | None = None,
        local_port: int = 2222,
        ssh_key: str = "~/.ssh/id_ed25519",
    ):
        self.service_id = service_id
        self._console = console
        self._mcp = mcp_client
        self.local_port = local_port
        self.ssh_key = ssh_key
        self.tunnel_url: str | None = None
        self._local_proc: subprocess.Popen | None = None

    def _ensure_console(self) -> ConsoleShell:
        if self._console is None:
            self._console = ConsoleShell(self.service_id, mcp_client=self._mcp)
            self._console.connect()
            self._console.login()
        return self._console

    def ensure_on_vm(self) -> str:
        """Ensure cloudflared tunnel is running on the VM. Returns tunnel URL."""
        console = self._ensure_console()

        output = console.run_cmd(
            "pgrep -x cloudflared >/dev/null && echo RUNNING || echo STOPPED", wait=3
        )

        if "stopped" in output or "running" not in output:
            log.info("Starting cloudflared tunnel on VM %s", self.service_id)
            console.run_cmd(
                "nohup cloudflared tunnel --url tcp://localhost:22 "
                "> /tmp/cf-tunnel.log 2>&1 &",
                wait=15,
            )

        tunnel_url = self._extract_tunnel_url(console)
        if not tunnel_url:
            raise TunnelError("Could not extract tunnel URL from VM")

        self.tunnel_url = tunnel_url
        log.info("Tunnel URL: %s", tunnel_url)
        return tunnel_url

    def _extract_tunnel_url(self, console: ConsoleShell) -> str | None:
        """Get the tunnel URL via a transfer service for reliable extraction."""
        output = console.run_cmd(
            "grep -o 'https://[a-z0-9-]*\\.trycloudflare\\.com' "
            "/tmp/cf-tunnel.log | head -1 | curl -s -L -F 'f:1=<-' http://ix.io 2>&1",
            wait=10,
        )

        for line in output.split("\n"):
            line = line.strip().replace(" ", "")
            if "ix.io" in line and len(line) < 30:
                r = subprocess.run(
                    ["curl", "-s", "-L", line],
                    capture_output=True, text=True, timeout=10,
                )
                if "trycloudflare" in r.stdout:
                    return r.stdout.strip()

        for line in output.split("\n"):
            line = line.strip().replace(" ", "")
            if "trycloudflare" in line:
                return line

        return None

    def connect_local(self) -> None:
        """Start local cloudflared client to connect through the tunnel."""
        if not self.tunnel_url:
            raise TunnelError("No tunnel URL — call ensure_on_vm() first")

        cf_binary = _find_cloudflared()
        hostname = self.tunnel_url.replace("https://", "").rstrip("/")

        subprocess.run(["pkill", "-f", "cf-binary.*access"], capture_output=True)
        subprocess.run(["pkill", "-f", "cloudflared.*access"], capture_output=True)
        time.sleep(2)

        log.info("Starting local cloudflared client (port %d)", self.local_port)
        self._local_proc = subprocess.Popen(
            [cf_binary, "access", "tcp", "--hostname", hostname,
             "--url", f"localhost:{self.local_port}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(8)

    def ensure_ssh_key(self) -> None:
        """Add our SSH public key to the VM via console."""
        pubkey_path = os.path.expanduser(self.ssh_key + ".pub")
        if not os.path.isfile(pubkey_path):
            log.warning("No SSH public key at %s — skipping key injection", pubkey_path)
            return

        pubkey = open(pubkey_path).read().strip()
        console = self._ensure_console()

        console.run_cmd(f"echo '{pubkey}' >> ~/.ssh/authorized_keys", wait=3)
        console.run_cmd(
            "sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' "
            "/etc/ssh/sshd_config && sudo systemctl restart ssh",
            wait=5,
        )
        log.info("SSH key added to VM %s", self.service_id)

    def verify_ssh(self) -> bool:
        """Test SSH through the tunnel."""
        return _check_ssh("localhost", self.local_port, self.ssh_key)

    def close(self) -> None:
        if self._local_proc:
            self._local_proc.kill()
            self._local_proc = None
        if self._console:
            self._console.close()


def _check_ssh(
    ip: str, port: int = 22, key: str = "~/.ssh/id_ed25519", timeout: int = 8
) -> bool:
    """Test SSH connectivity."""
    try:
        r = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
             "-o", f"ConnectTimeout={timeout}", "-o", "LogLevel=ERROR",
             "-i", os.path.expanduser(key), "-p", str(port), f"debian@{ip}", "echo OK"],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        return "OK" in r.stdout
    except Exception:
        return False


def _find_cloudflared() -> str:
    """Find or download the cloudflared binary."""
    for path in _CF_BINARY_PATHS:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    path = "/tmp/cf-binary"
    log.info("Downloading cloudflared binary...")
    subprocess.run(
        ["wget", "-q", "-O", path,
         "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"],
        check=True, timeout=60,
    )
    subprocess.run(["chmod", "+x", path], check=True)
    return path


def ensure_ssh_access(
    service_id: int,
    local_port: int = 2222,
    key: str = "~/.ssh/id_ed25519",
    verbose: bool = True,
) -> tuple[str, int]:
    """Ensure SSH access to a VM. Returns (host, port).

    Tries direct SSH first. If blocked, establishes Cloudflare Quick Tunnel.

    Args:
        service_id: SHC VM service ID.
        local_port: Local port for tunnel (default 2222).
        key: SSH private key path.
        verbose: Print progress messages.

    Returns:
        (host, port) tuple for SSH connection.

    Raises:
        TunnelError: If neither direct SSH nor tunnel works.
    """
    from .client import SHCClient

    c = SHCClient()
    detail = c.get_vm(service_id)
    ip = detail["ips"][0]["ip"] if detail.get("ips") else None
    if not ip:
        raise TunnelError(f"VM {service_id} has no IP")

    if verbose:
        print(f"  VM {service_id} at {ip}")

    if _check_ssh(ip, key=key):
        if verbose:
            print("  Direct SSH works")
        return ip, 22

    if verbose:
        print("  Direct SSH blocked — establishing Cloudflare tunnel...")

    tunnel = CloudflareTunnel(
        service_id, local_port=local_port, ssh_key=key,
    )
    tunnel.ensure_on_vm()
    tunnel.connect_local()
    tunnel.ensure_ssh_key()

    if tunnel.verify_ssh():
        if verbose:
            print(f"  Tunnel SSH works on localhost:{local_port}")
        return "localhost", local_port

    raise TunnelError("Tunnel SSH failed after full setup")
