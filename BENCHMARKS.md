# SHC VPS Benchmarks

Performance comparison across providers, measured with our `shc_toolkit.benchmark` suite (YABS-modeled: sysbench CPU, fio disk, openssl, memory, network).

Last updated: 2026-06-22

## Summary

| Provider | Instance | CPU ST | CPU MT | Mem (MiB/s) | Rand 4K IOPS | $/day | Nested KVM |
|---|---|---|---|---|---|---|---|
| **SHC Dev VPS** | Standard (2C/8GB) | 435 | 849 | 6,550 | **117,878** | $0.49 | ✅ |
| **SHC NVMe VPS** | Standard (2C/8GB) | 451 | 898 | 6,549 | 44,527 | $0.49 | ❌ |
| **Hetzner** | CX22 (2C/4GB) | **602** | **1192** | 5,690 | 47,301 | ~$0.15 | ❌ |
| **GCP** | e2-standard-2 (2C/8GB) | 4,340¹ | 4,340¹ | N/A | 56,200¹ | ~$1.63 | ✅² |

¹ Published numbers from [vpsbenchmarks.com](https://vpsbenchmarks.com/yabs/google_compute_engine-2c-4gb-49d111) — not measured by us.
² GCP nested virtualization requires `--enable-nested-virtualization` flag on the instance template.

## Detailed results

### SHC Dev VPS Standard (VM 609)

| Metric | Value | Notes |
|---|---|---|
| **CPU** | Intel Xeon Skylake | Real silicon (not virtualized) |
| **vCPUs** | 2 | |
| **sysbench ST** | 435 events/s | |
| **sysbench MT** | 849 events/s | |
| **Memory read** | 6,550 MiB/s | |
| **Rand 4K Read IOPS** | 117,878 | **2.5x Hetzner, 2.7x SHC NVMe** |
| **Rand 4K Read latency** | 271 µs | |
| **Location** | Parsons, Kansas | AS394468 Wave Wireless LLC |
| **Nested KVM** | ✅ /dev/kvm with VMX flags | Required for tollgate router testing |
| **Disk** | 16 GB | |
| **Kernel** | 6.12.90+deb13.1-cloud-amd64 | Debian 13 |

### SHC NVMe VPS Standard (VM 608)

| Metric | Value | Notes |
|---|---|---|
| **CPU** | QEMU Virtual CPU 2.5+ | Virtualized |
| **vCPUs** | 2 | |
| **sysbench ST** | 451 events/s | |
| **sysbench MT** | 898 events/s | |
| **Memory read** | 6,549 MiB/s | |
| **Rand 4K Read IOPS** | 44,527 | |
| **Rand 4K Read latency** | 718 µs | |
| **Location** | Houston, Texas | AS401933 HashIT |
| **Nested KVM** | ❌ | NVMe VPS does not expose VMX/SVM |
| **Template support** | 37 OS templates | Config option 126 |

### Hetzner CX22 (nodns.shop)

| Metric | Value | Notes |
|---|---|---|
| **CPU** | AMD EPYC-Rome | |
| **vCPUs** | 2 | |
| **sysbench ST** | 602 events/s | **+33% vs SHC** |
| **sysbench MT** | 1192 events/s | **+40% vs SHC** |
| **Memory read** | 5,690 MiB/s | -13% vs SHC |
| **Rand 4K Read IOPS** | 47,301 | |
| **Rand 4K Read latency** | 676 µs | |
| **Location** | Falkenstein, Germany | AS24940 Hetzner |
| **Nested KVM** | ❌ | |
| **Disk** | 38 GB | |

## Pricing comparison

| Provider | Instance | $/day | $/month | vCPU | RAM | Disk | Nested KVM |
|---|---|---|---|---|---|---|---|
| **SHC Dev VPS** | Standard | $0.49 | $14.83 | 2 | 8 GB | 16 GB | ✅ |
| **SHC NVMe VPS** | Standard | $0.49 | $14.83 | 2 | 8 GB | 16 GB | ❌ |
| **Hetzner** | CX22 | ~$0.15 | $4.59 | 2 | 4 GB | 40 GB | ❌ |
| **GCP** | e2-standard-2 | ~$1.63 | $48.92 | 2 | 8 GB | pd-ssd | ✅ (flag) |

SHC Dev VPS is **3.3x cheaper** than GCP for the same specs + nested KVM.
Hetzner is **3.2x cheaper** than SHC but lacks nested KVM and has half the RAM.

## Provisioning time comparison

| Provider | Order → SSH ready | Notes |
|---|---|---|
| **SHC Dev VPS** | ~90 seconds | Fastest of all providers tested |
| **SHC NVMe VPS** | ~120 seconds | |
| **GCP** | ~120 seconds | From baked snapshot (instant deps) |
| **Hetzner** | ~15 seconds | Fastest provisioning |

## CI cycle time comparison

| Step | GCP (baked snapshot) | SHC (fresh VM) | SHC (with snapshot restore) |
|---|---|---|---|
| Order VM | ~2 min | ~1.5 min | ~1.5 min |
| Restore snapshot | N/A | N/A | ~5 sec |
| Install deps | 0 (baked) | ~5 min | 0 (snapshot) |
| Download images | 0 (baked) | ~2 min | 0 (snapshot) |
| Deploy worker | ~0.5 min | ~0.5 min | ~0.5 min |
| **Total to test-ready** | **~2.5 min** | **~9 min** | **~2 min** |
| Run quick tests | ~5 min | ~5 min | ~5 min |
| **Full cycle** | **~7.5 min** | **~14 min** | **~7 min** |

SHC with snapshot restore matches GCP's cycle time. Without snapshots, SHC adds ~6.5 min of setup per run.

## Benchmarking methodology

Our benchmark suite (`shc_toolkit.benchmark`) uses:

- **CPU**: `sysbench cpu --cpu-max-prime=20000 --threads=1` (single) and `--threads=$(nproc)` (multi)
- **CPU crypto**: `openssl speed -seconds 3 rsa2048 aes-256-cbc`
- **Disk**: `fio` with 4 profiles:
  - Sequential read: `--rw=read --bs=1M --size=1G --iodepth=32`
  - Sequential write: `--rw=write --bs=1M --size=1G --iodepth=32`
  - Random 4K read: `--rw=randread --bs=4K --size=1G --iodepth=32`
  - Random 4K write: `--rw=randwrite --bs=4K --size=1G --iodepth=32`
- **Memory**: `sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=read`
- **Network**: 100MB download from Cloudflare speed test

All tests use `--direct=1` (bypass page cache) and `--ioengine=libaio`.

## Running benchmarks

```bash
# On any SHC VM:
shc bench <service_id>

# Or directly:
python3 -m shc_toolkit.benchmark <host> [--user <user>] [--port <port>]
```

Results are saved to `benchmark_results/bench_<host>_<timestamp>.json`.

## Updating this file

Re-run benchmarks when:
- SHC announces infrastructure changes
- Monthly cadence for trend tracking
- Before/after any provider migration decision
- When comparing new instance types

```bash
# Generate fresh comparison:
python3 -c "
from shc_toolkit.benchmark import run_full_suite, print_results
# Dev VPS
r1 = run_full_suite('66.92.204.238', user='debian', port=22)
# NVMe VPS
r2 = run_full_suite('<nvme-ip>', user='ubuntu', port=22)
# Hetzner
r3 = run_full_suite('nodns.shop', user='root', port=22)
"
```
