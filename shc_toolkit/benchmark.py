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
import urllib.error
import urllib.request

try:
    import certifi
    import ssl

    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = None
from datetime import datetime, timezone
from typing import Any

from .provision import ssh_cmd

log = logging.getLogger(__name__)

# Directory for saving benchmark results (gitignored)
RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "benchmark_results"
)


def _ensure_results_dir() -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    return RESULTS_DIR


def _install_deps(host: str, user: str = "debian", port: int = 22) -> None:
    """Install benchmark dependencies (sysbench, fio) if missing."""
    log.info("Installing benchmark dependencies...")
    ssh_cmd(
        host,
        """
        export DEBIAN_FRONTEND=noninteractive
        need_install=""
        command -v sysbench >/dev/null 2>&1 || need_install="sysbench $need_install"
        command -v fio >/dev/null 2>&1 || need_install="fio $need_install"
        if [ -n "$need_install" ]; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq $need_install
        fi
        echo "deps ready: sysbench=$(command -v sysbench), fio=$(command -v fio)"
    """,
        user=user,
        port=port,
        timeout=180,
    )


# ── Pricing ───────────────────────────────────────────────────


SHC_CATALOG_URL = (
    "https://blesta.sovereignhybridcompute.com/user-api/v2/ordering/catalog"
)
HETZNER_PRICING_URL = "https://api.hetzner.cloud/v1/pricing"
SHC_DAILY_PRICE = "0.49"  # fallback when API is unreachable


def _http_get_json(
    url: str, headers: dict[str, str] | None = None, timeout: int = 15
) -> Any:
    """GET a URL and return parsed JSON. Raises on HTTP/parse error."""
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _collect_pricing_shc() -> dict[str, Any]:
    """Pull live pricing from SHC catalog API."""
    api_key = os.environ.get("SHC_API_KEY")
    fetched_at = datetime.now(timezone.utc).isoformat()
    if not api_key:
        return {
            "provider": "shc",
            "daily_price": SHC_DAILY_PRICE,
            "hourly_price": f"{float(SHC_DAILY_PRICE) / 24:.4f}",
            "currency": "USD",
            "billing_model": "pro-rata",
            "minimum_charge_hours": 1,
            "source_api": SHC_CATALOG_URL,
            "fetched_at": fetched_at,
            "note": "SHC_API_KEY not set; using fallback price",
        }
    try:
        data = _http_get_json(
            SHC_CATALOG_URL, headers={"Authorization": f"Bearer {api_key}"}
        )
        daily = _extract_shc_daily_price(data)
        return {
            "provider": "shc",
            "daily_price": daily,
            "hourly_price": f"{float(daily) / 24:.4f}",
            "currency": "USD",
            "billing_model": "pro-rata",
            "minimum_charge_hours": 1,
            "source_api": SHC_CATALOG_URL,
            "fetched_at": fetched_at,
        }
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        json.JSONDecodeError,
        ValueError,
    ) as e:
        log.warning(f"SHC pricing API unreachable: {e}")
        return {
            "provider": "shc",
            "daily_price": SHC_DAILY_PRICE,
            "hourly_price": f"{float(SHC_DAILY_PRICE) / 24:.4f}",
            "currency": "USD",
            "billing_model": "pro-rata",
            "minimum_charge_hours": 1,
            "source_api": SHC_CATALOG_URL,
            "fetched_at": fetched_at,
            "note": f"API unreachable ({e}); using fallback price",
        }


def _extract_shc_daily_price(catalog: Any) -> str:
    """Best-effort extraction of daily price from SHC catalog JSON."""
    if not isinstance(catalog, dict):
        return SHC_DAILY_PRICE
    # Walk the catalog looking for a pricing entry with term "day"

    def _walk(obj):
        if isinstance(obj, dict):
            term = str(obj.get("term", "")).lower()
            price = obj.get("price")
            if term in ("day", "daily", "1") and price is not None:
                return str(price)
            for v in obj.values():
                found = _walk(v)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = _walk(item)
                if found:
                    return found
        return None

    return _walk(catalog) or SHC_DAILY_PRICE


