# Firecracker Pool Mode — Proof of Concept

Live-measured data validating the future Firecracker backend for the
ephemeral GitHub Actions runner wedge. All numbers taken on
`Amperstrand/shc-toolkit` SHC Dev VPS (2026-07-04, US-Katy-Texas).

## Headline

A pool of Firecracker microVMs on a long-lived SHC Dev VPS host spawns
**1 μVM in 2 s, 4 μVMs concurrently in 2.7 s wall** — vs **100 s** for
the current "full VPS per job" model. That's a **~50× single-job speedup**
and **~150× throughput at parallelism 4**.

## Architecture

```
Today (full VPS per job):
   per job: order SHC VPS → wait 100s → SSH → bootstrap runner → run → cancel
   cost:    ~$0.01/job prorated

Future pool mode (long-lived host + μVMs):
   host:    one always-on SHC Dev VPS (e.g. dev-8c-32gb, $1.78/day)
   per job: spawn μVM via Firecracker API → 2s boot → runner inside μVM → run → kill μVM
   cost:    ~$0.0002/job (2s prorated from $1.78/day) + host prorated
```

The host VM is the only thing paying the 100s SHC scheduling tax. Once
running, it serves μVMs at ~2 s each, scaling linearly with vCPU count.

## Phase 2 — single μVM boot timing

Linux 6.1 LTS kernel built on the SHC Dev VPS itself
(`dev-4c-16gb`, GCC 13.3, 5.3 min build), using Firecracker's published
`microvm-kernel-ci-x86_64-6.1.config`. Booted via Firecracker v1.9.1 with
Alpine 3.20 mini rootfs.

| Event | Time |
|---|---|
| Firecracker process start → "Successfully started microvm" | **23 ms** |
| Kernel first message | +0 ms (parallel with FC setup) |
| Kernel reached `Run /sbin/init as init process` | **1.10 s** from kernel start |
| Total Firecracker wall (start → μVM ready for userspace) | **~1.14 s** |

For comparison, AWS publishes 125 ms Firecracker boot on dedicated
hardware. SHC's nested KVM (L2 virt) measures 1.1 s — about 9× slower
than bare metal but **88× faster than the 100 s SHC VPS scheduling floor**.

## Phase 3 — concurrency scaling

`scripts/firecracker-pool-bench.py` spawns N μVMs concurrently on a
single `dev-4c-16gb` host (4 vCPU / 16 GB). Each μVM gets 1 vCPU / 256 MB
RAM, its own CoW copy of the Alpine rootfs, its own Firecracker process
and API socket. Boot is timed per-μVM via console polling for the kernel's
`Run /sbin/init` message.

| Concurrent μVMs | Wall (s) | Per-μVM wall (s) | Boot→init min/avg/max (s) | Throughput |
|---|---|---|---|---|
| 1 | 2.60 | 2.60 | 2.08 / 2.08 / 2.08 | 0.38 μVM/s |
| 2 | 2.49 | 1.25 | 1.90 / 1.93 / 1.96 | 0.80 μVM/s |
| 4 | 2.67 | 0.67 | 1.96 / 2.06 / 2.13 | **1.50 μVM/s** |

**Key observations**:

1. **Boot time stays flat at ~2 s** regardless of concurrency. Firecracker
   μVMs are isolated; vCPU contention doesn't materially slow boot at
   these counts.
2. **Throughput scales linearly**: N=1→2→4 gives 0.38→0.80→1.50 μVM/s.
   At N=4 (one μVM per host core), per-μVM wall is just 0.67 s.
3. Slight variance (1.90–2.13 s) is rootfs I/O contention — each μVM
   starts with a fresh 512 MB ext4 copy. A snapshot-backed rootfs
   (single read-only base + overlay-per-μVM) would eliminate this.

## Cost model comparison

For a workload of **100 jobs/day**:

