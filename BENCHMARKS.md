# SHC VPS Benchmarks

Raw performance data across providers, measured with our `shc_toolkit.benchmark` suite (YABS-compatible: sysbench CPU, fio disk, iperf3 network, openssl, memory, optional Geekbench 6).

Last updated: 2026-06-23

## Summary

| Provider | Instance | CPU ST | CPU MT | Mem (MiB/s) | Rand 4K IOPS | $/hour | $/day | Nested KVM |
|---|---|---|---|---|---|---|---|---|
| **SHC Dev VPS** | Standard (2C/8GB) | 435 | 849 | 6,550 | 117,878 | $0.0204 | $0.49 | ✅ |
| **SHC NVMe VPS** | Standard (2C/8GB) | 451 | 898 | 6,549 | 44,527 | $0.0204 | $0.49 | ❌ |
| **Hetzner** | CX22 (2C/4GB) | 602 | 1192 | 5,690 | 47,301 | ~$0.006 | ~$0.15 | ❌ |
| **GCP** | e2-standard-2 (2C/8GB) | 4,340¹ | 4,340¹ | N/A | 56,200¹ | ~$0.068 | ~$1.63 | ✅² |

¹ Published numbers from [vpsbenchmarks.com](https://vpsbenchmarks.com/yabs/google_compute_engine-2c-4gb-49d111) — not measured by us.

² GCP nested virtualization requires `--enable-nested-virtualization` flag on the instance template.

> **Note:** GCP raised peering/CDN egress rates effective May 1, 2026.

## Detailed results

### SHC Dev VPS Standard (VM 609)

| Metric | Value | Notes |
|---|---|---|
| **CPU** | Intel Xeon Skylake | Real silicon (not virtualized) |
| **vCPUs** | 2 | |
| **sysbench ST** | 435 events/s | |
| **sysbench MT** | 849 events/s | |
| **Memory read** | 6,550 MiB/s | |
| **Rand 4K Read IOPS** | 117,878 | |
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
| **sysbench ST** | 602 events/s | |
| **sysbench MT** | 1192 events/s | |
| **Memory read** | 5,690 MiB/s | |
| **Rand 4K Read IOPS** | 47,301 | |
| **Rand 4K Read latency** | 676 µs | |
| **Location** | Falkenstein, Germany | AS24940 Hetzner |
| **Nested KVM** | ❌ | |
| **Disk** | 38 GB | |

## Pricing comparison

| Provider | Instance | $/hour | $/day | $/month | vCPU | RAM | Disk | Nested KVM |
|---|---|---|---|---|---|---|---|---|
| **SHC Dev VPS** | Standard | $0.0204 | $0.49 | $14.83 | 2 | 8 GB | 16 GB | ✅ |
| **SHC NVMe VPS** | Standard | $0.0204 | $0.49 | $14.83 | 2 | 8 GB | 16 GB | ❌ |
| **Hetzner** | CX22 | ~$0.006 | ~$0.15 | $4.59 | 2 | 4 GB | 40 GB | ❌ |
| **GCP** | e2-standard-2 | ~$0.068 | ~$1.63 | $48.92 | 2 | 8 GB | pd-ssd | ✅ (flag) |

> SHC bills per day but refunds pro-consumed. Minimum charge is 1 hour.
> Pricing source: SHC catalog API (live) — `GET https://blesta.sovereignhybridcompute.com/user-api/v2/ordering/catalog`

## Provisioning time comparison

| Provider | Order → SSH ready | Notes |
|---|---|---|
| **SHC Dev VPS** | ~90 seconds | |
| **SHC NVMe VPS** | ~120 seconds | |
| **GCP** | ~120 seconds | From baked snapshot (instant deps) |
| **Hetzner** | ~15 seconds | |

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

## Benchmarking methodology

Our benchmark suite (`shc_toolkit.benchmark`) uses:

- **Pricing source**: SHC catalog API (live) — fetched at benchmark start via `collect_pricing()`. Hetzner pricing from `https://api.hetzner.cloud/v1/pricing`.
- **CPU**: `sysbench cpu --cpu-max-prime=20000 --threads=1` (single) and `--threads=$(nproc)` (multi)
- **CPU crypto**: `openssl speed -seconds 3 rsa2048 aes-256-cbc`
- **Disk**: `fio` with 4 profiles:
  - Sequential read: `--rw=read --bs=1M --size=1G --iodepth=32`
  - Sequential write: `--rw=write --bs=1M --size=1G --iodepth=32`
  - Random 4K read: `--rw=randread --bs=4K --size=1G --iodepth=32`
  - Random 4K write: `--rw=randwrite --bs=4K --size=1G --iodepth=32`
- **Disk (YABS)**: `fio --rw=randrw --rwmixread=50 --iodepth=64 --numjobs=2 --size=2G --runtime=30` across 4k/64k/512k/1m blocksizes
- **Memory**: `sysbench memory --memory-block-size=1K --memory-total-size=10G --memory-oper=read`
- **Network**: 100MB download from Cloudflare speed test
- **Network (iperf3)**: `iperf3 -c <server> -P 8 -t 10 -J` against bouygues.testdebit.info (Paris), iperf.he.net (Fremont), speedtest.wtnet.de (Amsterdam)
- **Geekbench 6** (optional): Downloaded from cdn.geekbench.com, run with `--json`

All fio tests use `--direct=1` (bypass page cache) and `--ioengine=libaio`.

## Running benchmarks

```bash
# On any SHC VM (full suite with live pricing + YABS + iperf3):
shc bench <service_id>

# Or directly (all tests):
python3 -m shc_toolkit.benchmark <host> [--user <user>] [--port <port>]

# With optional Geekbench 6:
python3 -c "
from shc_toolkit.benchmark import run_full_suite, print_results
r = run_full_suite('<host>', user='debian', run_geekbench=True, provider='shc')
print_results(r)
"
```

Results are saved to `benchmark_results/bench_<host>_<timestamp>.json`.

## Updating this file

Re-run benchmarks when:
- SHC announces infrastructure changes
- Monthly cadence for trend tracking
- Before/after any provider migration decision
- When comparing new instance types

```bash
# Generate fresh data with live pricing:
python3 -c "
from shc_toolkit.benchmark import run_full_suite, print_results
# Dev VPS
r1 = run_full_suite('66.92.204.238', user='debian', port=22, provider='shc')
# NVMe VPS
r2 = run_full_suite('<nvme-ip>', user='ubuntu', port=22, provider='shc')
# Hetzner
r3 = run_full_suite('nodns.shop', user='root', port=22, provider='hetzner')
"
```
