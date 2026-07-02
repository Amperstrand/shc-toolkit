"""Comprehensive tenant-VM reconnaissance for the SHC security audit.

Orders ONE NVMe VM (production tier, cloud-init runs), SSHes in, and captures
a broad set of diagnostics to surface 'known unknowns' about SHC's
infrastructure, network, provisioning, and security posture.

All output is saved to notes/recon-<timestamp>/ for the authorized pen-test
record. Always cancels the VM.
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
    return r.stdout if r.returncode == 0 else f"<rc={r.returncode}> {r.stderr}"


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


# Each probe: (filename, command, timeout)
PROBES = [
    # System identity
    ("01-system-info.txt", "uname -a; echo '---'; cat /etc/os-release; echo '---'; uptime; echo '---'; free -h; echo '---'; nproc; echo '---'; df -h", 15),
    ("02-dmesg-proxmox.txt", "sudo dmesg 2>/dev/null | grep -iE 'proxmox|qemu|kvm|hyperv|xen|vmware' | head -30", 15),
    # Network — the core of "router configuration / provisioning"
    ("03-ip-addr.txt", "ip -o addr show", 10),
    ("04-ip-route.txt", "ip route show; echo '---'; ip -6 route show 2>/dev/null | head -10", 10),
    ("05-arp-neighbors.txt", "ip neigh show; echo '---'; arp -an 2>/dev/null", 10),
    ("06-resolv-conf.txt", "cat /etc/resolv.conf", 5),
    ("07-network-interfaces.txt", "ls -la /sys/class/net/; echo '---'; for i in /sys/class/net/*; do echo \"== $(basename $i) ==\"; cat $i/address 2>/dev/null; cat $i/mtu 2>/dev/null; done", 10),
    # Metadata service — does SHC have one (like AWS/GCP IMDS)?
    ("08-metadata-service.txt", "curl -s -m 3 http://169.254.169.254/ 2>&1 || echo 'no response'; echo '---'; curl -s -m 3 http://169.254.169.254/latest/meta-data/ 2>&1 || echo 'no AWS-style'; echo '---'; curl -s -m 3 -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/ 2>&1 || echo 'no GCP-style'", 15),
    # Gateway probe — what is at .1?
    ("09-gateway-probe.txt", "GATEWAY=$(ip route | awk '/default/{print $3; exit}'); echo \"gateway: $GATEWAY\"; curl -s -m 3 http://$GATEWAY/ 2>&1 | head -20 || echo 'no http'; echo '---'; ping -c 2 -W 2 $GATEWAY 2>&1", 15),
    # Cloud-init state
    ("10-cloud-init-status.txt", "sudo cloud-init status --long 2>&1", 15),
    ("11-cloud-init-cfg.txt", "cat /etc/cloud/cloud.cfg 2>/dev/null | head -60; echo '=== cfg.d ==='; ls /etc/cloud/cloud.cfg.d/ 2>/dev/null; echo '=== disabled? ==='; ls -la /etc/cloud/cloud-init.disabled* 2>/dev/null || echo 'no marker'", 10),
    ("12-seed-disk-userdata.txt", "sudo mkdir -p /mnt/seed; sudo mount /dev/sr0 /mnt/seed 2>/dev/null; sudo cat /mnt/seed/user-data 2>&1", 10),
    ("13-seed-disk-vendordata.txt", "sudo cat /mnt/seed/vendor-data 2>&1", 10),
    ("14-seed-disk-metadata.txt", "sudo cat /mnt/seed/meta-data 2>&1; echo '---'; sudo cat /mnt/seed/network-config 2>&1", 10),
    # SSH security posture
    ("15-sshd-config.txt", "sudo grep -vE '^#|^$' /etc/ssh/sshd_config 2>/dev/null; echo '=== drop-ins ==='; sudo grep -rvE '^#|^$' /etc/ssh/sshd_config.d/ 2>/dev/null | head -30; echo '=== host keys ==='; sudo ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub 2>/dev/null; sudo ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub 2>/dev/null", 15),
    # Security hardening
    ("16-security-baseline.txt", "systemctl is-active auditd 2>&1; echo '---'; systemctl is-active apparmor 2>&1; echo '---'; systemctl is-active ufw 2>&1; echo '---'; systemctl is-active fail2ban 2>&1; echo '---'; sudo auditctl -l 2>/dev/null | head -20; echo '---'; sudo aa-status 2>/dev/null | head -10", 15),
    # qemu-guest-agent — the host<->guest channel
    ("17-qemu-guest-agent.txt", "systemctl status qemu-guest-agent 2>&1 | head -15; echo '=== config ==='; cat /etc/systemd/system/qemu-guest-agent.service.d/*.conf 2>/dev/null; echo '=== log ==='; sudo tail -20 /var/log/qemu-guest-agent.log 2>/dev/null || echo 'no log'", 15),
    # SHC-specific tooling
    ("18-shc-packages.txt", "dpkg -l 2>/dev/null | grep -iE 'shc|sovereign|blesta|tollgate' || echo 'no SHC-specific packages'; echo '=== all packages ==='; dpkg -l 2>/dev/null | awk '{print $2}' | sort", 15),
    # Users and access
    ("19-users-groups.txt", "cat /etc/passwd | grep -v nologin | grep -v false; echo '=== sudoers ==='; sudo cat /etc/sudoers 2>/dev/null | grep -vE '^#|^$'; sudo ls /etc/sudoers.d/ 2>/dev/null; echo '=== ssh keys ==='; cat ~/.ssh/authorized_keys 2>/dev/null; sudo cat /root/.ssh/authorized_keys 2>/dev/null || echo 'no root keys'", 15),
    # Cron and timers — any SHC scheduled tasks?
    ("20-cron-timers.txt", "sudo crontab -l 2>/dev/null; echo '=== cron.d ==='; sudo ls /etc/cron.d/ 2>/dev/null; echo '=== systemd timers ==='; systemctl list-timers --all 2>&1 | head -20", 15),
    # Proxmox/hypervisor detection
    ("21-hypervisor-detection.txt", "sudo virt-what 2>/dev/null || echo 'no virt-what'; echo '---'; systemd-detect-virt 2>/dev/null; echo '---'; cat /sys/hypervisor/type 2>/dev/null || echo 'no /sys/hypervisor'; echo '---'; sudo dmesg 2>/dev/null | grep -i 'BIOS\\|hypervisor\\|KVM\\|QEMU' | head -10", 15),
    # iptables/nftables — firewall rules
    ("22-firewall-rules.txt", "sudo iptables -L -n 2>&1 | head -30; echo '=== nft ==='; sudo nft list ruleset 2>&1 | head -30", 15),
    # Processes — what's running?
    ("23-processes.txt", "ps aux --sort=-%mem | head -30", 10),
    # Open ports
    ("24-open-ports.txt", "ss -tlnp 2>/dev/null | head -20", 10),
]


def main():
    if not Path(THROWKEY + ".pub").exists():
        print("ERROR: run ssh-keygen first"); return 2
    c = SHCClient()
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    outdir = NOTES / f"recon-nvme-{ts}"
    outdir.mkdir(parents=True, exist_ok=True)
    hostname = f"tg-recon-{uuid.uuid4().hex[:5]}"
    sid = None
    try:
        pkg, pr = resolve_size("nvme-1c-4gb")
        print(f"ordering NVMe recon VM ({hostname})...")
        r = c.submit_order(package_id=pkg, pricing_id=pr, hostname=hostname,
                           ssh_key=Path(THROWKEY + ".pub").read_text().strip(),
                           include_dev_vps_options=False, check_credit=True)
        if r.get("invoice_id"):
            c.pay_invoice(r["invoice_id"])
        sids = r.get("service_ids") or ([r["service_id"]] if r.get("service_id") else [])
        sid = int(sids[0])
        print(f"service_id={sid}; provisioning...")
        vm = c.wait_for_provisioning(sid, timeout=600, interval=10)
        host = vm["ips"][0]["ip"] if vm.get("ips") else ""
        print(f"ready at {host}; applying key...")
        c.apply_ssh_key_live(sid, Path(THROWKEY + ".pub").read_text().strip())
        if not wait_ssh(host):
            print("SSH failed; aborting recon"); return 5
        print(f"SSH up; running {len(PROBES)} probes; saving to {outdir}")
        (outdir / "META.json").write_text(json.dumps({
            "service_id": sid, "hostname": hostname, "ip": host,
            "tier": "nvme-1c-4gb", "timestamp": ts,
            "probe_count": len(PROBES),
        }, indent=2))
        for fname, cmd, timeout in PROBES:
            print(f"  {fname}...", end=" ", flush=True)
            out = ssh(host, cmd, timeout)
            (outdir / fname).write_text(out)
            print(f"{len(out)} bytes")
        print(f"\nrecon complete: {outdir}")
        return 0
    finally:
        if sid:
            print(f"cancelling {sid}...")
            try: c.cancel_vm(sid, immediate=True); print("  cancelled")
            except Exception as e: print(f"  cancel failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
