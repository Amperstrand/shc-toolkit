"""
VPS benchmark suite: CPU, disk, memory, network, and system info.

Runs standard Linux benchmarking tools (sysbench, fio, openssl) over SSH
and collects structured JSON results. Results are saved locally in
benchmark_results/ (gitignored).

Modeled after YABS (Yet Another Bench Script) but implemented as a
reusable Python module with structured output.
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any

from .provision import ssh_cmd

log = logging.getLogger(__name__)

# Directory for saving benchmark results (gitignored)
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "benchmark_results")


def _ensure_results_dir() -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    return RESULTS_DIR


def _install_deps(host: str, user: str = "debian", port: int = 22) -> None:
    """Install benchmark dependencies (sysbench, fio) if missing."""
    log.info("Installing benchmark dependencies...")
    ssh_cmd(host, """
        export DEBIAN_FRONTEND=noninteractive
        need_install=""
        command -v sysbench >/dev/null 2>&1 || need_install="sysbench $need_install"
        command -v fio >/dev/null 2>&1 || need_install="fio $need_install"
        if [ -n "$need_install" ]; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq $need_install
        fi
        echo "deps ready: sysbench=$(command -v sysbench), fio=$(command -v fio)"
    """, user=user, port=port, timeout=180)


# ── System Info ───────────────────────────────────────────────


def collect_sysinfo(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Collect basic system information."""
    log.info("Collecting system info...")
    raw = ssh_cmd(host, """
        echo "=== uname ==="
        uname -a
        echo "=== cpu ==="
        lscpu | grep -E '^(Model name|CPU\\(s\\)|Thread|Core|Socket|MHz|Cache)'
        echo "=== mem ==="
        free -h | head -2
        echo "=== disk ==="
        lsblk -d -o NAME,SIZE,TYPE,ROTA,MODEL 2>/dev/null || echo "lsblk not available"
        echo "=== os ==="
        cat /etc/os-release | head -4
        echo "=== uptime ==="
        uptime
        echo "=== kernel_modules ==="
        grep -c 'vmx\\|svm' /proc/cpuinfo 2>/dev/null || echo "0"
    """, user=user, port=port)

    info: dict[str, Any] = {"raw": raw}

    # Parse structured fields
    for line in raw.splitlines():
        if line.startswith("Model name:"):
            info["cpu_model"] = line.split(":", 1)[1].strip()
        elif line.startswith("CPU(s):") and "cpu_count" not in info:
            info["cpu_count"] = int(line.split(":")[1].strip())
        elif line.startswith("Thread(s) per core:"):
            info["threads_per_core"] = int(line.split(":")[1].strip())
        elif line.startswith("Core(s) per socket:"):
            info["cores_per_socket"] = int(line.split(":")[1].strip())
        elif line.startswith("CPU MHz:"):
            info["cpu_mhz"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))
        elif line.startswith("L3 cache:"):
            info["l3_cache"] = line.split(":")[1].strip()

    info["nested_virt"] = "vmx" in raw or "svm" in raw
    info["timestamp"] = datetime.now(timezone.utc).isoformat()

    return info


# ── CPU Benchmarks ────────────────────────────────────────────


