"""Spec-encoding size names for SHC VM plans.

Names follow the {line}-{cpu}c-{ram}gb convention:
    nvme-2c-8gb, ssd-1c-4gb, hdd-4c-16gb, dev-2c-8gb

SIZE_MAP and _PRICING_LOOKUP are derived from ``catalog_model.py`` at import
time — no hardcoded data, no duplication.
"""

from __future__ import annotations

from .catalog_model import packages as _model_packages
from .catalog_model import pricing_id as _model_pricing_id


def spec_name(line: str, cpu: int, ram_mb: int) -> str:
    """Generate a spec-encoding size name from specs."""
    return f"{line}-{cpu}c-{ram_mb // 1024}gb"


# Physical facility (SHC module group) per catalog line. Earned live
# 2026-09-01 (lightning-playground #96 fuzz campaign): the "SSD VPS"
# and "Dev VPS" lines both land in the Cherryvale, Kansas facility,
# which was UNREACHABLE from the EU lab route — two fresh orders sat
# with port 22 closed and the cloud-init bootstrap signal unfired
# (health diagnosed it as a cloud-init deadlock; the real cause was the
# facility), both canceled with refund. The Katy, Texas facility
# (NVMe + HDD lines) provisioned SSH-reachable in under a minute.
# Ordering an ssd-* or dev-* size is therefore a trap for EU-route
# sessions — the CLI surfaces this so nobody re-derives it by burn.
FACILITIES: dict[str, dict] = {
    "nvme": {
        "module_group_id": 4,
        "facility": "Katy, Texas",
        "reachability": "ok",
    },
    "hdd": {
        "module_group_id": 8,
        "facility": "Katy, Texas (HDD)",
        "reachability": "ok",
    },
    "ssd": {
        "module_group_id": 7,
        "facility": "Cherryvale, Kansas",
        "reachability": "unreachable-eu-2026-09-01",
    },
    "dev": {
        "module_group_id": 7,
        "facility": "Cherryvale, Kansas",
        "reachability": "unreachable-eu-2026-09-01",
    },
}


def _build_size_map() -> dict[str, dict]:
    result: dict[str, dict] = {}
    for pkg in _model_packages():
        key = spec_name(pkg["line"], pkg["cpu"], pkg["memory_mb"])
        daily = next(p["price"] for p in pkg["pricing"] if p["period"] == "day")
        fac = FACILITIES.get(pkg["line"], {})
        result[key] = {
            "package_id": pkg["package_id"],
            "cpu": pkg["cpu"],
            "ram_mb": pkg["memory_mb"],
            "disk_gb": pkg["disk_gb"],
            "line": pkg["line"],
            "name": pkg["name"],
            "daily_price": daily,
            "module_group_id": fac.get("module_group_id"),
            "facility": fac.get("facility"),
            "reachability": fac.get("reachability"),
        }
    return result


SIZE_MAP: dict[str, dict] = _build_size_map()

_PRICING_LOOKUP: dict[int, int] = {
    pkg["package_id"]: _model_pricing_id(pkg["package_id"]) for pkg in _model_packages()
}


def resolve_size(size: str) -> tuple[int, int]:
    """Resolve a spec-encoding size name to (package_id, pricing_id).

    Raises:
        ValueError: If size name is not recognized.
    """
    entry = SIZE_MAP.get(size.lower().strip())
    if not entry:
        valid = ", ".join(SIZE_MAP)
        raise ValueError(f'Unknown size "{size}". Valid sizes: {valid}')
    return entry["package_id"], _PRICING_LOOKUP[entry["package_id"]]


def resolve_specs(
    cpu: int | None = None,
    ram_mb: int | None = None,
    disk_gb: int | None = None,
    *,
    line: str | None = None,
) -> tuple[int, int]:
    """Find the cheapest plan that meets or exceeds the requested specs.

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
            f"No plan matches specs: cpu>={cpu}, ram_mb>={ram_mb}, "
            f"disk_gb>={disk_gb}, line={line}"
        )
    cheapest = min(candidates, key=lambda e: float(e["daily_price"]))
    return cheapest["package_id"], _PRICING_LOOKUP[cheapest["package_id"]]


def list_sizes(line: str | None = None) -> list[dict]:
    """List all available sizes, optionally filtered by line."""
    result = []
    for name, entry in SIZE_MAP.items():
        if line and entry["line"] != line:
            continue
        result.append({"size": name, **entry})
    return result
