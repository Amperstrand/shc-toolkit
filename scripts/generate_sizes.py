#!/usr/bin/env python3
"""Fetch the live SHC catalog and regenerate sizes tables in Python, Go, or Pulumi form.

Single source of truth for SHC VM sizes. Downstream repos regenerate their
embedded copies from this script:

    # terraform-provider-shc (from its repo root, sibling checkout):
    python3 ../shc-toolkit/scripts/generate_sizes.py --format go --output provider/sizes.go
    # shc-pulumi:
    python3 ../shc-toolkit/scripts/generate_sizes.py --format pulumi --output src/shc_pulumi/sizes.py

Refresh the toolkit itself from a checkout:

    python scripts/generate_sizes.py                       # live -> shc_toolkit/sizes.py + cache
    python scripts/generate_sizes.py --from-cache          # regenerate from catalog_cache.json
    python scripts/generate_sizes.py --check               # report live vs cached drift

Requires SHC_API_KEY in env for any live fetch.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LINE_ORDER = ["nvme", "ssd", "hdd", "dev"]
TERM_ORDER = {"day": 0, "week": 1, "month": 2, "year": 3}


def _repo_root() -> Path:
    """Repo root when running from a checkout; CWD otherwise.

    Falls back to CWD so the script also works via ``python3 -`` (stdin), e.g.
    ``curl ... | python3 - --format go --output ...`` and from downstream repos
    where --output is resolved relative to the caller's CWD.
    """
    try:
        here = Path(__file__).resolve().parent
        root = here.parent
        if (root / "shc_toolkit").is_dir() and (root / "scripts").is_dir():
            return root
    except (NameError, OSError):
        pass
    return Path.cwd()


ROOT = _repo_root()
CACHE_PATH = ROOT / "shc_toolkit" / "catalog_cache.json"
SIZES_PATH = ROOT / "shc_toolkit" / "sizes.py"


def fetch_catalog() -> list[dict]:
    sys.path.insert(0, str(ROOT))
    from shc_toolkit.client import SHCClient
    return SHCClient().get_catalog()


def normalize_package(raw: dict) -> dict:
    """Flatten a raw catalog package into the cached shape."""
    pkg_id = raw["package_id"]
    name = raw["name"]
    line = _detect_line(raw)

    return {
        "package_id": pkg_id,
        "name": name,
        "line": line,
        "cpu": raw["cpu"],
        "memory_mb": raw["memory_mb"],
        "disk_gb": raw["disk_gb"],
        "bandwidth_gb": raw["bandwidth_gb"],
        "ipv4": raw["ipv4"],
        "ipv6": raw["ipv6"],
        "snapshot_limit": raw.get("snapshot_limit"),
        "backup_limit": raw.get("backup_limit"),
        "template": raw.get("template"),
        "module_groups": raw.get("module_groups", []),
        "default_module_group_id": raw.get("default_module_group_id"),
        "module_group_required": raw.get("module_group_required", False),
        "order_form_id": raw.get("order_form_id"),
        "order_form_label": raw.get("order_form_label"),
        "pricings": _extract_pricings(raw),
        "config_options": _extract_config_options(raw),
    }


def _detect_line(raw: dict) -> str:
    label = (raw.get("order_form_label") or "").lower()
    name = raw.get("name", "").lower()
    if "dev" in label or "dev" in name:
        return "dev"
    if "hdd" in label or "hdd" in name:
        return "hdd"
    if "ssd" in label or "ssd" in name:
        return "ssd"
    return "nvme"


def _extract_pricings(raw: dict) -> list[dict]:
    out = []
    for p in raw.get("pricing", []):
        out.append({
            "pricing_id": p["pricing_id"],
            "term": p.get("term"),
            "period": p.get("period"),
            "price": p.get("price"),
            "renew": p.get("renew"),
            "setup_fee": p.get("setup_fee"),
            "currency": p.get("currency", "USD"),
        })
    out.sort(key=lambda x: TERM_ORDER.get(x["period"], 99))
    return out


def _extract_config_options(raw: dict) -> dict[str, dict]:
    """Extract config options keyed by option name, deduped across billing terms."""
    seen = {}
    for block in raw.get("available_config_options", []):
        for opt in block.get("options", []):
            name = opt["name"]
            if name in seen:
                continue
            seen[name] = {
                "option_id": opt["option_id"],
                "label": opt.get("label", name),
                "addable": opt.get("addable", False),
                "editable": opt.get("editable", False),
                "values": [
                    {
                        "value": v["value"],
                        "name": v["name"],
                        "default": v.get("default", False),
                    }
                    for v in opt.get("values", [])
                ],
            }
    return seen


def build_cache(catalog: list[dict]) -> dict:
    packages = [normalize_package(p) for p in catalog]
    packages.sort(key=lambda p: (LINE_ORDER.index(p["line"]) if p["line"] in LINE_ORDER else 99, p["cpu"], p["package_id"]))
    return {
        "_meta": {
            "description": "Local cache of SHC catalog data. Auto-generated by scripts/generate_sizes.py from GET /ordering/catalog. Do not edit by hand.",
            "source": "https://blesta.sovereignhybridcompute.com/user-api/v2/ordering/catalog",
            "package_count": len(packages),
        },
        "packages": packages,
    }


# ---------------------------------------------------------------------------
# Row extraction (shared by all renderers)
# ---------------------------------------------------------------------------

def _size_rows(cache: dict) -> list[dict]:
    """Flatten cache packages into one row per size, with spec key + daily price."""
    rows = []
    for p in cache["packages"]:
        line = p["line"]
        cpu = p["cpu"]
        ram_gb = p["memory_mb"] // 1024
        spec_key = f"{line}-{cpu}c-{ram_gb}gb"
        daily = next((pr for pr in p["pricings"] if pr["period"] == "day"), None)
        rows.append({
            "spec_key": spec_key,
            "package_id": p["package_id"],
            "pricing_id": daily["pricing_id"] if daily else 0,
            "cpu": cpu,
            "ram_mb": p["memory_mb"],
            "disk_gb": p["disk_gb"],
            "line": line,
            "name": p["name"],
            "daily_price": daily["price"] if daily else "0.00",
        })
    return rows


# ---------------------------------------------------------------------------
# Python renderer (shc_toolkit/sizes.py)
# ---------------------------------------------------------------------------

_SIZES_PY_TEMPLATE = '''"""VM size catalog for SHC, auto-generated from GET /ordering/catalog.

