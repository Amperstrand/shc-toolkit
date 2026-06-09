"""
VM provisioning: install Caddy, get TLS certs via DNS-01 + nodns, verify HTTPS.

Pipeline:
1. Publish A record via nodns (Nostr kind 11111)
2. Publish _acme-challenge TXT via nodns
3. Run certbot with manual DNS-01 hook
4. Install cert in Caddy
5. Verify HTTPS response

Note: Caddy's built-in automatic HTTPS uses HTTP-01 (port 80) by default.
For DNS-01 challenges (no port 80 needed), we use certbot with manual hooks
and feed the TXT records through nodns.
"""

from __future__ import annotations

import logging
import subprocess
import time
from typing import Any

log = logging.getLogger(__name__)


def ssh_cmd(host: str, cmd: str, user: str = "debian", timeout: int = 120) -> str:
    """Run a command on the VM via SSH."""
    result = subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-o", f"ConnectTimeout={min(timeout, 15)}",
         f"{user}@{host}", cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"SSH command failed (rc={result.returncode}): {cmd}\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
    return result.stdout.strip()


def scp_to_vm(host: str, local: str, remote: str, user: str = "debian") -> str:
    """Copy file to VM via scp."""
    result = subprocess.run(
        ["scp", "-o", "StrictHostKeyChecking=no", "-O",
         local, f"{user}@{host}:{remote}"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"scp failed: {result.stderr}")
    return result.stdout.strip()


def install_caddy(host: str, user: str = "debian") -> str:
    """Install Caddy on Debian VM."""
    log.info(f"Installing Caddy on {host}...")
    return ssh_cmd(host, """
        sudo apt-get update -qq
        sudo apt-get install -y -qq debian-keyring debian-archive-keyring apt-transport-https curl
        curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg 2>/dev/null
        curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list > /dev/null
        sudo apt-get update -qq
        sudo apt-get install -y -qq caddy
        caddy version
    """, user=user, timeout=180)


def install_certbot(host: str, user: str = "debian") -> str:
    """Install certbot on Debian VM."""
    log.info(f"Installing certbot on {host}...")
    return ssh_cmd(host, """
        sudo apt-get install -y -qq certbot
        certbot --version
    """, user=user, timeout=120)


def generate_caddyfile(fqdn: str, backend_port: int = 8080) -> str:
    """Generate a Caddyfile that serves HTTPS with manual cert + reverse proxy."""
    return f"""{fqdn} {{
    tls /etc/ssl/certs/{fqdn}.pem /etc/ssl/private/{fqdn}.key
    reverse_proxy localhost:{backend_port}
    respond /health "OK" 200
}}
"""


def setup_caddy(host: str, fqdn: str, user: str = "debian") -> str:
    """Write Caddyfile and restart Caddy."""
    caddyfile = generate_caddyfile(fqdn)
    log.info(f"Writing Caddyfile for {fqdn} on {host}...")

    ssh_cmd(host, f"sudo mkdir -p /etc/caddy")
    # Write Caddyfile via stdin to avoid quoting issues
    subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}",
         "sudo tee /etc/caddy/Caddyfile > /dev/null"],
        input=caddyfile,
        text=True,
        timeout=30,
    )
    return ssh_cmd(host, "sudo systemctl restart caddy && sudo systemctl status caddy --no-pager -l | head -5")


def get_cert_dns01(
    host: str,
    fqdn: str,
    email: str = "admin@nodns.shop",
    user: str = "debian",
) -> str:
    """Get Let's Encrypt cert using certbot with manual DNS-01.

    IMPORTANT: The ACME challenge TXT record must already be published
    via nodns BEFORE calling this. Use nodns.publish_acme_challenge().

    This uses certbot's manual authenticator with --manual-auth-hook disabled
    since we handle DNS via nodns separately.
    """
    log.info(f"Requesting cert for {fqdn} via DNS-01...")

    # Create cert directory
    ssh_cmd(host, "sudo mkdir -p /etc/ssl/certs /etc/ssl/private")

    # Use certbot certonly with manual DNS plugin
    # --manual: interactive but we pre-place the challenge
    # --preferred-challenges dns-01: use DNS challenge
    # --manual-auth-hook: not used, we publish TXT via nodns separately
    result = ssh_cmd(
        host,
        f"""
        sudo certbot certonly \\
            --manual \\
            --preferred-challenges dns \\
            --manual-auth-hook /bin/true \\
            --manual-cleanup-hook /bin/true \\
            -d {fqdn} \\
            --email {email} \\
            --agree-tos \\
            --non-interactive \\
            --manual-public-ip-logging-ok \\
            --dns-{fqdn}-01-wait 0 || true

        # Copy certs to caddy-accessible location
        sudo cp /etc/letsencrypt/live/{fqdn}/fullchain.pem /etc/ssl/certs/{fqdn}.pem 2>/dev/null
        sudo cp /etc/letsencrypt/live/{fqdn}/privkey.pem /etc/ssl/private/{fqdn}.key 2>/dev/null
        sudo chmod 644 /etc/ssl/certs/{fqdn}.pem
        sudo chmod 600 /etc/ssl/private/{fqdn}.key
        ls -la /etc/ssl/certs/{fqdn}.pem /etc/ssl/private/{fqdn}.key
        """,
        user=user,
        timeout=300,
    )
    return result


def verify_https(fqdn: str, timeout: int = 30) -> dict:
    """Verify HTTPS is working by curling the domain."""
    try:
        result = subprocess.run(
            ["curl", "-sSf", "--max-time", str(timeout),
             f"https://{fqdn}/health"],
            capture_output=True,
            text=True,
            timeout=timeout + 10,
        )
        return {
            "fqdn": fqdn,
            "status_code": "ok" if result.returncode == 0 else "failed",
            "body": result.stdout.strip(),
            "success": result.returncode == 0,
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        return {"fqdn": fqdn, "success": False, "error": str(e)}
