#!/usr/bin/env python3
"""
Publish benchmark results to Blossom + Nostr.

Uploads a benchmark JSON file to a Blossom server (BUD-02 PUT with BUD-11 auth),
then publishes a kind 30078 Nostr event with the benchmark data in the content
and a ``file`` tag pointing to the Blossom blob URL.

Uses the nak CLI (https://github.com/fiatjaf/nak) for all Nostr event signing.
The nsec is read from a file and passed via the NOSTR_SECRET_KEY env var so it
never appears in the process list. Stdlib only — no pip dependencies.

Usage:
    python3 scripts/publish_benchmarks.py benchmark_results/bench_10x0x0x_20260622.json \\
        --nsec-file ~/.config/shc/nsec \\
        --blossom-server https://blossom.psbt.me \\
        --relays wss://relay.damus.io,wss://relay.cashu.email
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

# --- Constants ---

DEFAULT_BLOSSOM_SERVER = "https://blossom.psbt.me"
DEFAULT_RELAYS = "wss://relay.damus.io,wss://relay.cashu.email"
FREE_TIER_SIZE_LIMIT = 1_000_000  # 1 MB — files under this are free on blossom.psbt.me

# Kind 30078 = NIP-78 application-specific data (parameterized replaceable).
KIND_APP_DATA = 30078

# SHC catalog API for live pricing enrichment.
SHC_CATALOG_URL = "https://blesta.sovereignhybridcompute.com/user-api/v2/ordering/catalog"
SHC_DAILY_PRICE_FALLBACK = "0.49"

import certifi
import ssl
_SSL_CTX = ssl.create_default_context(cafile=certifi.where())


# --- Utility functions ---


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 hex digest of a file (streaming, constant memory)."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _guess_content_type(file_path: str, fallback: str = "application/json") -> str:
    """Guess MIME type from extension. Defaults to application/json."""
    if file_path.endswith(".json"):
        return "application/json"
    return fallback


# --- Blossom upload (BUD-02 + BUD-11) ---


def _sign_blossom_auth_event(
    nsec_file: str,
    sha256_hash: str,
    action: str = "upload",
    expiration_seconds: int = 3600,
) -> dict[str, Any]:
    """Sign a kind 24242 Blossom auth event (BUD-11) using nak CLI.

    Creates and signs the event WITHOUT publishing to relays. The key is passed
    via NOSTR_SECRET_KEY env var so it never shows in the process list.
    """
    expiration = str(int(time.time()) + expiration_seconds)

    with open(nsec_file) as f:
        nsec_hex = f.read().strip()

    label = "Upload" if action == "upload" else action.title()
    cmd = [
        "nak", "event",
        "-k", "24242",
        "-c", f"{label} Blob",
        "-t", f"t={action}",
        "-t", f"x={sha256_hash}",
        "-t", f"expiration={expiration}",
    ]

    env = os.environ.copy()
    env["NOSTR_SECRET_KEY"] = nsec_hex

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, env=env)

    if result.returncode != 0:
        raise RuntimeError(
            f"nak event (BUD-11 auth) failed: {result.stderr.strip()[:300]}"
        )

    for line in reversed(result.stdout.strip().split("\n")):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)

    raise RuntimeError(f"Could not parse nak output: {result.stdout[:200]}")


def _make_auth_header(signed_event: dict[str, Any]) -> str:
    """Create the Authorization header value: ``Nostr <base64url(event)>``."""
    event_json = json.dumps(signed_event, separators=(",", ":"))
    encoded = base64.urlsafe_b64encode(event_json.encode()).decode().rstrip("=")
    return f"Nostr {encoded}"


def upload_to_blossom(
    file_path: str,
    nsec_file: str,
    blossom_server: str = DEFAULT_BLOSSOM_SERVER,
) -> dict[str, Any]:
    """Upload a file to a Blossom server via BUD-02 PUT with BUD-11 auth.

    Returns a dict with keys: url, sha256, size.
    Raises RuntimeError on HTTP errors or Cashu payment requirements (402).
    """
    file_size = os.path.getsize(file_path)
    sha256 = compute_sha256(file_path)
    content_type = _guess_content_type(file_path)

    print(
        f"  Uploading: {file_path} ({file_size:,} bytes, {content_type}, "
        f"sha256: {sha256[:16]}...)"
    )

    if file_size < FREE_TIER_SIZE_LIMIT:
        print("  OK: Under 1MB — free tier (no Cashu payment needed)")

    with open(file_path, "rb") as f:
        file_data = f.read()

    auth_event = _sign_blossom_auth_event(nsec_file, sha256)
    auth_header = _make_auth_header(auth_event)

    headers = {
        "Authorization": auth_header,
        "Content-Type": content_type,
        "Content-Length": str(len(file_data)),
        "X-SHA-256": sha256,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "*/*",
        "Origin": blossom_server.rstrip("/"),
    }

    upload_url = f"{blossom_server.rstrip('/')}/upload"
    req = urllib.request.Request(upload_url, data=file_data, headers=headers, method="PUT")

    try:
        with urllib.request.urlopen(req, timeout=60, context=_SSL_CTX) as response:
            body = json.loads(response.read())
            blob_url = body.get("url", f"{blossom_server.rstrip('/')}/{sha256}")
            print(f"  Uploaded: {blob_url}")
            return {
                "url": blob_url,
                "sha256": sha256,
                "size": file_size,
            }

    except urllib.error.HTTPError as e:
        if e.code == 402:
            cashu_header = e.headers.get("X-Cashu", "")
            detail = e.read().decode()[:300]
            raise RuntimeError(
                f"Blossom server requires Cashu payment (HTTP 402). "
                f"X-Cashu: {cashu_header}. Obtain a token and retry. Body: {detail}"
            )
        body = e.read().decode()[:500]
        raise RuntimeError(f"Blossom upload failed: HTTP {e.code}\n{body}")


# --- Pricing enrichment ---


def _fetch_shc_pricing() -> dict[str, Any]:
    """Fetch live daily pricing from the SHC catalog API.

    Falls back to a static price if the API is unreachable or SHC_API_KEY is
    not set. Always includes the source_api URL so the SPA can display it.
    """
    fetched_at = datetime.now(timezone.utc).isoformat()
    api_key = os.environ.get("SHC_API_KEY")

    if not api_key:
        return {
            "provider": "shc",
            "daily_price": SHC_DAILY_PRICE_FALLBACK,
            "hourly_price": f"{float(SHC_DAILY_PRICE_FALLBACK) / 24:.4f}",
            "currency": "USD",
            "billing_model": "pro-rata",
            "source_api": SHC_CATALOG_URL,
            "fetched_at": fetched_at,
            "note": "SHC_API_KEY not set; using fallback price",
        }

    try:
        req = urllib.request.Request(
            SHC_CATALOG_URL,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            catalog = json.loads(resp.read().decode("utf-8"))

        daily = _extract_shc_daily_price(catalog)
        return {
            "provider": "shc",
            "daily_price": daily,
            "hourly_price": f"{float(daily) / 24:.4f}",
            "currency": "USD",
            "billing_model": "pro-rata",
            "source_api": SHC_CATALOG_URL,
            "fetched_at": fetched_at,
        }
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, ValueError) as e:
        print(f"  WARNING: SHC pricing API unreachable: {e}")
        return {
            "provider": "shc",
            "daily_price": SHC_DAILY_PRICE_FALLBACK,
            "hourly_price": f"{float(SHC_DAILY_PRICE_FALLBACK) / 24:.4f}",
            "currency": "USD",
            "billing_model": "pro-rata",
            "source_api": SHC_CATALOG_URL,
            "fetched_at": fetched_at,
            "note": f"API unreachable ({e}); using fallback price",
        }


def _extract_shc_daily_price(catalog: Any) -> str:
    """Walk the SHC catalog JSON looking for a daily price entry."""

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

    return _walk(catalog) or SHC_DAILY_PRICE_FALLBACK


# --- Benchmark event publishing (kind 30078) ---


def _derive_run_id(results: dict[str, Any], file_path: str) -> str:
    """Derive a unique benchmark run ID from host + timestamp.

    Format: bench-<host>-<YYYYMMDDHHMMSS>
    Falls back to the filename stem if host/timestamp are missing.
    """
    host = results.get("host", "")
    ts_raw = results.get("completed_at") or results.get("started_at") or ""

    # Try to parse the ISO timestamp into a compact YYYYMMDDHHMMSS.
    ts_compact = ""
    if ts_raw:
        try:
            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            ts_compact = dt.strftime("%Y%m%d%H%M%S")
        except (ValueError, TypeError):
            pass

    if host and ts_compact:
        # Sanitize host for use in a d-tag (no dots/special chars).
        host_clean = re.sub(r"[^a-zA-Z0-9_-]", "-", host)
        return f"bench-{host_clean}-{ts_compact}"

    # Fallback: use the filename without extension.
    return f"bench-{os.path.splitext(os.path.basename(file_path))[0]}"


def _nak_available() -> bool:
    """Check if nak CLI is installed and on PATH."""
    result = subprocess.run(["which", "nak"], capture_output=True, text=True)
    return result.returncode == 0


def _parse_nak_publish_output(stderr: str) -> dict[str, Any]:
    """Parse nak stderr for per-relay acceptance/rejection status.

    nak exits 0 even when relays reject events (whitelist blocks, rate limits).
    The relay status lines appear on stderr. This extracts them so callers can
    detect silent rejections.
    """
    relay_results: dict[str, dict[str, Any]] = {}
    pattern = re.compile(r"^publishing to (.+?)\.\.\. (success\.|failed:)\s*(.*)$")
    for line in stderr.splitlines():
        line = line.strip()
        m = pattern.match(line)
        if not m:
            continue
        relay, status_raw, message = m.group(1), m.group(2), m.group(3).strip()
        accepted = status_raw.startswith("success")
        relay_results[relay] = {
            "accepted": accepted,
            "message": message if message else ("" if accepted else "unknown"),
        }
    any_accepted = any(r["accepted"] for r in relay_results.values())
    all_rejected_reasons = [
        f"{relay}: {r['message']}" for relay, r in relay_results.items() if not r["accepted"]
    ]
    return {
        "relay_results": relay_results,
        "any_accepted": any_accepted,
        "all_rejected_reasons": all_rejected_reasons,
    }


def publish_benchmark_event(
    results_json: dict[str, Any],
    nsec_file: str,
    relays: list[str],
    blossom_url: str | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Publish a kind 30078 Nostr event with benchmark data.

    The event content is the full benchmark JSON (stringified). Tags:
        ["d", run_id]               — parameterized replaceable identifier
        ["t", "benchmark"]          — topic tag for SPA discovery
        ["file", blossom_url]       — link to the Blossom blob (if uploaded)
        ["hostname", host]          — display tag (if host present)

    Args:
        results_json: The benchmark results dict (from run_full_suite or similar).
        nsec_file: Path to a file containing a hex Nostr private key.
        relays: List of Nostr relay URLs to publish to.
        blossom_url: Optional Blossom blob URL to include as a file tag.
        run_id: Optional run ID for the d-tag. Auto-derived if None.

    Returns:
        Dict with: success, event_id, event, relay_status. On failure:
        success=False, error=... (plus event_id/event if signed but rejected).
    """
    if not relays:
        return {"success": False, "error": "No relays configured."}

    if not _nak_available():
        return {
            "success": False,
            "error": "nak CLI not found. Install: https://github.com/fiatjaf/nak",
        }

    if run_id is None:
        run_id = _derive_run_id(results_json, "<unknown>")

    content = json.dumps(results_json, separators=(",", ":"), default=str)

    tags: list[list[str]] = [
        ["d", run_id],
        ["t", "benchmark"],
    ]

    if blossom_url:
        tags.append(["file", blossom_url])

    host = results_json.get("host")
    if host:
        tags.append(["hostname", str(host)])

    # Build the nak command. Each tag becomes a -t key=val1;val2 argument.
    with open(nsec_file) as f:
        nsec_hex = f.read().strip()

    cmd = [
        "nak", "event",
        "-k", str(KIND_APP_DATA),
        "-c", content,
    ]

    for tag in tags:
        tag_key = tag[0]
        tag_vals = ";".join(str(t) for t in tag[1:])
        cmd.extend(["-t", f"{tag_key}={tag_vals}"])

    cmd.extend(relays)

    env = os.environ.copy()
    env["NOSTR_SECRET_KEY"] = nsec_hex

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)

    if result.returncode != 0:
        return {
            "success": False,
            "error": f"nak event failed: {result.stderr.strip()[:300]}",
        }

    nak_status = _parse_nak_publish_output(result.stderr)

    event: dict[str, Any] = {}
    event_id = ""
    try:
        event = json.loads(result.stdout.strip().split("\n")[-1])
        event_id = event.get("id", "")
    except (json.JSONDecodeError, IndexError):
        pass

    if not nak_status["any_accepted"]:
        reasons = "; ".join(nak_status["all_rejected_reasons"]) or "all relays rejected (no detail)"
        return {
            "success": False,
            "error": f"Event signed but rejected by all relays: {reasons}",
            "event_id": event_id,
            "event": event,
            "relay_status": nak_status,
        }

    return {
        "success": True,
        "event_id": event_id,
        "event": event,
        "relay_status": nak_status,
    }