Spec-encoding names follow the {line}-{cpu}c-{ram}gb convention:
    nvme-2c-8gb, ssd-1c-4gb, hdd-4c-16gb, dev-2c-8gb

The static SIZE_MAP is the default fast path (no network, no auth).
For live pricing, use SHCClient.get_catalog().

Regenerate:
    python scripts/generate_sizes.py
"""

from __future__ import annotations

SIZE_MAP: dict[str, dict] = {
__ENTRIES__
}


def resolve_size(size: str) -> tuple[int, int]:
    """Resolve a spec-encoding size name to (package_id, pricing_id).

    Args:
        size: Size name like `nvme-2c-8gb`, `hdd-1c-4gb`, `dev-4c-16gb`.

    Returns:
        (package_id, pricing_id) tuple.

    Raises:
        ValueError: If size name is not recognized.
    """
    entry = SIZE_MAP.get(size.lower().strip())
    if not entry:
        valid = ", ".join(SIZE_MAP.keys())
        raise ValueError(f"Unknown size \\"{size}\\". Valid sizes: {valid}")
    return entry["package_id"], _PRICING_LOOKUP[entry["package_id"]]


def resolve_specs(
    cpu: int | None = None,
    ram_mb: int | None = None,
    disk_gb: int | None = None,
    *,
    line: str | None = None,
) -> tuple[int, int]:
    """Find the cheapest plan that meets or exceeds the requested specs.

    Args:
        cpu: Minimum CPU cores required.
        ram_mb: Minimum RAM in MB required.
        disk_gb: Minimum disk in GB required.
        line: Filter by `nvme`, `ssd`, `hdd`, or `dev`. None = all.

    Returns:
        (package_id, pricing_id) of the cheapest matching plan.

    Raises:
        ValueError: If no plan matches the specs.
    """
    candidates = []
    for entry in SIZE_MAP.values():
        if line and entry["line"] != line:
            continue
        if cpu and entry["cpu"] < cpu:
            continue
        if ram_mb and entry["ram_mb"] < ram_mb:
            continue
        if disk_gb and entry["disk_gb"] < disk_gb:
            continue
        candidates.append(entry)
    if not candidates:
        raise ValueError(
            f"No plan matches specs: cpu>={cpu}, ram_mb>={ram_mb}, disk_gb>={disk_gb}, line={line}"
        )
    cheapest = min(candidates, key=lambda e: float(e["daily_price"]))
    return cheapest["package_id"], _PRICING_LOOKUP[cheapest["package_id"]]


def list_sizes(line: str | None = None) -> list[dict]:
    """List all available sizes with their specs.

    Args:
        line: Filter by `nvme`, `ssd`, `hdd`, or `dev`. None = all.

    Returns:
        List of size dicts with size, package_id, cpu, ram_mb, disk_gb, line, name, daily_price.
    """
    result = []
    for name, entry in SIZE_MAP.items():
        if line and entry["line"] != line:
            continue
        result.append({"size": name, **entry})
    return result


def spec_name(line: str, cpu: int, ram_mb: int) -> str:
    """Generate a spec-encoding size name from specs."""
    return f"{line}-{cpu}c-{ram_mb // 1024}gb"


_PRICING_LOOKUP: dict[int, int] = {
__PRICING_LOOKUP__
}
'''


def render_sizes_py(cache: dict) -> str:
    """Render the toolkit's shc_toolkit/sizes.py module."""
    rows = _size_rows(cache)
    entries_lines = []
    pricing_lines = []
    for r in rows:
        entries_lines.append(
            f'    "{r["spec_key"]}": {{"package_id": {r["package_id"]}, "cpu": {r["cpu"]}, '
            f'"ram_mb": {r["ram_mb"]}, "disk_gb": {r["disk_gb"]}, "line": "{r["line"]}", '
            f'"name": "{r["name"]}", "daily_price": "{r["daily_price"]}"}},'
        )
        pricing_lines.append(f'    {r["package_id"]}: {r["pricing_id"]},  # {r["spec_key"]}')
    body = _SIZES_PY_TEMPLATE.replace("__ENTRIES__", "\n".join(entries_lines))
    body = body.replace("__PRICING_LOOKUP__", "\n".join(pricing_lines))
    return body


