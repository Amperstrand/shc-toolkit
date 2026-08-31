"""VM-side self-destruct: per-run suicide key + systemd oneshot timer.

Defense-in-depth cleanup for ephemeral CI VMs. The controller teardown
runs first; this timer fires even when the controller is dead (workflow
cancelled mid-run, network partition), cancelling the VM ``minutes``
after boot. The hourly reaper stays as the last-resort backstop.

Live-earned constraints this encodes (probed 2026-08-27):

- Only ``full``-scope credentials can cancel — cancel is a money op
  (prorated refund), so ``operate``-scope API keys and nostr operate
  leases both 403 it, confirm-gate or not.
- Bearer API keys CANNOT mint other keys (``POST /account/api-keys`` is
  forbidden for them); minting needs HTTP Basic (email + password).

Two key sources, in resolution order (``arm_self_destruct``):

1. a pre-minted key via the ``SHC_SUICIDE_KEY`` env var — the CI-friendly
   path: one short-expiry full key stored as a repo/runner secret,
   planted on every VM (no Basic creds needed at run time);
2. a per-run mint over HTTP Basic (``SHC_ACCOUNT_EMAIL`` /
   ``SHC_ACCOUNT_PASSWORD``, or explicit args) — ``expires_in_days=1``
   (API minimum) so the planted key self-revokes; ``revokeApiKey`` is
   Basic+OTP identity-class, so an API-key controller cannot revoke it.

NEVER arm this on a box running untrusted code (e.g. tollgate VMs):
the planted key grants account-wide spend for up to its lifetime.
"""

from __future__ import annotations

import base64
import json as _json
from collections.abc import Callable
from typing import Any

from .client import BASE_URL, USER_AGENT, _error_from_body

SUICIDE_KEY_ENV = "SHC_SUICIDE_KEY"
ACCOUNT_EMAIL_ENV = "SHC_ACCOUNT_EMAIL"
ACCOUNT_PASSWORD_ENV = "SHC_ACCOUNT_PASSWORD"

KEY_PATH = "/etc/shc/self-destruct.key"


def mint_suicide_key(
    email: str,
    password: str,
    service_id: int,
    *,
    base_url: str = BASE_URL,
) -> str:
    """Mint a per-run suicide key over HTTP Basic: full scope (only full
    can cancel), 1-day expiry (API minimum — it self-revokes)."""
    import httpx

    with httpx.Client(timeout=30.0) as http:
        resp = http.request(
            "POST",
            f"{base_url}/account/api-keys",
            auth=(email, password),
            headers={"User-Agent": USER_AGENT},
            json={
                "name": f"selfdestruct-{service_id}",
                "scope": "full",
                "expires_in_days": 1,
            },
        )
    try:
        body: Any = _json.loads(resp.text) if resp.text.strip() else {}
    except _json.JSONDecodeError:
        body = {}
    if resp.status_code >= 400:
        raise _error_from_body(body, resp.text, resp.status_code)
    data = body.get("data", body)
    key = data.get("api_key") or data.get("key")
    if not key:
        raise RuntimeError(f"api-key mint returned no key: {resp.text[:200]}")
    return key


def selfdestruct_script(service_id: int, base_url: str = BASE_URL) -> str:
    """The on-VM python3 script: cancel THIS vm, incl. the 409
    confirmation_id -> ``X-User-Api-Confirm`` re-send dance. Stdlib
    only (no shc-toolkit install on the box)."""
    return f'''#!/usr/bin/env python3
"""SHC VM self-destruct: cancel this VM (controller-dead failsafe).

Planted by shc_toolkit.selfdestruct. The Bearer key is a short-expiry
full-scope key at {KEY_PATH} (0400, root) — nothing else on the box.
"""
import json
import sys
import urllib.error
import urllib.request

BASE = {base_url!r}
SID = {service_id!r}
KEY_FILE = {KEY_PATH!r}
IDEM = f"selfdestruct-{{SID}}"


def cancel(key, extra_headers=None):
    req = urllib.request.Request(
        f"{{BASE}}/vm/{{SID}}/cancel",
        data=json.dumps({{"immediate": True}}).encode(),
        headers={{
            "Authorization": f"Bearer {{key}}",
            "Content-Type": "application/json",
            "Idempotency-Key": IDEM,
            "User-Agent": "shc-toolkit-selfdestruct/1",
            **(extra_headers or {{}}),
        }},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode()


def main():
    key = open(KEY_FILE).read().strip()
    try:
        status, body = cancel(key)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 409:
            conf = _json_loads(body).get("confirmation", {{}}) or {{}}
            cid = conf.get("confirmation_id") or (conf.get("structuredContent", {{}}) or {{}}).get("confirmation_id")
            if not cid:
                sys.exit(f"self-destruct: 409 without confirmation_id: {{body[:200]}}")
            status, body = cancel(key, {{"X-User-Api-Confirm": cid}})
        elif e.code == 404:
            print("self-destruct: VM already cancelled — nothing to do")
            return
        else:
            raise
    print(f"self-destruct: cancel HTTP {{status}}: {{body[:200]}}")


def _json_loads(text):
    try:
        return json.loads(text)
    except ValueError:
        return {{}}


if __name__ == "__main__":
    main()
'''