def _collect_pricing_hetzner() -> dict[str, Any]:
    """Pull live pricing from Hetzner public pricing endpoint."""
    fetched_at = datetime.now(timezone.utc).isoformat()
    try:
        data = _http_get_json(HETZNER_PRICING_URL)
        pricing = data.get("pricing", {}) if isinstance(data, dict) else {}
        return {
            "provider": "hetzner",
            "currency": pricing.get("currency", "EUR"),
            "vat_rate": pricing.get("vat_rate"),
            "image_prices": pricing.get("image", {}),
            "floating_ip_prices": pricing.get("floating_ip", {}),
            "traffic_prices": pricing.get("traffic", {}),
            "source_api": HETZNER_PRICING_URL,
            "fetched_at": fetched_at,
        }
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        log.warning(f"Hetzner pricing API unreachable: {e}")
        return {
            "provider": "hetzner",
            "pricing_available": False,
            "source_api": HETZNER_PRICING_URL,
            "fetched_at": fetched_at,
            "note": f"API unreachable ({e})",
        }


def collect_pricing(host: str, provider: str = "shc") -> dict[str, Any]:
    """Fetch live pricing for the given provider. Falls back gracefully."""
    log.info(f"Collecting pricing for provider={provider} (host={host})...")
    if provider == "auto":
        if os.environ.get("SHC_API_KEY"):
            provider = "shc"
        else:
            provider = "unknown"
    if provider == "shc":
        return _collect_pricing_shc()
    if provider == "hetzner":
        return _collect_pricing_hetzner()
    return {"provider": "unknown", "pricing_available": False}


# ── System Info ───────────────────────────────────────────────


def collect_sysinfo(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Collect basic system information."""
    log.info("Collecting system info...")
    raw = ssh_cmd(
        host,
        """
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
    """,
        user=user,
        port=port,
    )

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
    sb_out = ssh_cmd(
        host,
        """
        sysbench cpu --cpu-max-prime=20000 --threads=1 run 2>&1
    """,
        user=user,
        port=port,
        timeout=120,
    )

    sb_multi = ssh_cmd(
        host,
        """
        sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) run 2>&1
    """,
        user=user,
        port=port,
        timeout=120,
    )

    # openssl speed — RSA and AES
    ssl_out = ssh_cmd(
        host,
        """
        openssl speed -seconds 3 rsa2048 aes-256-cbc 2>&1
    """,
        user=user,
        port=port,
        timeout=60,
    )

    result: dict[str, Any] = {}

    # Parse sysbench single-thread
    for line in sb_out.splitlines():
        if "total time:" in line.lower():
            result["sysbench_st_time_s"] = float(
                line.split(":")[1].strip().rstrip("s").rstrip("m")
            )
        elif "events per second:" in line.lower():
            result["sysbench_st_eps"] = float(
                line.split(":")[1].strip().rstrip("s").rstrip("m")
            )

    # Parse sysbench multi-thread
    for line in sb_multi.splitlines():
        if "total time:" in line.lower():
            result["sysbench_mt_time_s"] = float(
                line.split(":")[1].strip().rstrip("s").rstrip("m")
            )
        elif "events per second:" in line.lower():
            result["sysbench_mt_eps"] = float(
                line.split(":")[1].strip().rstrip("s").rstrip("m")
            )

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
    seq_read = ssh_cmd(
        host,
        r"""
        fio --name=seq-read \
            --rw=read --bs=1M --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 --fsync=10000 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """,
        user=user,
        port=port,
        timeout=120,
    )

    # Sequential write
    seq_write = ssh_cmd(
        host,
        r"""
        fio --name=seq-write \
            --rw=write --bs=1M --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 --fsync=10000 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """,
        user=user,
        port=port,
        timeout=120,
    )

    # Random 4K read
    rand_read = ssh_cmd(
        host,
        r"""
        fio --name=rand-read \
            --rw=randread --bs=4K --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """,
        user=user,
        port=port,
        timeout=120,
    )

    # Random 4K write
    rand_write = ssh_cmd(
        host,
        r"""
        fio --name=rand-write \
            --rw=randwrite --bs=4K --size=1G --numjobs=1 \
            --ioengine=libaio --iodepth=32 \
            --direct=1 \
            --runtime=30 --time_based \
            --group_reporting \
            --output-format=json 2>/dev/null
    """,
        user=user,
        port=port,
        timeout=120,
    )

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


def bench_disk_yabs(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Run YABS-standard fio randrw tests across 4k/64k/512k/1m blocksizes."""
    log.info("Running YABS-compatible disk benchmarks (fio randrw)...")

    # Single SSH call runs all 4 blocksizes and emits a delimited stream of JSON blobs.
    raw = ssh_cmd(
        host,
        r"""
        for BS in 4k 64k 512k 1m; do
            echo "===FIO_START_${BS}==="
            fio --name=rand_rw \
                --ioengine=libaio \
                --rw=randrw \
                --rwmixread=50 \
                --bs=${BS} \
                --iodepth=64 \
                --numjobs=2 \
                --size=2G \
                --runtime=30 \
                --gtod_reduce=1 \
                --direct=1 \
                --group_reporting \
                --output-format=json 2>/dev/null
            echo "===FIO_END_${BS}==="
        done
    """,
        user=user,
        port=port,
        timeout=300,
    )

    results: dict[str, Any] = {}

    def _parse_one(label: str, blob: str) -> None:
        try:
            data = json.loads(blob)
            job = data.get("jobs", [{}])[0]
            r = job.get("read", {})
            w = job.get("write", {})
            # fio JSON 'bw' is in KiB/s
            r_bw_kib = r.get("bw", 0)
            w_bw_kib = w.get("bw", 0)
            results[label] = {
                "read_iops": round(r.get("iops", 0.0), 2),
                "write_iops": round(w.get("iops", 0.0), 2),
                "read_mb_s": round(r_bw_kib / 1024, 2),
                "write_mb_s": round(w_bw_kib / 1024, 2),
            }
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
            results[label] = {"error": str(e), "raw": blob[:500]}

    for bs in ("4k", "64k", "512k", "1m"):
        start_marker = f"===FIO_START_{bs}==="
        end_marker = f"===FIO_END_{bs}==="
        si = raw.find(start_marker)
        ei = raw.find(end_marker)
        if si == -1 or ei == -1 or ei <= si:
            results[bs] = {"error": f"markers not found for {bs}"}
            continue
        blob = raw[si + len(start_marker) : ei].strip()
        _parse_one(bs, blob)

    return results