# ---------------------------------------------------------------------------
# Go renderer (terraform-provider-shc/provider/sizes.go)
# ---------------------------------------------------------------------------

_SIZES_GO_TEMPLATE = '''package provider

import "fmt"

type sizeEntry struct {
	PackageID  int64
	PricingID  int64
	CPU        int64
	RamMB      int64
	DiskGB     int64
	Line       string
	Name       string
	DailyPrice float64
}

var sizeMap = map[string]sizeEntry{
__ENTRIES__
}

func resolveSize(size string) (int64, int64, error) {
	s, ok := sizeMap[size]
	if !ok {
		valid := make([]string, 0, len(sizeMap))
		for k := range sizeMap {
			valid = append(valid, k)
		}
		return 0, 0, fmt.Errorf("unknown size '%s'. Valid sizes: nvme-{1,2,4,8,16}c-{4,8,16,32,64}gb, ssd-*, hdd-*, dev-*. Examples: nvme-2c-8gb, hdd-1c-4gb, dev-4c-16gb", size)
	}
	return s.PackageID, s.PricingID, nil
}

func resolveSpecs(cpu, ramMB, diskGB int64, line string) (int64, int64, error) {
	lineRank := map[string]int{"nvme": 0, "ssd": 1, "hdd": 2, "dev": 3}
	var best *sizeEntry
	for _, s := range sizeMap {
		if line != "" && s.Line != line {
			continue
		}
		if cpu > 0 && s.CPU < cpu {
			continue
		}
		if ramMB > 0 && s.RamMB < ramMB {
			continue
		}
		if diskGB > 0 && s.DiskGB < diskGB {
			continue
		}
		if best == nil {
			best = &s
			continue
		}
		if s.DailyPrice < best.DailyPrice {
			best = &s
		} else if s.DailyPrice == best.DailyPrice && lineRank[s.Line] < lineRank[best.Line] {
			best = &s
		}
	}
	if best == nil {
		return 0, 0, fmt.Errorf("no plan matches: cpu>=%d, ram>=%dMB, disk>=%dGB, line=%s", cpu, ramMB, diskGB, line)
	}
	return best.PackageID, best.PricingID, nil
}
'''


