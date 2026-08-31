#!/usr/bin/env python3
"""Generate size tables for downstream repos from the static catalog model.

Reads from ``shc_toolkit/catalog_model.py`` (no network call, no API key needed).

Usage:
    # Generate Go for terraform-provider-shc:
    python3 scripts/generate_sizes.py --format go --output ../terraform-provider-shc/provider/sizes.go

    # Generate Pulumi sizes:
    python3 scripts/generate_sizes.py --format pulumi --output ../shc-pulumi/src/shc_pulumi/sizes.py

    # Print Go to stdout:
    python3 scripts/generate_sizes.py --format go

The Python toolkit's sizes.py derives from catalog_model.py at import time —
no generation needed for Python.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shc_toolkit.catalog_model import _LINES as _model_lines
from shc_toolkit.catalog_model import packages as _packages
from shc_toolkit.catalog_model import pricing_id as _pricing_id
from shc_toolkit.catalog_model import templates as _templates
from shc_toolkit.sizes import spec_name


def _rows() -> list[dict]:
    """Build flat row dicts from the catalog model."""
    result = []
    for pkg in _packages():
        daily = next(p for p in pkg["pricing"] if p["period"] == "day")
        result.append(
            {
                "spec_key": spec_name(pkg["line"], pkg["cpu"], pkg["memory_mb"]),
                "package_id": pkg["package_id"],
                "pricing_id": _pricing_id(pkg["package_id"]),
                "cpu": pkg["cpu"],
                "ram_mb": pkg["memory_mb"],
                "disk_gb": pkg["disk_gb"],
                "line": pkg["line"],
                "name": pkg["name"],
                "daily_price": float(daily["price"]),
            }
        )
    return result


# ── Go renderer (terraform-provider-shc/provider/sizes.go) ──────────

_GO_TEMPLATE = """package provider

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
		return 0, 0, fmt.Errorf("unknown size '%s'. Valid sizes: nvme-{1,2,4,8,16}c-{4,8,16,32,64}gb, ssd-*, hdd-*, dev-*", size)
	}
	return s.PackageID, s.PricingID, nil
}

