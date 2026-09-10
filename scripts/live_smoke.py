#!/usr/bin/env python3
"""Monthly multi-zone live smoke: one VM per catalog line, order → provision
→ ssh_key check → reachability → cancel → refund.

Exercises the full toolkit path against the real API for EVERY facility:
static storefront triple, catalog model pricing, order, active+IP readiness,
ssh_key persistence, TCP/22 from this vantage, and — for flagged
(Cherryvale) lines — the Katy→Cherryvale bastion canary (the internal route
SHC hasn't added yet; #39). Cost: ~$0.01 per zone (1h minimum, prorated
refund) — ~$0.04-0.06 per all-zone run, monthly.

Zone-dependent criteria (AGENTS "Zone-dependent test criteria"):
  * stable lines (nvme/hdd, Katy): hard pass/fail — defects FAIL the run
  * watch lines (ssd/dev, Cherryvale): log-only — failures WARN, never fail
  * stock/availability rejections: WARN for any line (capacity ≠ defect)
  * the bastion canary reports both ways: unreachable is today's expected
    state; OPEN means SHC added the internal route (celebrate on #39)

Usage:
    SHC_API_KEY=shc_live_... python3 scripts/live_smoke.py [--zone all|nvme|hdd|ssd|dev] [--timeout 240]

Exit 0 = stable lines healthy (watch lines may have warned); 1 = a stable
line failed or any cancel failed (a failed cancel means STILL BILLING).
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shc_toolkit.client import SHCClient
from shc_toolkit.sizes import is_watch_line, smallest_size_for_line

LINES = ("nvme", "hdd", "ssd", "dev")

_STOCK_MARKERS = ("stock", "unavailable", "sold out", "capacity", "no slots")


def _is_stock_error(exc: Exception) -> bool:
    text = f"{getattr(exc, 'code', '')} {exc}".lower()
    return any(marker in text for marker in _STOCK_MARKERS)


def _wait_active_ip(client: SHCClient, sid: int, timeout: int) -> str | None:
    """service_status active + IP (provisioning_state lies — lesson 1)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        vm = client.get_vm(sid)
        ips = vm.get("ips", [])
        ip = ips[0]["ip"] if ips and isinstance(ips[0], dict) else None
        if vm.get("service_status") == "active" and ip:
            return ip
        if vm.get("provisioning_state") in ("failed", "error"):
            return None
        time.sleep(10)
    return None


def _tcp22(ip: str, timeout: float = 15.0) -> bool:
    try:
        with socket.create_connection((ip, 22), timeout=timeout):
            return True
    except OSError:
        return False


class Bastion:
    """One Katy VM reused for the Cherryvale bastion canary checks.

    The internal Katy→Cherryvale route is the thing being monitored: SSH to
    the bastion, then /dev/tcp to the flagged VM. Unreachable from the
    bastion is today's expected state (#39); OPEN means SHC added the route.
    """

    def __init__(self, client: SHCClient, ssh_key: str | None, log=print):
        self._client = client
        self._ssh_key = ssh_key
        self._log = log
        self.sid: int | None = None
        self.ip: str | None = None

    def ensure(self) -> bool:
        if self.sid:
            return True
        size = smallest_size_for_line("nvme")
        if not size:
            self._log("WARN: bastion skipped — no nvme size in catalog")
            return False
        try:
            result = self._client.order_vm(
                hostname="ci-live-smoke-bastion-reap2h",
                size=size[0],
                ssh_key=self._ssh_key,
                pay=False,
            )
            self.sid = (
                result.get("service_id") or (result.get("service_ids") or [None])[0]
            )
        except Exception as e:
            self._log(f"WARN: bastion order failed: {e}")
            return False
        self.ip = _wait_active_ip(self._client, self.sid, 240)
        if not self.ip:
            self._log("WARN: bastion never reached active+IP — canary skipped")
            return False
        self._log(f"bastion up: sid={self.sid} ip={self.ip}")
        return True

    def can_reach(self, target_ip: str) -> str:
        """'open' | 'unreachable' | 'skipped' — never raises."""
        if not self.ensure():
            return "skipped"
        if not self._ssh_key:
            return "skipped"
        probe = (
            f"timeout 8 bash -c 'exec 3<>/dev/tcp/{target_ip}/22 "
            f"&& head -c 20 <&3' 2>/dev/null"
        )
        try:
            r = subprocess.run(
                [
                    "ssh",
                    "-o",
                    "StrictHostKeyChecking=no",
                    "-o",
                    "UserKnownHostsFile=/dev/null",
                    "-o",
                    "BatchMode=yes",
                    "-o",
                    "ConnectTimeout=15",
                    f"debian@{self.ip}",
                    probe,
                ],
                capture_output=True,
                text=True,
                timeout=40,
            )
        except subprocess.TimeoutExpired:
            return "unreachable"
        return "open" if r.returncode == 0 else "unreachable"

    def cancel(self) -> None:
        if self.sid:
            try:
                self._client.cancel_vm(self.sid, immediate=True, confirm=True)
                self._log(f"bastion sid={self.sid} cancelled")
            except Exception as e:
                self._log(f"FAIL: bastion cancel failed ({e}) — STILL BILLING")