def render_sizes_go(cache: dict) -> str:
    """Render terraform-provider-shc/provider/sizes.go."""
    rows = _size_rows(cache)
    max_key = max(len(f'"{r["spec_key"]}":') for r in rows)
    lines = []
    for r in rows:
        key = f'\t"{r["spec_key"]}":'
        pad = " " * (max_key - len(key.strip()) + 1)
        lines.append(
            f'{key}{pad}{{{r["package_id"]}, {r["pricing_id"]}, {r["cpu"]}, '
            f'{r["ram_mb"]}, {r["disk_gb"]}, "{r["line"]}", "{r["name"]}", {r["daily_price"]}}},'
        )
    return _SIZES_GO_TEMPLATE.replace("__ENTRIES__", "\n".join(lines))


# ---------------------------------------------------------------------------
# Pulumi renderer (shc-pulumi/src/shc_pulumi/sizes.py)
# ---------------------------------------------------------------------------

_SIZES_PULUMI_TEMPLATE = '''"""VM size catalog for SHC, auto-generated from GET /ordering/catalog.

Spec-encoding names follow the {line}-{cpu}c-{ram}gb convention:
    nvme-2c-8gb, ssd-1c-4gb, hdd-4c-16gb, dev-2c-8gb

The static SIZE_MAP is the default fast path (no network, no auth).
"""

from __future__ import annotations

SIZE_MAP: dict[str, dict] = {
__ENTRIES__
}

_DAILY_PRICES = {p: float(v) for p, v in {
__PRICES__
}.items()}

_LINE_RANK = {"nvme": 0, "ssd": 1, "hdd": 2, "dev": 3}


def resolve_size(size: str) -> tuple[int, int]:
    entry = SIZE_MAP.get(size.lower().strip())
    if not entry:
        valid = ", ".join(SIZE_MAP.keys())
        raise ValueError(f"Unknown size '{size}'. Valid: {valid}")
    return int(entry["package_id"]), int(entry["pricing_id"])


def resolve_specs(
    cpu: int | None = None,
    ram_mb: int | None = None,
    disk_gb: int | None = None,
    *,
    line: str | None = None,
) -> tuple[int, int]:
    candidates = []
    for entry in SIZE_MAP.values():
        if line and entry["line"] != line:
            continue
        if cpu and entry["cpu"] < cpu:
            continue
        if ram_mb and entry["ram_mb"] < ram_mb:
            continue
        if disk_gb and entry["disk_gb"] < disk_gb:
            continue
        candidates.append(entry)
    if not candidates:
        raise ValueError(f"No plan matches: cpu>={cpu}, ram>={ram_mb}, disk>={disk_gb}, line={line}")
    cheapest = min(candidates, key=lambda e: (_DAILY_PRICES[e["package_id"]], _LINE_RANK[e["line"]]))
    return int(cheapest["package_id"]), int(cheapest["pricing_id"])
'''


def render_sizes_pulumi(cache: dict) -> str:
    """Render shc-pulumi/src/shc_pulumi/sizes.py."""
    rows = _size_rows(cache)
    max_key = max(len(f'"{r["spec_key"]}":') for r in rows)
    max_pkg = max(len(str(r["package_id"])) for r in rows)
    max_pri = max(len(str(r["pricing_id"])) for r in rows)
    max_cpu = max(len(str(r["cpu"])) for r in rows)
    max_ram = max(len(str(r["ram_mb"])) for r in rows)
    max_disk = max(len(str(r["disk_gb"])) for r in rows)
    max_line = max(len(r["line"]) for r in rows)

    entry_lines = []
    for r in rows:
        key = f'"{r["spec_key"]}":'.ljust(max_key) + " "
        pkg = (str(r["package_id"]) + ",").ljust(max_pkg + 1) + " "
        pri = (str(r["pricing_id"]) + ",").ljust(max_pri + 1) + " "
        cpu = (str(r["cpu"]) + ",").ljust(max_cpu + 1) + " "
        ram = (str(r["ram_mb"]) + ",").ljust(max_ram + 1) + " "
        disk = (str(r["disk_gb"]) + ",").ljust(max_disk + 1) + " "
        line = ('"' + r["line"] + '",').ljust(max_line + 3) + " "
        entry_lines.append(
            f'    {key}{{"package_id": {pkg}"pricing_id": {pri}'
            f'"cpu": {cpu}"ram_mb": {ram}"disk_gb": {disk}'
            f'"line": {line}"name": "{r["name"]}"}},'
        )

    # Group daily prices by line (rows are pre-sorted by line, so runs are contiguous).
    price_lines = []
    current_line = None
    group: list[str] = []
    for r in rows:
        if r["line"] != current_line:
            if group:
                price_lines.append("    " + ", ".join(group) + ",")
            current_line = r["line"]
            group = []
        group.append(f'{r["package_id"]}: {r["daily_price"]}')
    if group:
        price_lines.append("    " + ", ".join(group) + ",")

    body = _SIZES_PULUMI_TEMPLATE.replace("__ENTRIES__", "\n".join(entry_lines))
    body = body.replace("__PRICES__", "\n".join(price_lines))
    return body


