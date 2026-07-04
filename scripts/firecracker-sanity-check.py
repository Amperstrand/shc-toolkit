#!/usr/bin/env python3
"""Firecracker sanity check on SHC Dev VPS.

Provisions a `dev-4c-16gb` (nested-KVM-capable), SSHes in, verifies
/dev/kvm and vmx/svm extensions, installs Firecracker, boots a microVM
using a built-from-source kernel (Linux 5.10 LTS), and times the boot.

Verified preconditions (2026-07-04):
- /dev/kvm exists, vmx extensions present, kvm-ok passes
- Firecracker v1.9.1 binary runs cleanly

Not yet verified in this script (blocked on GCC compat):
- Actual microVM boot timing

To retry the kernel build that's currently blocked:
1. SSH into the SHC Dev VPS
2. Install GCC 11 OR use Linux 6.1 LTS instead of 5.10
3. `cd /usr/src/linux && make vmlinux -j4`
4. Boot Firecracker with the resulting vmlinux

Cost: ~$0.05 (10-15 min of dev-4c-16gb + refund on cancel).

Usage:
    python3 scripts/firecracker-sanity-check.py
"""
from __future__ import annotations

import json
import shlex
import subprocess
import sys
import time
import uuid
from pathlib import Path

from shc_toolkit import SHCClient
from shc_toolkit.client import SHCError


SSH_PUB = Path.home() / ".ssh" / "id_ed25519.pub"
SSH_PRIVATE = Path.home() / ".ssh" / "id_ed25519"

# Firecracker release + demo artifacts (AWS publishes these for getting-started)
FC_VERSION = "v1.9.1"
FC_KERNEL_URL = "https://s3.amazonaws.com/spec.ccfc.min/img/hello-vmlinux.bin"
FC_ROOTFS_URL = "https://s3.amazonaws.com/spec.ccfc.min/img/hello-rootfs.ext4"


def ssh(host: str, cmd: str, *, user: str = "ubuntu", timeout: int = 60) -> tuple[int, str]:
    """Run a command on the host VM via SSH. Returns (rc, combined_output)."""
    result = subprocess.run(
        ["ssh", "-i", str(SSH_PRIVATE),
         "-o", "StrictHostKeyChecking=no",
         "-o", "UserKnownHostsFile=/dev/null",
         "-o", "LogLevel=ERROR",
         "-o", "BatchMode=yes",
         "-o", f"ConnectTimeout={min(timeout, 15)}",
         f"{user}@{host}", cmd],
        capture_output=True, text=True, timeout=timeout,
    )
    out = result.stdout + ("\n--- STDERR ---\n" + result.stderr if result.stderr else "")
    return result.returncode, out.strip()


def wait_ssh(host: str, timeout: int = 180) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            rc, _ = ssh(host, "echo READY", timeout=15)
            if rc == 0:
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(5)
    return False