def bench_cpu(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Run CPU benchmarks: sysbench prime test + openssl speed."""
    log.info("Running CPU benchmarks...")

    # sysbench CPU — single-threaded prime calculation
    sb_out = ssh_cmd(host, """
        sysbench cpu --cpu-max-prime=20000 --threads=1 run 2>&1
    """, user=user, port=port, timeout=120)

    sb_multi = ssh_cmd(host, """
        sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) run 2>&1
    """, user=user, port=port, timeout=120)

    # openssl speed — RSA and AES
    ssl_out = ssh_cmd(host, """
        openssl speed -seconds 3 rsa2048 aes-256-cbc 2>&1
    """, user=user, port=port, timeout=60)

    result: dict[str, Any] = {}

    # Parse sysbench single-thread
    for line in sb_out.splitlines():
        if "total time:" in line.lower():
            result["sysbench_st_time_s"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))
        elif "events per second:" in line.lower():
            result["sysbench_st_eps"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))

    # Parse sysbench multi-thread
    for line in sb_multi.splitlines():
        if "total time:" in line.lower():
            result["sysbench_mt_time_s"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))
        elif "events per second:" in line.lower():
            result["sysbench_mt_eps"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))

    # Parse openssl
    for line in ssl_out.splitlines():
        parts = line.split()
        if len(parts) >= 6 and parts[0] == "rsa":
            try:
                result["openssl_rsa2048_sign_per_s"] = float(parts[2])
                result["openssl_rsa2048_verify_per_s"] = float(parts[4])
            except (ValueError, IndexError):
                pass
        elif len(parts) >= 3 and "aes-256" in line.lower():
            try:
                # Last number is throughput in bytes/s
                result["openssl_aes256_cbc_bytes_per_s"] = float(parts[-1])
            except (ValueError, IndexError):
                pass

    result["raw_sysbench_st"] = sb_out
    result["raw_sysbench_mt"] = sb_multi
    result["raw_openssl"] = ssl_out

    return result


# ── Disk Benchmarks ───────────────────────────────────────────


def bench_disk(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Run disk I/O benchmarks: sequential + random 4K using fio."""
    log.info("Running disk benchmarks (fio)...")

    # Sequential read
    seq_read = ssh_cmd(host, r"""
        fio --name=seq-read \
            --rw=read --bs=1M --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 --fsync=10000 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """, user=user, port=port, timeout=120)

    # Sequential write
    seq_write = ssh_cmd(host, r"""
        fio --name=seq-write \
            --rw=write --bs=1M --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 --fsync=10000 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """, user=user, port=port, timeout=120)

    # Random 4K read
    rand_read = ssh_cmd(host, r"""
        fio --name=rand-read \
            --rw=randread --bs=4K --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """, user=user, port=port, timeout=120)

    # Random 4K write
    rand_write = ssh_cmd(host, r"""
        fio --name=rand-write \
            --rw=randwrite --bs=4K --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """, user=user, port=port, timeout=120)

    result: dict[str, Any] = {}

    def _parse_fio(raw: str, label: str) -> None:
        try:
            data = json.loads(raw)
            job = data.get("jobs", [{}])[0]
            opts = job.get("job options", {})
            read = job.get("read", {})

            bw = read.get("bw", 0)
            iops = read.get("iops", 0.0)
            lat_ns = read.get("lat_ns", {})
            lat_mean_ns = lat_ns.get("mean", 0.0)

            result[label] = {
                "bw_bytes_per_s": bw,
                "bw_mb_per_s": round(bw / 1024 / 1024, 2) if bw else 0,
                "iops": round(iops, 2),
                "lat_mean_us": round(lat_mean_ns / 1000, 2) if lat_mean_ns else 0,
                "ioengine": opts.get("ioengine", "?"),
                "iodepth": opts.get("iodepth", "?"),
                "bs": opts.get("bs", "?"),
            }
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            result[label] = {"error": str(e), "raw": raw[:500]}

    _parse_fio(seq_read, "sequential_read")
    _parse_fio(seq_write, "sequential_write")
    _parse_fio(rand_read, "random_4k_read")
    _parse_fio(rand_write, "random_4k_write")

    return result


# ── Memory Benchmark ──────────────────────────────────────────