# ---------------------------------------------------------------------------
# Drift check
# ---------------------------------------------------------------------------

def check_drift(live: list[dict], cached: dict) -> list[str]:
    """Return list of human-readable drift descriptions. Empty = no drift."""
    diffs = []
    live_pkgs = {p["package_id"]: p for p in live}
    cached_pkgs = {p["package_id"]: p for p in cached.get("packages", [])}

    for pkg_id in sorted(set(live_pkgs) | set(cached_pkgs)):
        if pkg_id not in cached_pkgs:
            diffs.append(f"package {pkg_id} added live: {live_pkgs[pkg_id]['name']}")
            continue
        if pkg_id not in live_pkgs:
            diffs.append(f"package {pkg_id} removed live (still cached): {cached_pkgs[pkg_id]['name']}")
            continue
        lp, cp = live_pkgs[pkg_id], cached_pkgs[pkg_id]
        for field in ("cpu", "memory_mb", "disk_gb", "bandwidth_gb", "name"):
            lv = lp.get(field)
            cv = cp.get(field)
            if lv != cv:
                diffs.append(f"package {pkg_id} field '{field}': cached={cv!r} live={lv!r}")
        live_daily = next((pr["price"] for pr in lp.get("pricing", []) if pr.get("period") == "day"), None)
        cached_daily = next((pr["price"] for pr in cp.get("pricings", []) if pr.get("period") == "day"), None)
        if live_daily is not None and cached_daily is not None and live_daily != cached_daily:
            diffs.append(f"package {pkg_id} daily price: cached={cached_daily!r} live={live_daily!r}")
    return diffs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

RENDERERS = {
    "python": render_sizes_py,
    "go": render_sizes_go,
    "pulumi": render_sizes_pulumi,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch the SHC catalog and regenerate sizes tables in Python, Go, or Pulumi form.",
    )
    parser.add_argument("--format", choices=list(RENDERERS), default="python",
                        help="Output format (default: python)")
    parser.add_argument("--output", default=None,
                        help="Output path. Default: python -> shc_toolkit/sizes.py; go/pulumi -> stdout")
    parser.add_argument("--from-cache", action="store_true",
                        help="Read catalog_cache.json instead of fetching live")
    parser.add_argument("--check", action="store_true",
                        help="Compare live catalog vs cached, exit 1 on drift")
    args = parser.parse_args(argv)

    if args.from_cache:
        if not CACHE_PATH.exists():
            print(f"error: cache not found: {CACHE_PATH}", file=sys.stderr)
            return 1
        cache = json.loads(CACHE_PATH.read_text())
    else:
        print("Fetching live catalog...", file=sys.stderr)
        live = fetch_catalog()
        cache = build_cache(live)
        if args.check:
            existing = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {"packages": []}
            diffs = check_drift(live, existing)
            if not diffs:
                print("No drift detected.", file=sys.stderr)
                return 0
            print("DRIFT DETECTED:", file=sys.stderr)
            for d in diffs:
                print(f"  - {d}", file=sys.stderr)
            return 1

    text = RENDERERS[args.format](cache)

    if args.output:
        out_path = Path(args.output)
    elif args.format == "python":
        out_path = SIZES_PATH
    else:
        sys.stdout.write(text)
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text)
    print(f"Wrote {len(cache['packages'])} packages ({args.format}) -> {out_path}", file=sys.stderr)

    # Preserve historical behavior: a live python regen refreshes the cache too.
    if args.format == "python" and not args.from_cache and not args.output:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(cache, indent=2) + "\n")
        print(f"Wrote cache -> {CACHE_PATH}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