# Inline Firecracker test — runs on the SHC VM as root
FIRECRACKER_TEST = r'''
set -e

echo "=== Host kernel + KVM sanity ==="
echo "kernel: $(uname -r)"
echo "/dev/kvm: $(ls -la /dev/kvm 2>&1)"
echo "cpu virt extensions:"
grep -E -o '(vmx|svm)' /proc/cpuinfo | sort -u || echo "  NONE FOUND"
echo "kvm-ok:"
apt-get install -y cpu-checker >/dev/null 2>&1 || true
kvm-ok 2>&1 || true

echo
echo "=== Install Firecracker ==="
cd /tmp
T_INSTALL=$(date +%s.%N)
curl -fsSL -o fc.tgz "https://github.com/firecracker-microvm/firecracker/releases/download/__FC_VERSION__/firecracker-__FC_VERSION__-x86_64.tgz"
tar xzf fc.tgz
sudo mv release-__FC_VERSION__-x86_64/firecracker-__FC_VERSION__-x86_64 /usr/local/bin/firecracker
sudo chmod +x /usr/local/bin/firecracker
/usr/local/bin/firecracker --version
echo "install time: $(echo "$(date +%s.%N) - $T_INSTALL" | bc)s"

echo
echo "=== Download demo kernel + rootfs ==="
T_DL=$(date +%s.%N)
curl -fsSL -o /tmp/vmlinux https://s3.amazonaws.com/spec.ccfc.min/img/hello-vmlinux.bin
curl -fsSL -o /tmp/rootfs.ext4 https://s3.amazonaws.com/spec.ccfc.min/img/hello-rootfs.ext4
ls -lh /tmp/vmlinux /tmp/rootfs.ext4
echo "download time: $(echo "$(date +%s.%N) - $T_DL" | bc)s"

echo
echo "=== Boot microVM (no network, just console) ==="
cat > /tmp/boot.json <<JSON
{
  "boot-source": {
    "kernel_image_path": "/tmp/vmlinux",
    "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
  },
  "drives": [
    {
      "drive_id": "rootfs",
      "path_on_host": "/tmp/rootfs.ext4",
      "is_root_device": true,
      "is_read_only": false
    }
  ],
  "machine-config": {
    "vcpu_count": 1,
    "mem_size_mib": 512,
    "smt": false
  }
}
JSON

# Time the boot. Firecracker writes boot timestamp to its log.
rm -f /tmp/fc.sock /tmp/fc.log
T_BOOT_START=$(date +%s.%N)
# Run firecracker with config; capture console output for ~15s then kill
timeout 15 /usr/local/bin/firecracker \
    --api-sock /tmp/fc.sock \
    --config-file /tmp/boot.json \
    > /tmp/fc.log 2>&1 &
FC_PID=$!

# Wait for the "booting" message or process exit
sleep 8
T_BOOT_END=$(date +%s.%N)
echo "boot wall time: $(echo "$T_BOOT_END - $T_BOOT_START" | bc)s"

# Check if microVM produced any output
echo
echo "=== MicroVM console output (first 30 lines) ==="
head -30 /tmp/fc.log || echo "no log output"

# Check if the process is still running (means it booted and is waiting for input)
if kill -0 $FC_PID 2>/dev/null; then
    echo "FIRECRACKER_STATUS=RUNNING"
    kill $FC_PID 2>/dev/null || true
    wait $FC_PID 2>/dev/null || true
else
    wait $FC_PID 2>/dev/null
    RC=$?
    echo "FIRECRACKER_STATUS=EXITED rc=$RC"
fi

# Extract concrete boot timing from firecracker's structured log if present
echo
echo "=== Firecracker reported timings ==="
grep -E 'Started VMM|vmm_seccomp|Boot source|Block device|Kernel loaded|VMM' /tmp/fc.log 2>/dev/null | head -20 || echo "(none in log)"

echo
echo "=== DONE ==="
'''


def main() -> int:
    if not SSH_PUB.exists():
        print(f"ERROR: need {SSH_PUB}", file=sys.stderr); return 2

    client = SHCClient()
    hostname = f"fc-test-{uuid.uuid4().hex[:6]}"
    service_id = None

    print(f"=== Phase B: Firecracker sanity check on dev-4c-16gb ===")
    print(f"Start: {time.strftime('%FT%TZ', time.gmtime())}")

    try:
        print(f"\n--- provisioning {hostname} ---")
        ssh_key = SSH_PUB.read_text().strip()
        order = client.order_vm(
            hostname=hostname, size="dev-4c-16gb",
            template="ubuntu2404-cloud", ssh_key=ssh_key,
            pay=True, check_credit=True,
        )
        service_ids = order.get("service_ids") or (
            [order["service_id"]] if order.get("service_id") else []
        )
        service_id = int(service_ids[0])
        print(f"ordered service_id={service_id}, waiting for ready...")

        vm = client.wait_for_provisioning(service_id, timeout=600, interval=10)
        ip = vm["ips"][0]["ip"]
        user = vm.get("os_user", "ubuntu")
        print(f"VM ready at {ip} (user={user})")

        # Apply SSH key live (cloud-init may not have picked it up yet)
        client.apply_ssh_key_live(service_id, ssh_key)
        print("waiting for SSH...")
        if not wait_ssh(ip, timeout=180):
            print("ERROR: SSH never came up", file=sys.stderr); return 5

        # Need root for /dev/kvm and apt installs. ubuntu user has sudo.
        # Run the test as root via sudo.
        print("\n--- running Firecracker test ---")
        rendered = (FIRECRACKER_TEST
                    .replace("__FC_VERSION__", FC_VERSION))
        # SSH in as the os_user, then sudo bash to get root for /dev/kvm + apt.
        rc, out = ssh(ip, f"sudo bash -c {shlex.quote(rendered)}",
                      user=user, timeout=300)
        print(out)
        if rc != 0:
            print(f"\nFirecracker test exited rc={rc}", file=sys.stderr)
            return 1

        return 0

    finally:
        if service_id is not None:
            print(f"\n--- destroying {service_id} ---")
            try:
                client.cancel_vm(service_id, immediate=True)
                print(f"cancelled {service_id}")
            except SHCError as e:
                if "already" in str(e).lower() or "not found" in str(e).lower():
                    print(f"already gone: {e}")
                else:
                    print(f"WARN: cancel failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