def bench_memory(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Run memory benchmark: sysbench memory test."""
    log.info("Running memory benchmark...")

    out = ssh_cmd(host, """
        sysbench memory --memory-block-size=1K --memory-total-size=10G \
            --memory-oper=read --threads=1 run 2>&1
    """, user=user, port=port, timeout=120)

    result: dict[str, Any] = {}
    for line in out.splitlines():
        if "transfer rate:" in line.lower() or "transferred" in line.lower():
            # e.g. "  10240.00 MiB transferred (13312.47 MiB/sec)"
            parts = line.split("(")
            if len(parts) == 2:
                rate_str = parts[1].split("MiB/sec")[0].strip()
                try:
                    result["read_mib_per_s"] = float(rate_str)
                except ValueError:
                    pass
        elif "total time:" in line.lower():
            result["time_s"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))
        elif "operations per second" in line.lower() or "events per second" in line.lower():
            parts = line.split(":")
            if len(parts) == 2:
                try:
                    result["ops_per_s"] = float(parts[1].strip())
                except ValueError:
                    pass

    result["raw"] = out
    return result


# ── Network Benchmark ─────────────────────────────────────────


def bench_network(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Run network benchmark: download speed from public test servers."""
    log.info("Running network benchmark...")

    # Download speed test from public CDN test files
    out = ssh_cmd(host, """
        echo "=== download_speedtest ==="
        # Test download from Cloudflare (100MB)
        curl -o /dev/null -s -w "cf_100mb_download_speed_bytes_per_s:%{speed_download}\\ncf_100mb_total_time_s:%{time_total}\\n" \
            --connect-timeout 10 --max-time 30 \
            "https://speed.cloudflare.com/__down?bytes=100000000" 2>&1
        echo "=== ip_info ==="
        curl -s --max-time 5 https://ipinfo.io 2>/dev/null || echo "{}"
        echo ""
        echo "=== hostname ==="
        hostname
    """, user=user, port=port, timeout=60)

    result: dict[str, Any] = {"raw": out}

    for line in out.splitlines():
        if line.startswith("cf_100mb_download_speed_bytes_per_s:"):
            try:
                bps = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))
                result["download_mbps"] = round(bps * 8 / 1_000_000, 2)
                result["download_bytes_per_s"] = round(bps, 0)
            except (ValueError, IndexError):
                pass
        elif line.startswith("cf_100mb_total_time_s:"):
            try:
                result["download_time_s"] = float(line.split(":")[1].strip().rstrip("s").rstrip("m"))
            except (ValueError, IndexError):
                pass

    # Try to parse ipinfo JSON
    try:
        ipinfo_start = out.index("=== ip_info ===") + len("=== ip_info ===")
        ipinfo_end = out.index("=== hostname ===")
        ipinfo_raw = out[ipinfo_start:ipinfo_end].strip()
        ipinfo = json.loads(ipinfo_raw)
        result["ipinfo"] = {
            "ip": ipinfo.get("ip"),
            "city": ipinfo.get("city"),
            "region": ipinfo.get("region"),
            "country": ipinfo.get("country"),
            "org": ipinfo.get("org"),
        }
    except (ValueError, json.JSONDecodeError):
        pass

    return result


# ── Full Suite ────────────────────────────────────────────────


def run_full_suite(
    host: str,
    user: str = "debian",
    port: int = 22,
    skip_disk: bool = False,
    skip_network: bool = False,
) -> dict[str, Any]:
    """Run the full benchmark suite and return structured results.

    Results are also saved to benchmark_results/<timestamp>.json.
    """
    log.info(f"Starting full benchmark suite against {host}...")
    start = time.time()

    _install_deps(host, user, port)

    results: dict[str, Any] = {
        "host": host,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "benchmarks": {},
    }

    # System info (always run)
    results["sysinfo"] = collect_sysinfo(host, user, port)

    # CPU
    results["benchmarks"]["cpu"] = bench_cpu(host, user, port)

    # Memory
    results["benchmarks"]["memory"] = bench_memory(host, user, port)

    # Disk (can be slow)
    if not skip_disk:
        results["benchmarks"]["disk"] = bench_disk(host, user, port)
    else:
        results["benchmarks"]["disk"] = {"skipped": True}

    # Network
    if not skip_network:
        results["benchmarks"]["network"] = bench_network(host, user, port)
    else:
        results["benchmarks"]["network"] = {"skipped": True}

    elapsed = time.time() - start
    results["elapsed_seconds"] = round(elapsed, 1)
    results["completed_at"] = datetime.now(timezone.utc).isoformat()

    # Save results
    _ensure_results_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = os.path.join(RESULTS_DIR, f"bench_{host}_{ts}.json")
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    results["_saved_to"] = result_file

    log.info(f"Benchmark complete in {elapsed:.0f}s. Results: {result_file}")
    return results