def run_line(
    client: SHCClient,
    line: str,
    bastion: Bastion,
    ssh_key: str | None,
    timeout: int,
    hostname_prefix: str,
) -> list[str]:
    """One catalog line. Returns hard failures (warnings print, don't collect)."""
    failures: list[str] = []
    watch = is_watch_line(line)
    tier = "WATCH" if watch else "STABLE"
    smallest = smallest_size_for_line(line)
    if not smallest:
        return [f"{line}: no size in catalog (catalog model drift?)"]
    size_name, info = smallest
    print(f"\n=== {tier} zone {line} ({size_name}, ${info['daily_price']}/day) ===")
    t0 = time.time()
    sid: int | None = None

    try:
        try:
            result = client.order_vm(
                hostname=f"{hostname_prefix}-{line}-reap2h",
                size=size_name,
                ssh_key=ssh_key,
                pay=False,
            )
            sid = result.get("service_id") or (result.get("service_ids") or [None])[0]
        except Exception as e:
            if _is_stock_error(e):
                print(f"WARN: {line}: out of stock / unavailable ({e})")
                return failures
            msg = f"{line}: order failed: {e}"
            (print(f"WARN: {msg}") if watch else failures.append(msg))
            return failures
        if not sid:
            failures.append(f"{line}: no service_id in order result")
            return failures
        print(f"[{time.time() - t0:5.1f}s] ordered sid={sid}")

        ip = _wait_active_ip(client, sid, timeout)
        if not ip:
            msg = f"{line}: no active+IP within {timeout}s (sid={sid})"
            (print(f"WARN: {msg}") if watch else failures.append(msg))
            return failures
        print(f"[{time.time() - t0:5.1f}s] ACTIVE ip={ip}")

        vm = client.get_vm(sid)
        if ssh_key and not vm.get("ssh_key"):
            msg = f"{line}: ssh_key not stored — storefront triple regression?"
            (print(f"WARN: {msg}") if watch else failures.append(msg))
        if vm.get("os_template") != "debian13-cloud":
            msg = f"{line}: unexpected template {vm.get('os_template')!r}"
            (print(f"WARN: {msg}") if watch else failures.append(msg))

        direct = _tcp22(ip)
        verdict = "open" if direct else "closed"
        if watch:
            print(
                f"[{time.time() - t0:5.1f}s] direct TCP/22 from this vantage: "
                f"{verdict} (GitHub/Azure reaches Cherryvale via the narrow "
                f"path; most of the world does not — #39)"
            )
            through = bastion.can_reach(ip)
            if through == "open":
                print(
                    f"[{time.time() - t0:5.1f}s] bastion Katy→{line}: OPEN — "
                    f"the internal route EXISTS (report on #39!)"
                )
            elif through == "unreachable":
                print(
                    f"[{time.time() - t0:5.1f}s] bastion Katy→{line}: "
                    f"unreachable (expected until SHC adds the internal route)"
                )
            else:
                print(f"[{time.time() - t0:5.1f}s] bastion Katy→{line}: skipped")
        else:
            if not direct:
                failures.append(f"{line}: TCP/22 closed from this vantage ({ip})")
            else:
                print(f"[{time.time() - t0:5.1f}s] direct TCP/22: open")
    finally:
        if sid:
            try:
                client.cancel_vm(sid, immediate=True, confirm=True)
                print(f"[{time.time() - t0:5.1f}s] cancelled sid={sid}")
            except Exception as e:
                failures.append(
                    f"{line}: cancel failed ({e}) — sid={sid} STILL BILLING"
                )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zone",
        default="all",
        choices=("all", *LINES),
        help="which catalog line(s) to smoke (default: all four)",
    )
    parser.add_argument(
        "--timeout", type=int, default=240, help="provision wait seconds per zone"
    )
    parser.add_argument("--hostname", default="ci-live-smoke")
    args = parser.parse_args()

    api_key = os.environ.get("SHC_API_KEY", "")
    if not api_key:
        print("ERROR: SHC_API_KEY not set", file=sys.stderr)
        return 2

    ssh_pub = Path.home() / ".ssh" / "id_ed25519.pub"
    ssh_key = ssh_pub.read_text().strip() if ssh_pub.exists() else None

    client = SHCClient(api_key=api_key)
    bastion = Bastion(client, ssh_key)
    lines = LINES if args.zone == "all" else (args.zone,)
    t0 = time.time()
    failures: list[str] = []

    try:
        for line in lines:
            failures.extend(
                run_line(client, line, bastion, ssh_key, args.timeout, args.hostname)
            )
    finally:
        bastion.cancel()

    for f in failures:
        print(f"FAIL: {f}")
    verdict = "PASSED" if not failures else "FAILED"
    print(f"\n[{time.time() - t0:5.1f}s] multi-zone smoke {verdict}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