# ── Memory Benchmark ──────────────────────────────────────────


def bench_memory(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Run memory benchmark: sysbench memory test."""
    log.info("Running memory benchmark...")

    out = ssh_cmd(
        host,
        """
        sysbench memory --memory-block-size=1K --memory-total-size=10G \
            --memory-oper=read --threads=1 run 2>&1
    """,
        user=user,
        port=port,
        timeout=120,
    )

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
        elif (
            "operations per second" in line.lower()
            or "events per second" in line.lower()
        ):
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
    out = ssh_cmd(
        host,
        """
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
    """,
        user=user,
        port=port,
        timeout=60,
    )

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
                result["download_time_s"] = float(
                    line.split(":")[1].strip().rstrip("s").rstrip("m")
                )
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


def bench_network_iperf3(
    host: str, user: str = "debian", port: int = 22
) -> dict[str, Any]:
    """Run iperf3 against 3 public servers (Paris, Fremont, Amsterdam)."""
    log.info("Running iperf3 network benchmarks...")

    servers = {
        "bouygues.testdebit.info": "Paris",
        "iperf.he.net": "Fremont, CA",
        "speedtest.wtnet.de": "Amsterdam",
    }

    ssh_cmd(
        host,
        """
        command -v iperf3 >/dev/null 2>&1 || {
            export DEBIAN_FRONTEND=noninteractive
            sudo apt-get update -qq && sudo apt-get install -y -qq iperf3
        }
        echo "iperf3 ready: $(command -v iperf3 || echo MISSING)"
    """,
        user=user,
        port=port,
        timeout=120,
    )

    results: dict[str, Any] = {}

    for server, location in servers.items():
        # || true keeps ssh_cmd from raising when a server is unreachable
        raw = ssh_cmd(
            host,
            f"""
            iperf3 -c {server} -P 8 -t 10 -J 2>/dev/null || echo "IPERF3_FAILED_{server}"
        """,
            user=user,
            port=port,
            timeout=30,
        )

        if f"IPERF3_FAILED_{server}" in raw:
            results[server] = {"location": location, "available": False}
            log.info(f"iperf3 server {server} unreachable, skipping")
            continue

        try:
            data = json.loads(raw)
            end = data.get("end", {})
            sum_recv = end.get("sum_received", end.get("sum", {}))
            bps = sum_recv.get("bits_per_second", 0)
            retransmits = end.get("sum_sent", end.get("sum", {})).get("retransmits", 0)
            results[server] = {
                "location": location,
                "available": True,
                "download_bps": round(bps, 0),
                "download_mbps": round(bps / 1_000_000, 2),
                "retransmits": retransmits,
            }
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            results[server] = {
                "location": location,
                "available": False,
                "error": str(e),
            }

    return results


# ── Geekbench 6 (optional) ────────────────────────────────────


GEEKBENCH_URL = "https://cdn.geekbench.com/Geekbench-6.3.0-Linux.tar.gz"


def bench_geekbench(host: str, user: str = "debian", port: int = 22) -> dict[str, Any]:
    """Download, run Geekbench 6, parse single/multi-core scores. Optional."""
    log.info("Running Geekbench 6 (optional)...")

    raw = ssh_cmd(
        host,
        f"""
        set -e
        cd /tmp
        curl -fsSL -o geekbench6.tar.gz {GEEKBENCH_URL} || {{
            echo "GB_DOWNLOAD_FAILED"
            exit 0
        }}
        tar xzf geekbench6.tar.gz
        GB_DIR=$(ls -d Geekbench-6*-Linux 2>/dev/null | head -1)
        if [ -z "$GB_DIR" ]; then
            echo "GB_EXTRACT_FAILED"
            exit 0
        fi
        cd "$GB_DIR"
        ./geekbench6 --json > /tmp/gb_result.json 2>/dev/null || {{
            echo "GB_RUN_FAILED"
            exit 0
        }}
        echo "===GB_START==="
        cat /tmp/gb_result.json
        echo "===GB_END==="
    """,
        user=user,
        port=port,
        timeout=600,
    )

    if "GB_DOWNLOAD_FAILED" in raw:
        return {"available": False, "reason": "download failed"}
    if "GB_EXTRACT_FAILED" in raw:
        return {"available": False, "reason": "extract failed"}
    if "GB_RUN_FAILED" in raw:
        return {"available": False, "reason": "run failed (license required?)"}

    si = raw.find("===GB_START===")
    ei = raw.find("===GB_END===")
    if si == -1 or ei == -1:
        return {"available": False, "reason": "no output markers", "raw": raw[:500]}

    try:
        data = json.loads(raw[si + len("===GB_START===") : ei].strip())
        scores = data.get("scores", {})
        return {
            "available": True,
            "single_core": scores.get("singleCore", scores.get("single_core", {})).get(
                "score"
            ),
            "multi_core": scores.get("multiCore", scores.get("multi_core", {})).get(
                "score"
            ),
            "version": data.get("version", "?"),
        }
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return {"available": False, "reason": f"parse error: {e}", "raw": raw[:500]}


# ── Full Suite ────────────────────────────────────────────────


def run_full_suite(
    host: str,
    user: str = "debian",
    port: int = 22,
    skip_disk: bool = False,
    skip_network: bool = False,
    run_yabs: bool = True,
    run_iperf3: bool = True,
    run_geekbench: bool = False,
    collect_pricing: bool = True,
    provider: str = "auto",
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

    if collect_pricing:
        prov = provider
        if prov == "auto":
            prov = "shc" if os.environ.get("SHC_API_KEY") else "unknown"
        if prov == "shc":
            results["pricing"] = _collect_pricing_shc()
        elif prov == "hetzner":
            results["pricing"] = _collect_pricing_hetzner()
        else:
            results["pricing"] = {"provider": "unknown", "pricing_available": False}
    else:
        results["pricing"] = {"pricing_available": False, "skipped": True}

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

    # YABS-compatible fio tests
    if run_yabs and not skip_disk:
        results["benchmarks"]["disk_yabs"] = bench_disk_yabs(host, user, port)
    else:
        results["benchmarks"]["disk_yabs"] = {"skipped": True}

    # Network
    if not skip_network:
        results["benchmarks"]["network"] = bench_network(host, user, port)
    else:
        results["benchmarks"]["network"] = {"skipped": True}

    # iperf3 network tests
    if run_iperf3 and not skip_network:
        results["benchmarks"]["network_iperf3"] = bench_network_iperf3(host, user, port)
    else:
        results["benchmarks"]["network_iperf3"] = {"skipped": True}

    # Geekbench 6 (optional)
    if run_geekbench:
        results["benchmarks"]["geekbench"] = bench_geekbench(host, user, port)
    else:
        results["benchmarks"]["geekbench"] = {"skipped": True}

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
    pricing = results.get("pricing", {})

    print("\n" + "=" * 60)
    print(f"  VPS Benchmark: {results.get('host', '?')}")
    print("=" * 60)

    if pricing and not pricing.get("skipped"):
        pprov = pricing.get("provider", "?")
        if pricing.get("pricing_available", True) and "daily_price" in pricing:
            daily = pricing["daily_price"]
            hourly = pricing.get("hourly_price", "?")
            model = pricing.get("billing_model", "?")
            min_hrs = pricing.get("minimum_charge_hours", "?")
            src = "SHC catalog API" if pprov == "shc" else f"{pprov} API"
            print(
                f"\n  Price: ${hourly}/hr (${daily}/day, {model} {min_hrs}hr min)"
                f"  — source: {src}"
            )
        elif pprov != "unknown":
            print(f"\n  Price: ({pprov} pricing unavailable)")

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
            print(
                f"  sysbench single-thread:  {cpu['sysbench_st_eps']:.0f} events/s "
                f"({cpu.get('sysbench_st_time_s', '?')}s)"
            )
        if "sysbench_mt_eps" in cpu:
            print(
                f"  sysbench multi-thread:   {cpu['sysbench_mt_eps']:.0f} events/s "
                f"({cpu.get('sysbench_mt_time_s', '?')}s)"
            )
        if "openssl_rsa2048_sign_per_s" in cpu:
            print(
                f"  OpenSSL RSA2048 sign:    {cpu['openssl_rsa2048_sign_per_s']:.0f} ops/s"
            )
        if "openssl_rsa2048_verify_per_s" in cpu:
            print(
                f"  OpenSSL RSA2048 verify:  {cpu['openssl_rsa2048_verify_per_s']:.0f} ops/s"
            )

    # Geekbench (optional, show early near CPU)
    gb = bench.get("geekbench", {})
    if gb and gb.get("available"):
        print(f"\n{'─' * 60}")
        print(f"  GEEKBENCH 6 (v{gb.get('version', '?')})")
        print(f"{'─' * 60}")
        sc = gb.get("single_core")
        mc = gb.get("multi_core")
        if sc is not None:
            print(f"  Single-core:  {sc}")
        if mc is not None:
            print(f"  Multi-core:   {mc}")

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
                print(
                    f"  {label:22s}  {d['bw_mb_per_s']:>8.1f} MB/s  "
                    f"{d['iops']:>10.0f} IOPS  "
                    f"lat={d['lat_mean_us']:.1f}µs"
                )

    # YABS-compatible disk tests
    yabs = bench.get("disk_yabs", {})
    if yabs and not yabs.get("skipped"):
        print(f"\n{'─' * 60}")
        print("  DISK BENCHMARKS — YABS (fio randrw)")
        print(f"{'─' * 60}")
        print(
            f"  {'BS':>5s}  {'R IOPS':>10s} {'W IOPS':>10s}  "
            f"{'R MB/s':>8s} {'W MB/s':>8s}"
        )
        for bs in ("4k", "64k", "512k", "1m"):
            d = yabs.get(bs, {})
            if isinstance(d, dict) and "read_iops" in d:
                print(
                    f"  {bs:>5s}  {d['read_iops']:>10.0f} {d['write_iops']:>10.0f}  "
                    f"{d['read_mb_s']:>8.1f} {d['write_mb_s']:>8.1f}"
                )

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

    # iperf3 network tests
    iperf = bench.get("network_iperf3", {})
    if iperf and not iperf.get("skipped"):
        print(f"\n{'─' * 60}")
        print("  NETWORK BENCHMARKS — iperf3 (8 parallel, 10s)")
        print(f"{'─' * 60}")
        for _server, info in iperf.items():
            if not isinstance(info, dict):
                continue
            loc = info.get("location", "?")
            if info.get("available"):
                mbps = info.get("download_mbps", 0)
                retr = info.get("retransmits", 0)
                print(f"  {loc:20s}  {mbps:>10.1f} Mbps  (retransmits: {retr})")
            else:
                print(f"  {loc:20s}  (unavailable)")

    elapsed = results.get("elapsed_seconds", 0)
    print(f"\n  Completed in {elapsed:.0f}s")
    print("=" * 60)

    saved = results.get("_saved_to")
    if saved:
        print(f"  Results saved: {saved}")