func resolveSizeFull(size string) (pkgID, priceID, cpu, ramMB int64, diskGB int64, line string, dailyPrice float64, err error) {
	s, ok := sizeMap[size]
	if !ok {
		return 0, 0, 0, 0, 0, "", 0, fmt.Errorf("unknown size '%s'", size)
	}
	return s.PackageID, s.PricingID, s.CPU, s.RamMB, s.DiskGB, s.Line, s.DailyPrice, nil
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

// knownTemplates is generated from catalog_model — do not edit by hand.
var knownTemplates = []string{
__TEMPLATES__
}

var lineOrderFormIDs = map[string]int64{
__ORDER_FORMS__
}

// Storefront triples per line (SHC validates order_form_id together with
// module_group_id/package_group_id against the plan's storefront path, and
// the order-time ssh_key only survives the FULL triple — a lone form id
// 400s (form 11) or silently drops the key (forms 1/7). Values captured
// from live shc order --dry-run normalized_request, 2026-08-21).
var lineModuleGroupIDs = map[string]int64{
__MODULE_GROUPS__
}

var linePackageGroupIDs = map[string]int64{
__PACKAGE_GROUPS__
}

func orderFormIDForPackage(packageID int64) (int64, bool) {
	for _, s := range sizeMap {
		if s.PackageID == packageID {
			if formID, ok := lineOrderFormIDs[s.Line]; ok {
				return formID, true
			}
		}
	}
	return 0, false
}

func dailyPriceForPackage(packageID int64) (float64, bool) {
	for _, s := range sizeMap {
		if s.PackageID == packageID {
			return s.DailyPrice, true
		}
	}
	return 0, false
}
"""


def render_go() -> str:
    rows = _rows()
    max_key = max(len(f'"{r["spec_key"]}":') for r in rows)
    lines = []
    for r in rows:
        key = f'\t"{r["spec_key"]}":'
        pad = " " * (max_key - len(key.strip()) + 1)
        lines.append(
            f"{key}{pad}{{{r['package_id']}, {r['pricing_id']}, {r['cpu']}, "
            f'{r["ram_mb"]}, {r["disk_gb"]}, "{r["line"]}", "{r["name"]}", {r["daily_price"]:.2f}}},'
        )
    tmpl_lines = "\n".join(f'\t"{t}",' for t in sorted(_templates("dev")))
    form_lines = "\n".join(
        f'\t"{line}": {info["order_form"]},' for line, info in _model_lines.items()
    )
    mg_lines = "\n".join(
        f'\t"{line}": {info["module_group"]},' for line, info in _model_lines.items()
    )
    pg_lines = "\n".join(
        f'\t"{line}": {info["package_group"]},' for line, info in _model_lines.items()
    )
    return (
        _GO_TEMPLATE.replace("__ENTRIES__", "\n".join(lines))
        .replace("__TEMPLATES__", tmpl_lines)
        .replace("__ORDER_FORMS__", form_lines)
        .replace("__MODULE_GROUPS__", mg_lines)
        .replace("__PACKAGE_GROUPS__", pg_lines)
    )


# ── Pulumi renderer (shc-pulumi/src/shc_pulumi/sizes.py) ────────────

_PULUMI_TEMPLATE = '''"""VM size catalog for SHC, generated from catalog_model.py.

Spec-encoding names follow the {line}-{cpu}c-{ram}gb convention:
    nvme-2c-8gb, ssd-1c-4gb, hdd-4c-16gb, dev-2c-8gb
"""

from __future__ import annotations

SIZE_MAP: dict[str, dict] = {
__ENTRIES__
}

_PRICING_LOOKUP: dict[int, int] = {
__PRICING__
}


def resolve_size(size: str) -> tuple[int, int]:
    entry = SIZE_MAP.get(size.lower().strip())
    if not entry:
        valid = ", ".join(SIZE_MAP)
        raise ValueError(f"Unknown size '{size}'. Valid: {valid}")
    return entry["package_id"], _PRICING_LOOKUP[entry["package_id"]]


def resolve_specs(cpu=None, ram_mb=None, disk_gb=None, *, line=None):
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
        raise ValueError(f"No plan matches: cpu>={cpu}, ram_mb>={ram_mb}, disk_gb>={disk_gb}, line={line}")
    cheapest = min(candidates, key=lambda e: float(e["daily_price"]))
    return cheapest["package_id"], _PRICING_LOOKUP[cheapest["package_id"]]


def list_sizes(line=None):
    result = []
    for name, entry in SIZE_MAP.items():
        if line and entry["line"] != line:
            continue
        result.append({"size": name, **entry})
    return result


def spec_name(line, cpu, ram_mb):
    return f"{line}-{cpu}c-{ram_mb // 1024}gb"
'''


def render_pulumi() -> str:
    rows = _rows()
    entries = []
    pricing = []
    for r in rows:
        entries.append(
            f'    "{r["spec_key"]}": {{"package_id": {r["package_id"]}, "cpu": {r["cpu"]}, '
            f'"ram_mb": {r["ram_mb"]}, "disk_gb": {r["disk_gb"]}, "line": "{r["line"]}", '
            f'"name": "{r["name"]}", "daily_price": "{r["daily_price"]:.2f}"}},'
        )
        pricing.append(f"    {r['package_id']}: {r['pricing_id']},")
    return _PULUMI_TEMPLATE.replace("__ENTRIES__", "\n".join(entries)).replace(
        "__PRICING__", "\n".join(pricing)
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate size tables for downstream repos from catalog_model.py"
    )
    parser.add_argument(
        "--format",
        choices=["go", "pulumi"],
        default="go",
        help="Output format (default: go)",
    )
    parser.add_argument("--output", help="Output path (default: stdout)")
    args = parser.parse_args()

    if args.format == "go":
        output = render_go()
    else:
        output = render_pulumi()

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(output)} bytes to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
