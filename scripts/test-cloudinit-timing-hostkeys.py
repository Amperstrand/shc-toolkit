"""cloud-init completion timing + SSH host key uniqueness test.

Orders TWO NVMe VMs from the same template, then:
1. Polls cloud-init status on VM #1 every 10s for 5 min (does it complete? error?)
2. Captures SSH host keys from BOTH VMs (are they unique or duplicated?)
3. Checks if vendor-data hardening (auditd, guest-agent) actually applied

Always cancels both VMs. Saves results to notes/.
"""
from __future__ import annotations
import os, subprocess, sys, time, uuid, json
from pathlib import Path
from shc_toolkit import SHCClient
from shc_pulumi.sizes import resolve_size

THROWKEY = "/tmp/tg-cloudinit-probe-key"
NOTES = Path(__file__).resolve().parent.parent / "notes"


def ssh(host, cmd, timeout=30):
    r = subprocess.run(
        ["ssh", "-i", THROWKEY, "-o", "StrictHostKeyChecking=no",
         "-o", "UserKnownHostsFile=/dev/null", "-o", "LogLevel=ERROR",
         "-o", f"ConnectTimeout={min(timeout,15)}", f"debian@{host}", cmd],
        capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip() if r.returncode == 0 else f"<rc={r.returncode}>"


def wait_ssh(host, timeout=240):
    end = time.time() + timeout
    while time.time() < end:
        try:
            if "SSH_READY" in ssh(host, "echo SSH_READY", 15):
                return True
        except Exception:
            pass
        time.sleep(8)
    return False


def order_vm(c, label, size="nvme-1c-4gb"):
    pkg, pr = resolve_size(size)
    hostname = f"tg-timing-{uuid.uuid4().hex[:5]}"
    r = c.submit_order(package_id=pkg, pricing_id=pr, hostname=hostname,
                       ssh_key=Path(THROWKEY + ".pub").read_text().strip(),
                       include_dev_vps_options=False, check_credit=True)
    if r.get("invoice_id"):
        c.pay_invoice(r["invoice_id"])
    sids = r.get("service_ids") or ([r["service_id"]] if r.get("service_id") else [])
    sid = int(sids[0])
    vm = c.wait_for_provisioning(sid, timeout=600, interval=10)
    host = vm["ips"][0]["ip"] if vm.get("ips") else ""
    c.apply_ssh_key_live(sid, Path(THROWKEY + ".pub").read_text().strip())
    return sid, host, hostname


def main():
    if not Path(THROWKEY + ".pub").exists():
        print("ERROR: run ssh-keygen first"); return 2
    c = SHCClient()
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    outdir = NOTES / f"timing-hostkeys-{ts}"
    outdir.mkdir(parents=True, exist_ok=True)
    results = {"timestamp": ts, "vms": []}
    sids = []

    try:
        # --- VM #1: cloud-init timing poll ---
        print("=== ordering NVMe VM #1 (timing poll) ===")
        sid1, host1, name1 = order_vm(c, "timing")
        sids.append(sid1)
        if not wait_ssh(host1):
            print("VM #1 SSH failed"); return 5
        print(f"VM #1 ready at {host1}; polling cloud-init status every 10s for 5 min...")

        timing_log = []
        for i in range(30):  # 5 min, every 10s
            status = ssh(host1, "sudo cloud-init status 2>&1; echo \"rc=$?\"")
            elapsed = i * 10
            timing_log.append(f"[+{elapsed:03d}s] {status}")
            print(f"  [+{elapsed:03d}s] {status[:80]}")
            if "done" in status.lower() or "error" in status.lower() or "disabled" in status.lower():
                # cloud-init reached a terminal state; do a few more polls then stop
                for j in range(3):
                    time.sleep(10)
                    s2 = ssh(host1, "sudo cloud-init status 2>&1; echo \"rc=$?\"")
                    timing_log.append(f"[+{(i+j+1)*10:03d}s] {s2}")
                    print(f"  [+{(i+j+1)*10:03d}s] {s2[:80]}")
                break
            time.sleep(10)

        (outdir / "cloud-init-timing.txt").write_text("\n".join(timing_log))
        results["vm1"] = {"sid": sid1, "ip": host1, "hostname": name1}

        # After timing poll, check if vendor-data hardening applied
        print("\n=== checking vendor-data hardening on VM #1 ===")
        hardening = {
            "auditd": ssh(host1, "systemctl is-active auditd 2>&1"),
            "qemu_guest_agent": ssh(host1, "systemctl is-active qemu-guest-agent 2>&1"),
            "password_auth": ssh(host1, "sudo grep -i '^PasswordAuthentication' /etc/ssh/sshd_config 2>&1 || echo 'not set'"),
            "permit_root": ssh(host1, "sudo grep -i '^PermitRootLogin' /etc/ssh/sshd_config 2>&1 || echo 'not set'"),
        }
        (outdir / "hardening-check-vm1.txt").write_text(json.dumps(hardening, indent=2))
        for k, v in hardening.items():
            print(f"  {k}: {v}")

        # Capture host keys from VM #1
        keys1 = ssh(host1, "sudo ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub 2>&1; sudo ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub 2>&1; sudo cat /etc/ssh/ssh_host_ed25519_key.pub 2>&1")
        (outdir / "hostkeys-vm1.txt").write_text(keys1)

        # --- VM #2: host key uniqueness comparison ---
        print("\n=== ordering NVMe VM #2 (host key comparison) ===")
        sid2, host2, name2 = order_vm(c, "hostkeys")
        sids.append(sid2)
        if not wait_ssh(host2):
            print("VM #2 SSH failed; skipping host key comparison")
        else:
            print(f"VM #2 ready at {host2}; capturing host keys...")
            time.sleep(15)  # give cloud-init time to finish key generation
            keys2 = ssh(host2, "sudo ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub 2>&1; sudo ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub 2>&1; sudo cat /etc/ssh/ssh_host_ed25519_key.pub 2>&1")
            (outdir / "hostkeys-vm2.txt").write_text(keys2)
            results["vm2"] = {"sid": sid2, "ip": host2, "hostname": name2}

            # Compare
            print("\n=== host key comparison ===")
            fp1 = [l for l in keys1.splitlines() if "SHA256" in l]
            fp2 = [l for l in keys2.splitlines() if "SHA256" in l]
            print(f"  VM #1 fingerprints: {fp1}")
            print(f"  VM #2 fingerprints: {fp2}")
            if fp1 and fp2 and fp1 == fp2:
                verdict = "DUPLICATE: both VMs have identical SSH host key fingerprints!"
                print(f"  ⚠️  {verdict}")
            elif fp1 and fp2:
                verdict = "UNIQUE: host key fingerprints differ between VMs (good)"
                print(f"  ✅ {verdict}")
            else:
                verdict = "INCONCLUSIVE: could not capture fingerprints from both VMs"
                print(f"  ❓ {verdict}")
            (outdir / "hostkey-verdict.txt").write_text(verdict)

        (outdir / "SUMMARY.json").write_text(json.dumps(results, indent=2))
        print(f"\nresults saved to {outdir}")
        return 0

    finally:
        for sid in sids:
            if sid:
                print(f"cancelling {sid}...")
                try: c.cancel_vm(sid, immediate=True); print("  cancelled")
                except Exception as e: print(f"  cancel failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