| Model | Cold-start / job | Cost / job | Cost / day |
|---|---|---|---|
| Full VPS per job (current) | 100 s | ~$0.01 | ~$1.00 |
| Pool of 1 host + μVMs | ~2 s | ~$0.0002 + host/100 | ~$1.78 (host only) |
| Pool of 1 host + μVMs (1000 jobs/day) | ~2 s | ~$0.00002 + host/1000 | ~$1.78 |

The pool model breaks even with full-VPS-per-job at ~178 jobs/day on a
single `dev-8c-32gb` host, then wins decisively above that. The cold-start
win is constant (50×) at any volume.

## What's NOT in this PoC

- **Networking inside μVMs**: not configured. Real runner registration
  needs outbound HTTPS to api.github.com. Standard fix: TAP device per
  μVM + NAT on the host, ~10 lines of `ip` commands. Documented in
  Firecracker's `docs/network-setup.md`.
- **Actions-runner inside μVM**: not installed. The Alpine mini-rootfs
  uses musl libc; actions-runner is glibc. Need a Debian/Ubuntu rootfs
  (~150 MB via `debootstrap --variant=minbase`). Build time ~90 s, done
  once per host VM lifetime.
- **Pool orchestrator**: not built. The benchmark script does the
  spawn-and-time; a real orchestrator would expose `spawn(label) →
  service_id`, `kill(label)`, `list()` over a Unix socket or HTTP API.
- **Webhook autoscaler integration**: not built. The natural path is
  GitHub `workflow_job` webhook → orchestrator.spawn(label) → μVM
  registers with that label → job runs → orchestrator.kill(label).

## How to reproduce

```bash
# 1. Provision an SHC Dev VPS (nested KVM required)
shc order --hostname fc-host --size dev-4c-16gb --template ubuntu2404-cloud --pay

# 2. SSH in and run the kernel build + boot test (one-time, ~6 min)
sudo apt-get install -y build-essential bc bison flex libelf-dev libssl-dev git curl
git clone --depth 1 --branch v6.1 https://github.com/torvalds/linux.git /usr/src/linux-6.1
cd /usr/src/linux-6.1
curl -fsSL https://raw.githubusercontent.com/firecracker-microvm/firecracker/main/resources/guest_configs/microvm-kernel-ci-x86_64-6.1.config > .config
echo "CONFIG_EXT4_FS=y" >> .config && make olddefconfig
make vmlinux -j4   # ~5 min on dev-4c-16gb

# 3. Install Firecracker + Alpine rootfs
curl -fsSL https://github.com/firecracker-microvm/firecracker/releases/download/v1.9.1/firecracker-v1.9.1-x86_64.tgz | tar xz
sudo mv release-v1.9.1-x86_64/firecracker-v1.9.1-x86_64 /usr/local/bin/firecracker
dd if=/dev/zero of=/tmp/rootfs.ext4 bs=1M count=512
mkfs.ext4 /tmp/rootfs.ext4 && sudo mount -o loop /tmp/rootfs.ext4 /mnt
curl -fsSL https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/alpine-minirootfs-3.20.3-x86_64.tar.gz | sudo tar xz -C /mnt
sudo umount /mnt

# 4. Run the pool benchmark
sudo python3 scripts/firecracker-pool-bench.py --count 4
```

## Roadmap from PoC → production

1. **Rootfs with runner pre-baked**: Debian minbase + actions-runner + deps.
   ~150 MB ext4 image, built once per host VM.
2. **Per-μVM networking**: TAP + NAT. Standard Firecracker pattern.
3. **Pool orchestrator**: long-lived daemon exposing `spawn` / `kill` /
   `list`. ~200 LOC Python.
4. **Webhook autoscaler**: GitHub App subscribing to `workflow_job` →
   calls orchestrator. Replaces in-workflow `provision-shc-runner` job.
5. **Snapshot-backed rootfs**: single read-only base, per-μVM overlay.
   Eliminates the 512 MB rootfs copy per spawn → boot drops further.
