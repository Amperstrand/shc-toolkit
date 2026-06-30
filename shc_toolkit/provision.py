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


def ssh_cmd(host: str, cmd: str, user: str = "debian", timeout: int = 120, port: int = 22) -> str:
    """Run a command on the VM via SSH."""
    result = subprocess.run(
        ["ssh", "-p", str(port),
         "-o", "StrictHostKeyChecking=no", "-o", f"ConnectTimeout={min(timeout, 15)}",
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


def scp_to_vm(host: str, local: str, remote: str, user: str = "debian", port: int = 22) -> str:
    """Copy file to VM via scp."""
    result = subprocess.run(
        ["scp", "-P", str(port), "-o", "StrictHostKeyChecking=no", "-O",
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
    """Generate a Caddyfile that serves HTTPS with Let's Encrypt cert + reverse proxy."""
    return f"""{fqdn} {{
    tls /etc/letsencrypt/live/{fqdn}/fullchain.pem /etc/letsencrypt/live/{fqdn}/privkey.pem
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


def generate_certbot_auth_hook(venv_path: str = "/home/debian/shc-toolkit", keypair_path: str = "/tmp/nodns-keypair.json") -> str:
    """Generate a certbot manual auth hook script.

    The hook reads CERTBOT_DOMAIN and CERTBOT_VALIDATION from the environment,
    publishes _acme-challenge TXT via nodns, and waits for propagation.
    """
    return f"""#!/bin/sh
# Certbot DNS-01 auth hook for nodns
export PATH="{venv_path}/bin:$PATH"
export PYTHONPATH="/home/debian:$PYTHONPATH"
python3 -c "
import sys, os, time, json
sys.path.insert(0, '/home/debian')
from nodns_vm import NoDNSKeyPair, publish_dns_records

kp_data = json.load(open('{keypair_path}'))
kp = NoDNSKeyPair.from_nsec(kp_data['nsec'])
domain = os.environ.get('CERTBOT_DOMAIN', '')
validation = os.environ.get('CERTBOT_VALIDATION', '')

print(f'Auth hook: _acme-challenge.{{domain}} -> {{validation[:40]}}...')
result = publish_dns_records(kp, [{{'type': 'TXT', 'name': '_acme-challenge', 'value': validation, 'ttl': 60}}])
print(f'Published TXT to {{result[\"relays_sent\"]}} relays, waiting 15s...')
time.sleep(15)
print('Done')
"
"""


def get_cert_dns01(
    host: str,
    fqdn: str,
    keypair_path: str = "/tmp/nodns-keypair.json",
    email: str = "admin@example.com",
    user: str = "debian",
) -> str:
    """Get Let's Encrypt cert using certbot with manual DNS-01 via nodns.

    Prerequisites:
    - nodns keypair saved to keypair_path on the VM
    - nostr-sdk installed in /home/debian/shc-toolkit venv
    - nodns_vm.py in /home/debian/

    Pipeline:
    1. Generate and deploy certbot auth hook to VM
    2. Run certbot certonly with --manual-auth-hook pointing to our script
    3. Auth hook publishes _acme-challenge TXT via nostr-sdk + nodns
    4. certbot verifies TXT record, issues cert
    """
    log.info(f"Requesting cert for {fqdn} via DNS-01...")

    hook_script = generate_certbot_auth_hook(keypair_path=keypair_path)
    hook_remote = "/tmp/certbot-auth-hook.sh"

    subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}",
         f"sudo tee {hook_remote} > /dev/null"],
        input=hook_script,
        text=True,
        timeout=30,
    )
    ssh_cmd(host, f"sudo chmod +x {hook_remote}")

    result = ssh_cmd(
        host,
        f"""
        sudo certbot certonly \
            --manual \
            --preferred-challenges dns \
            --manual-auth-hook {hook_remote} \
            --manual-cleanup-hook /bin/true \
            -d {fqdn} \
            --agree-tos \
            --email {email} \
            --non-interactive \
            --manual-public-ip-logging-ok
        """,
        user=user,
        timeout=300,
    )

    cert_dir = f"/etc/letsencrypt/live/{fqdn}"
    log.info(f"Cert issued: {cert_dir}/fullchain.pem")
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