def selfdestruct_units(minutes: int) -> dict[str, str]:
    """systemd unit files: a oneshot service (with failure retries) and
    an ``OnBootSec`` timer that survives reboots — unlike an ``at`` job,
    which a reboot silently discards."""
    service = """[Unit]
Description=SHC VM self-destruct (cancel this VM - controller-dead failsafe)

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/sbin/shc-self-destruct.py
Restart=on-failure
RestartSec=60
"""
    timer = f"""[Unit]
Description=Arm SHC VM self-destruct at boot+{minutes}min

[Timer]
OnBootSec={minutes}min
AccuracySec=1min
Unit=shc-self-destruct.service

[Install]
WantedBy=timers.target
"""
    return {"service": service, "timer": timer}


def build_installer(
    *, service_id: int, minutes: int, key: str, base_url: str = BASE_URL
) -> str:
    """One SSH command that plants everything. base64-wrapped so the key
    never appears in plaintext process listings or shell history."""
    installer = f"""#!/bin/bash
set -euo pipefail
install -d -m 0700 /etc/shc
umask 077
printf '%s\\n' {key!r} > {KEY_PATH}
chmod 0400 {KEY_PATH}
install -m 0700 /dev/stdin /usr/local/sbin/shc-self-destruct.py <<'PYEOF'
{selfdestruct_script(service_id, base_url)}PYEOF
cat > /etc/systemd/system/shc-self-destruct.service <<'UNITEOF'
{selfdestruct_units(minutes)["service"]}UNITEOF
cat > /etc/systemd/system/shc-self-destruct.timer <<'UNITEOF'
{selfdestruct_units(minutes)["timer"]}UNITEOF
systemctl daemon-reload
systemctl enable --now shc-self-destruct.timer
echo SELF_DESTRUCT_ARMED
"""
    blob = base64.b64encode(installer.encode()).decode()
    return f"echo {blob} | base64 -d | sudo bash"


def arm_self_destruct(
    ssh_run: Callable[[str], str],
    service_id: int,
    minutes: int,
    *,
    key: str | None = None,
    email: str | None = None,
    password: str | None = None,
    base_url: str = BASE_URL,
) -> dict[str, Any]:
    """Arm the on-VM self-destruct timer via ``ssh_run(cmd) -> stdout``.

    Key resolution: explicit ``key`` > ``SHC_SUICIDE_KEY`` env > per-run
    mint over HTTP Basic (explicit args > ``SHC_ACCOUNT_EMAIL`` /
    ``SHC_ACCOUNT_PASSWORD``). Raises RuntimeError with instructions
    when no source is available — arming is a requested guarantee, so
    failing loud beats shipping an unarmed VM silently.
    """
    import os

    source = "explicit"
    if not key:
        key = os.environ.get(SUICIDE_KEY_ENV) or None
        source = SUICIDE_KEY_ENV
    if not key:
        email = email or os.environ.get(ACCOUNT_EMAIL_ENV)
        password = password or os.environ.get(ACCOUNT_PASSWORD_ENV)
        if email and password:
            key = mint_suicide_key(email, password, service_id, base_url=base_url)
            source = f"minted ({ACCOUNT_EMAIL_ENV})"
    if not key:
        raise RuntimeError(
            "self-destruct needs a full-scope key: set "
            f"{SUICIDE_KEY_ENV} (pre-minted short-expiry key secret), or "
            f"{ACCOUNT_EMAIL_ENV} + {ACCOUNT_PASSWORD_ENV} for a per-run "
            "1-day mint. Bearer API keys cannot mint keys (Basic only), "
            "and only full scope can cancel."
        )
    out = ssh_run(
        build_installer(
            service_id=service_id, minutes=minutes, key=key, base_url=base_url
        )
    )
    if "SELF_DESTRUCT_ARMED" not in out:
        raise RuntimeError(f"installer did not signal arming: {out[-300:]}")
    return {
        "armed": True,
        "service_id": service_id,
        "minutes": minutes,
        "key_source": source,
    }
