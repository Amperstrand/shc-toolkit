#!/usr/bin/env python3
"""Audit feature parity across all 3 SHC repos.

Run from shc-toolkit root (sibling repos expected at ../terraform-provider-shc
and ../shc-pulumi).

Usage:
    python scripts/audit_cross_repo.py          # full report
    python scripts/audit_cross_repo.py --check   # exit 1 on any mismatch
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TF_ROOT = ROOT.parent / "terraform-provider-shc"
PULUMI_ROOT = ROOT.parent / "shc-pulumi"

REPOS = {
    "shc-toolkit": ROOT,
    "terraform-provider-shc": TF_ROOT,
    "shc-pulumi": PULUMI_ROOT,
}


def check_size_map_parity() -> list[str]:
    issues = []

    toolkit_map = _parse_python_sizes(ROOT / "shc_toolkit" / "sizes.py")
    pulumi_map = _parse_python_sizes(PULUMI_ROOT / "src" / "shc_pulumi" / "sizes.py")
    go_map = _parse_go_sizes(TF_ROOT / "provider" / "sizes.go")

    for name, (pkg, pricing) in toolkit_map.items():
        if name in pulumi_map:
            p_pkg, p_pricing = pulumi_map[name]
            if p_pkg != pkg:
                issues.append(f"[SIZES] {name}: toolkit pkg={pkg} but pulumi pkg={p_pkg}")
            if p_pricing and pricing and p_pricing != pricing:
                issues.append(f"[SIZES] {name}: toolkit pricing={pricing} but pulumi pricing={p_pricing}")
        else:
            issues.append(f"[SIZES] {name}: in toolkit but missing from pulumi")

        if name in go_map:
            g_pkg, g_pricing = go_map[name]
            if g_pkg != pkg:
                issues.append(f"[SIZES] {name}: toolkit pkg={pkg} but tf pkg={g_pkg}")
            if g_pricing and pricing and g_pricing != pricing:
                issues.append(f"[SIZES] {name}: toolkit pricing={pricing} but tf pricing={g_pricing}")
        else:
            issues.append(f"[SIZES] {name}: in toolkit but missing from tf")

    for name in set(pulumi_map) - set(toolkit_map):
        issues.append(f"[SIZES] {name}: in pulumi but missing from toolkit")
    for name in set(go_map) - set(toolkit_map):
        issues.append(f"[SIZES] {name}: in tf but missing from toolkit")

    return issues


def _parse_python_sizes(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    src = path.read_text()
    entries = {}
    for m in re.finditer(r'"([\w-]+)":\s*\{[^}]*"package_id":\s*(\d+)', src):
        name = m.group(1)
        pkg = int(m.group(2))
        pricing_match = re.search(r'"pricing_id":\s*(\d+)', m.group(0))
        pricing = int(pricing_match.group(1)) if pricing_match else 0
        entries[name] = (pkg, pricing)
    pricing_lookup = {}
    for m in re.finditer(r"(\d+):\s*(\d+),\s*#\s*[\w-]+", src):
        pricing_lookup[int(m.group(1))] = int(m.group(2))
    if pricing_lookup:
        for name, (pkg, pricing) in entries.items():
            if pricing == 0 and pkg in pricing_lookup:
                entries[name] = (pkg, pricing_lookup[pkg])
    return entries


def _parse_go_sizes(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    src = path.read_text()
    entries = {}
    for m in re.finditer(r'"([\w-]+)":\s*\{(\d+),\s*(\d+),', src):
        entries[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return entries


def check_feature(name: str, repo_root: Path, patterns: list[str], file_glob: str = "**/*") -> bool:
    for pattern in patterns:
        for f in repo_root.glob(file_glob):
            if not f.is_file():
                continue
            fstr = str(f)
            if "/.git/" in fstr or "node_modules" in fstr or "__pycache__" in fstr:
                continue
            try:
                if pattern.lower() in f.read_text(errors="ignore").lower():
                    return True
            except Exception:
                pass
    return False


def check_feature_matrix() -> list[str]:
    issues = []
    features = {
        "Cost audit": {
            "shc-toolkit": ["cost_tracker"],
            "terraform-provider-shc": ["CostTracker"],
            "shc-pulumi": ["estimate_daily_cost"],
        },
        "Config options": {
            "shc-toolkit": ["resolve_addons"],
            "terraform-provider-shc": ["ResolveAddons", "disk_gb"],
            "shc-pulumi": ["resolve_addons", "disk_gb"],
        },
        "Drift detection CI": {
            "shc-toolkit": ["drift"],
            "terraform-provider-shc": ["drift"],
            "shc-pulumi": ["drift"],
        },
        "Orphan cleanup": {
            "shc-toolkit": ["orphan", "CLEANUP"],
            "terraform-provider-shc": ["orphan", "CLEANUP"],
            "shc-pulumi": ["orphan", "Cleanup"],
        },
        "Referral link": {
            "shc-toolkit": ["lecture-mushroom-lunar"],
            "terraform-provider-shc": ["lecture-mushroom-lunar"],
            "shc-pulumi": ["lecture-mushroom-lunar"],
        },
        "Cross-links": {
            "shc-toolkit": ["Related Projects"],
            "terraform-provider-shc": ["Related Projects"],
            "shc-pulumi": ["Related Projects"],
        },
        "5% affiliate disclosure": {
            "shc-toolkit": ["5% recurring"],
            "terraform-provider-shc": ["5% recurring"],
            "shc-pulumi": ["5% recurring"],
        },
    }

    for feature_name, repo_patterns in features.items():
        for repo_name, patterns in repo_patterns.items():
            repo_root = REPOS[repo_name]
            if not check_feature(feature_name, repo_root, patterns):
                issues.append(f"[FEATURE] {repo_name}: missing '{feature_name}'")

    return issues


def check_billing_claims() -> list[str]:
    issues = []
    for repo_name, repo_root in REPOS.items():
        readme = repo_root / "README.md"
        if not readme.exists():
            continue
        content = readme.read_text()
        if "full day even if" in content.lower() or "daily billing minimum" in content.lower():
            issues.append(f"[BILLING] {repo_name}: still claims 'daily billing minimum' (should say hourly proration)")
    return issues


def check_dev_vps_claims() -> list[str]:
    issues = []
    for repo_name, repo_root in REPOS.items():
        readme = repo_root / "README.md"
        if not readme.exists():
            continue
        content = readme.read_text()
        if "not available on dev vps" in content.lower() and "snapshot" in content.lower():
            issues.append(f"[DEVVPS] {repo_name}: still claims Dev VPS snapshots don't work")
    return issues


# ---------------------------------------------------------------------------
# resolve_addons / ResolveAddons contract parity
# ---------------------------------------------------------------------------
#
# All three repos translate friendly specs (disk_gb, ram_mb, cpu, template)
# into SHC's option_id -> value map. The Python implementation lives in
# shc-toolkit (shc-pulumi calls it via dependency); the Go implementation
# lives in terraform-provider-shc. The two must stay in lock-step on:
#   1. accepted parameter names (after language convention)
#   2. return shape (dict[str, str] / map[string]string)
#   3. error semantics for the same edge cases
# This check inspects the source text so it works without executing Go from
# Python (or vice versa). When the audit was added (2026-07-09) the two
# implementations matched; any future drift is a real bug.

PY_PARAMS_EXPECTED = {"package_id", "ram_mb", "cpu", "disk_gb", "template"}
GO_PARAMS_EXPECTED = {"packageID", "diskGB", "ramMB", "cpu", "template"}
EDGE_CASE_MARKERS = [
    "not found in catalog",       # package_id missing
    "does not expose",            # option not present on package
    "not available",              # value not in option's value list
]


def check_resolve_addons_parity() -> list[str]:
    issues: list[str] = []

    py_src_path = ROOT / "shc_toolkit" / "client.py"
    go_src_path = TF_ROOT / "provider" / "client.go"
    go_test_path = TF_ROOT / "provider" / "config_options_test.go"

    if not py_src_path.exists():
        issues.append("[ADDONS] shc_toolkit/client.py missing — cannot check Python resolver")
        return issues
    if not go_src_path.exists():
        issues.append("[ADDONS] terraform-provider-shc/provider/client.go missing — cannot check Go resolver")
        return issues

    py_src = py_src_path.read_text()
    go_src = go_src_path.read_text()

    # 1. Python signature: must accept all 5 conceptual parameters.
    py_sig_match = re.search(r"def resolve_addons\(([^)]*)\)", py_src, re.DOTALL)
    if not py_sig_match:
        issues.append("[ADDONS] Python: resolve_addons definition not found")
    else:
        py_params = {p.strip().split(":")[0].split("=")[0] for p in py_sig_match.group(1).split(",")}
        py_params.discard("self")
        py_params.discard("")
        missing = PY_PARAMS_EXPECTED - py_params
        if missing:
            issues.append(f"[ADDONS] Python resolve_addons missing params: {sorted(missing)}")

    # 2. Go signature: must accept all 5 conceptual parameters (Go naming convention).
    go_sig_match = re.search(r"func \(.*\) ResolveAddons\(([^)]*)\)", go_src, re.DOTALL)
    if not go_sig_match:
        issues.append("[ADDONS] Go: ResolveAddons definition not found")
    else:
        go_params = {p.strip().split()[0] for p in go_sig_match.group(1).split(",") if p.strip()}
        missing = GO_PARAMS_EXPECTED - go_params
        if missing:
            issues.append(f"[ADDONS] Go ResolveAddons missing params: {sorted(missing)}")

    # 3. Return type: both must be string-keyed, string-valued maps.
    if "map[string]string" not in go_src:
        issues.append("[ADDONS] Go ResolveAddons does not return map[string]string")

    py_return_match = re.search(r"def resolve_addons.*?\) -> ([^:]*):", py_src, re.DOTALL)
    if not py_return_match or "dict[str, str]" not in py_return_match.group(1):
        # Some style: "-> dict[str, str]"; allow that match too.
        if "-> dict[str, str]" not in py_src:
            issues.append("[ADDONS] Python resolve_addons does not declare -> dict[str, str]")

    # 4. Edge-case error markers must appear in BOTH implementations.
    for marker in EDGE_CASE_MARKERS:
        if marker.lower() not in py_src.lower():
            issues.append(f"[ADDONS] Python resolve_addons missing error marker: '{marker}'")
        if marker.lower() not in go_src.lower():
            issues.append(f"[ADDONS] Go ResolveAddons missing error marker: '{marker}'")

    # 5. Go must have tests covering the edge cases (parity of test coverage).
    if go_test_path.exists():
        go_tests = go_test_path.read_text()
        required_test_names = ["Success", "MultipleSpecs", "InvalidValue", "PackageNotFound", "NoSpecs"]
        for required in required_test_names:
            if f"TestResolveAddons_{required}" not in go_tests:
                issues.append(f"[ADDONS] Go: missing TestResolveAddons_{required}")
    else:
        issues.append("[ADDONS] terraform-provider-shc: config_options_test.go missing")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Exit 1 on any issue")
    args = parser.parse_args()

    all_issues: list[str] = []

    print("=" * 60)
    print("SHC Cross-Repo Parity Audit")
    print("=" * 60)

    for name, root in REPOS.items():
        exists = "✅" if root.exists() else "❌ NOT FOUND"
        print(f"  {name}: {exists} ({root})")

    print()

    for check_name, check_fn in [
        ("Size Map Parity", check_size_map_parity),
        ("Feature Matrix", check_feature_matrix),
        ("Billing Claims", check_billing_claims),
        ("Dev VPS Claims", check_dev_vps_claims),
        ("resolve_addons Contract", check_resolve_addons_parity),
    ]:
        issues = check_fn()
        status = "✅ PASS" if not issues else f"❌ {len(issues)} issue(s)"
        print(f"\n{'─' * 40}")
        print(f"  {check_name}: {status}")
        print(f"{'─' * 40}")
        for issue in issues:
            print(f"  {issue}")
        all_issues.extend(issues)

    print(f"\n{'=' * 60}")
    if all_issues:
        print(f"TOTAL: {len(all_issues)} issue(s) found")
    else:
        print("TOTAL: All checks passed ✅")
    print("=" * 60)

    if args.check and all_issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