# ── Pretty Print ──────────────────────────────────────────────


def print_results(results: dict[str, Any]) -> None:
    """Print benchmark results in a readable table format."""
    sysinfo = results.get("sysinfo", {})
    bench = results.get("benchmarks", {})

    print("\n" + "=" * 60)
    print(f"  VPS Benchmark: {results.get('host', '?')}")
    print("=" * 60)

    # System info
    print(f"\n  CPU:     {sysinfo.get('cpu_model', '?')}")
    print(f"  Cores:   {sysinfo.get('cpu_count', '?')}")
    print(f"  Freq:    {sysinfo.get('cpu_mhz', '?')} MHz")
    print(f"  Nested:  {'Yes' if sysinfo.get('nested_virt') else 'No'}")

    # CPU results
    cpu = bench.get("cpu", {})
    if cpu:
        print(f"\n{'─' * 60}")
        print("  CPU BENCHMARKS")
        print(f"{'─' * 60}")
        if "sysbench_st_eps" in cpu:
            print(f"  sysbench single-thread:  {cpu['sysbench_st_eps']:.0f} events/s "
                  f"({cpu.get('sysbench_st_time_s', '?')}s)")
        if "sysbench_mt_eps" in cpu:
            print(f"  sysbench multi-thread:   {cpu['sysbench_mt_eps']:.0f} events/s "
                  f"({cpu.get('sysbench_mt_time_s', '?')}s)")
        if "openssl_rsa2048_sign_per_s" in cpu:
            print(f"  OpenSSL RSA2048 sign:    {cpu['openssl_rsa2048_sign_per_s']:.0f} ops/s")
        if "openssl_rsa2048_verify_per_s" in cpu:
            print(f"  OpenSSL RSA2048 verify:  {cpu['openssl_rsa2048_verify_per_s']:.0f} ops/s")

    # Memory
    mem = bench.get("memory", {})
    if mem and not mem.get("skipped"):
        print(f"\n{'─' * 60}")
        print("  MEMORY BENCHMARKS")
        print(f"{'─' * 60}")
        if "read_mib_per_s" in mem:
            print(f"  sysbench memory read:    {mem['read_mib_per_s']:.1f} MiB/s")
        if "ops_per_s" in mem:
            print(f"  sysbench memory ops:     {mem['ops_per_s']:.0f} ops/s")

    # Disk
    disk = bench.get("disk", {})
    if disk and not disk.get("skipped"):
        print(f"\n{'─' * 60}")
        print("  DISK BENCHMARKS (fio)")
        print(f"{'─' * 60}")
        for label, key in [
            ("Sequential Read", "sequential_read"),
            ("Sequential Write", "sequential_write"),
            ("Random 4K Read", "random_4k_read"),
            ("Random 4K Write", "random_4k_write"),
        ]:
            d = disk.get(key, {})
            if isinstance(d, dict) and "bw_mb_per_s" in d:
                print(f"  {label:22s}  {d['bw_mb_per_s']:>8.1f} MB/s  "
                      f"{d['iops']:>10.0f} IOPS  "
                      f"lat={d['lat_mean_us']:.1f}µs")

    # Network
    net = bench.get("network", {})
    if net and not net.get("skipped"):
        print(f"\n{'─' * 60}")
        print("  NETWORK BENCHMARKS")
        print(f"{'─' * 60}")
        if "download_mbps" in net:
            print(f"  Download (Cloudflare):   {net['download_mbps']:.1f} Mbps")
        ipinfo = net.get("ipinfo", {})
        if ipinfo:
            loc = f"{ipinfo.get('city', '?')}, {ipinfo.get('country', '?')}"
            print(f"  Location:                {loc}")
            print(f"  ISP:                     {ipinfo.get('org', '?')}")

    elapsed = results.get("elapsed_seconds", 0)
    print(f"\n  Completed in {elapsed:.0f}s")
    print("=" * 60)

    saved = results.get("_saved_to")
    if saved:
        print(f"  Results saved: {saved}")
