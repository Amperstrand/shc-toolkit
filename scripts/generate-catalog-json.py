#!/usr/bin/env python3
"""Generate the machine-readable catalog artifact (issue #37).

Dumps the static catalog model (``shc_toolkit/catalog_model.py``) into a
stable JSON document for cross-language consumers (Go provider, Pulumi
bridge, external tooling) — no SHC API call, no network, no deps: the
model module is loaded standalone (stdlib importlib) so this runs in any
bare CI job.

Output contract (``catalog.json``, repo root):
  * ``schema``      — artifact format version ("shc-catalog/1")
  * ``api_version`` — SHC API version the model encodes
  * ``toolkit_version`` — from pyproject.toml
  * ``lines``       — per line: label, storefront triple
                      (order_form/module_group/package_group ids),
                      template option id, templates, packages[]
  * ``packages``    — flat per-package view: specs, spec name, daily
                      price + pricing_id, option ids, templates

Deterministic: sorted keys, indent 2, trailing newline — two runs on the
same model produce byte-identical output (diff-friendly in git).

Usage:
    python3 scripts/generate-catalog-json.py            # write catalog.json
    python3 scripts/generate-catalog-json.py --check    # exit 1 if drift
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "shc-catalog/1"


def _load_standalone() -> dict:
    """Load catalog_model + pyproject version without importing the package.

    catalog_model is stdlib-only, but importing it as shc_toolkit.catalog_model
    pulls in shc_toolkit/__init__ (httpx). Standalone loading keeps this
    generator runnable in dependency-free CI jobs (same trick as
    audit_cross_repo.py).
    """
    spec = importlib.util.spec_from_file_location(
        "catalog_model_standalone", ROOT / "shc_toolkit" / "catalog_model.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    pyproject = (ROOT / "pyproject.toml").read_text()
    m = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    toolkit_version = m.group(1) if m else "unknown"
    return {"cm": mod, "toolkit_version": toolkit_version}


def build() -> dict:
    loaded = _load_standalone()
    cm = loaded["cm"]
    api_version = ""
    try:
        api_version = re.search(
            r'"version":\s*"([0-9.]+)"',
            (ROOT / "shc_toolkit" / "openapi.json").read_text()[:2000],
        ).group(1)
    except (FileNotFoundError, AttributeError):
        pass

    lines_out: dict[str, dict] = {}
    packages_out: list[dict] = []

    for line_name in sorted(cm._LINES):
        info = cm._LINES[line_name]
        line_pkgs = []
        for pkg_id in info["pkgs"]:
            pkg = cm.get_package(pkg_id)
            if pkg is None:
                continue
            tier = cm.tier_for_package(pkg_id) or 0
            entry = {
                "package_id": pkg_id,
                "name": pkg["name"],
                "line": line_name,
                "tier": cm._TIER_NAMES[tier]
                if tier < len(cm._TIER_NAMES)
                else str(tier),
                "spec": f"{line_name}-{pkg['cpu']}c-{pkg['memory_mb'] // 1024}gb",
                "cpu": pkg["cpu"],
                "ram_mb": pkg["memory_mb"],
                "disk_gb": pkg["disk_gb"],
                "bandwidth_gb": pkg.get("bandwidth_gb"),
                "ipv4": pkg.get("ipv4"),
                "snapshot_limit": pkg.get("snapshot_limit"),
                "backup_limit": pkg.get("backup_limit"),
                "daily_price": cm.daily_price_for_package(pkg_id),
                "pricing_id_daily": cm.pricing_id(pkg_id),
                "option_ids": cm.option_ids(pkg_id),
                "templates": cm.templates(line_name),
            }
            line_pkgs.append(entry)
            packages_out.append(entry)
        lines_out[line_name] = {
            "label": info["label"],
            "order_form_id": info["order_form"],
            "module_group_id": info["module_group"],
            "package_group_id": info["package_group"],
            "template_option_id": cm.template_option_id(line_name),
            "packages": line_pkgs,
        }

    return {
        "schema": SCHEMA,
        "api_version": api_version,
        "toolkit_version": loaded["toolkit_version"],
        "lines": lines_out,
        "packages": sorted(packages_out, key=lambda p: p["package_id"]),
    }


def render(doc: dict) -> str:
    return json.dumps(doc, indent=2, sort_keys=True, default=str) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if catalog.json differs from the current model (CI drift gate)",
    )
    args = parser.parse_args()

    out_path = ROOT / "catalog.json"
    rendered = render(build())

    if args.check:
        current = out_path.read_text() if out_path.exists() else ""
        if current != rendered:
            print(
                f"::error::catalog.json is stale vs shc_toolkit/catalog_model.py — "
                f"regenerate: python3 {out_path.name.replace('catalog.json', 'generate-catalog-json.py') if False else 'scripts/generate-catalog-json.py'}",
                file=sys.stderr,
            )
            return 1
        print("catalog.json up to date ✅")
        return 0

    out_path.write_text(rendered)
    n_pkgs = len(json.loads(rendered)["packages"])
    print(f"wrote {out_path} ({n_pkgs} packages, schema {SCHEMA})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