# --- CLI entry point ---


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publish benchmark results to Blossom + Nostr (kind 30078).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Example:
  python3 scripts/publish_benchmarks.py benchmark_results/bench_10x0x0x_20260622.json \\
      --nsec-file ~/.config/shc/nsec \\
      --blossom-server https://blossom.psbt.me \\
      --relays wss://relay.damus.io,wss://relay.cashu.email
""",
    )
    parser.add_argument(
        "benchmark_file",
        help="Path to the benchmark results JSON file (output of run_full_suite).",
    )
    parser.add_argument(
        "--nsec-file",
        required=True,
        help="Path to a file containing a hex Nostr private key.",
    )
    parser.add_argument(
        "--blossom-server",
        default=DEFAULT_BLOSSOM_SERVER,
        help=f"Blossom server base URL (default: {DEFAULT_BLOSSOM_SERVER}).",
    )
    parser.add_argument(
        "--relays",
        default=DEFAULT_RELAYS,
        help=f"Comma-separated Nostr relay URLs (default: {DEFAULT_RELAYS}).",
    )
    parser.add_argument(
        "--skip-blossom",
        action="store_true",
        help="Skip the Blossom upload (publish Nostr event only, no file tag).",
    )
    parser.add_argument(
        "--skip-pricing",
        action="store_true",
        help="Do not fetch live pricing. Use whatever is already in the JSON.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Override the benchmark run ID (d-tag). Auto-derived if omitted.",
    )

    args = parser.parse_args()

    # --- Load benchmark JSON ---
    if not os.path.isfile(args.benchmark_file):
        print(f"ERROR: File not found: {args.benchmark_file}", file=sys.stderr)
        return 1

    print(f"Loading benchmark data: {args.benchmark_file}")
    with open(args.benchmark_file) as f:
        results: dict[str, Any] = json.load(f)

    # --- Enrich with live pricing (unless skipped or already present) ---
    if not args.skip_pricing and "pricing" not in results:
        print("Fetching live pricing from SHC catalog API...")
        results["pricing"] = _fetch_shc_pricing()
    elif "pricing" in results:
        print("  Pricing already present in JSON — keeping existing data.")

    # We need to write the enriched JSON to a temp file for Blossom upload.
    upload_file = args.benchmark_file
    temp_file = None
    if not args.skip_blossom and "pricing" in results and results.get("pricing"):
        # Write enriched JSON to a temp file so Blossom has the full payload.
        temp_file = args.benchmark_file + ".published.json"
        with open(temp_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        upload_file = temp_file
        print(f"Wrote enriched JSON (with pricing) to: {temp_file}")

    relays = [r.strip() for r in args.relays.split(",") if r.strip()]
    if not relays:
        print("ERROR: No valid relays specified.", file=sys.stderr)
        return 1

    # --- Upload to Blossom ---
    blossom_url = None
    if not args.skip_blossom:
        print(f"\n--- Blossom Upload ({args.blossom_server}) ---")
        try:
            upload_result = upload_to_blossom(upload_file, args.nsec_file, args.blossom_server)
            blossom_url = upload_result["url"]
        except RuntimeError as e:
            print(f"\nERROR: Blossom upload failed: {e}", file=sys.stderr)
            print("  You can retry, or use --skip-blossom to publish Nostr only.")
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
            return 1

    # --- Publish Nostr event ---
    print(f"\n--- Nostr Publish ({len(relays)} relay{'s' if len(relays) != 1 else ''}) ---")
    run_id = args.run_id or _derive_run_id(results, args.benchmark_file)
    print(f"  Run ID: {run_id}")

    nostr_result = publish_benchmark_event(
        results_json=results,
        nsec_file=args.nsec_file,
        relays=relays,
        blossom_url=blossom_url,
        run_id=run_id,
    )

    if nostr_result.get("success"):
        print(f"  Published: event {nostr_result.get('event_id', '?')}")
        relay_status = nostr_result.get("relay_status", {})
        for relay_url, status in relay_status.get("relay_results", {}).items():
            state = "accepted" if status["accepted"] else f"rejected: {status['message']}"
            print(f"    {relay_url}: {state}")
    else:
        print(f"\nERROR: Nostr publish failed: {nostr_result.get('error', 'unknown')}",
              file=sys.stderr)
        if nostr_result.get("event_id"):
            print(f"  Event was signed (id: {nostr_result['event_id']}) but rejected.",
                  file=sys.stderr)
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        return 1

    # --- Cleanup temp file ---
    if temp_file and os.path.exists(temp_file):
        os.remove(temp_file)

    # --- Summary ---
    print("\n--- Done ---")
    print(f"  Benchmark: {results.get('host', '?')}")
    print(f"  Run ID:    {run_id}")
    if blossom_url:
        print(f"  Blossom:   {blossom_url}")
    print(f"  Event:     {nostr_result.get('event_id', '?')}")
    print(f"  Relays:    {', '.join(relays)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
