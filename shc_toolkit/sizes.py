# flake8: noqa: E501
"""VM size catalog for SHC, auto-generated from GET /ordering/catalog.

Spec-encoding names follow the {line}-{cpu}c-{ram}gb convention:
    nvme-2c-8gb, ssd-1c-4gb, hdd-4c-16gb, dev-2c-8gb

The static SIZE_MAP is the default fast path (no network, no auth).
For live pricing, use SHCClient.get_catalog().

Regenerate:
    python scripts/generate_sizes.py
"""

from __future__ import annotations

SIZE_MAP: dict[str, dict] = {
    "nvme-1c-4gb": {"package_id": 23, "cpu": 1, "ram_mb": 4096, "disk_gb": 8, "line": "nvme", "name": "NVMe VPS - Starter", "daily_price": "0.26"},
    "nvme-2c-8gb": {"package_id": 26, "cpu": 2, "ram_mb": 8192, "disk_gb": 16, "line": "nvme", "name": "NVMe VPS - Standard", "daily_price": "0.49"},
    "nvme-4c-16gb": {"package_id": 29, "cpu": 4, "ram_mb": 16384, "disk_gb": 32, "line": "nvme", "name": "NVMe VPS - Professional", "daily_price": "0.96"},
    "nvme-8c-32gb": {"package_id": 32, "cpu": 8, "ram_mb": 32768, "disk_gb": 64, "line": "nvme", "name": "NVMe VPS - Business", "daily_price": "1.91"},
    "nvme-16c-64gb": {"package_id": 35, "cpu": 16, "ram_mb": 65536, "disk_gb": 128, "line": "nvme", "name": "NVMe VPS - Enterprise", "daily_price": "3.79"},
    "ssd-1c-4gb": {"package_id": 56, "cpu": 1, "ram_mb": 4096, "disk_gb": 8, "line": "ssd", "name": "SSD VPS - Starter", "daily_price": "0.24"},
    "ssd-2c-8gb": {"package_id": 57, "cpu": 2, "ram_mb": 8192, "disk_gb": 16, "line": "ssd", "name": "SSD VPS - Standard", "daily_price": "0.46"},
    "ssd-4c-16gb": {"package_id": 58, "cpu": 4, "ram_mb": 16384, "disk_gb": 32, "line": "ssd", "name": "SSD VPS - Professional", "daily_price": "0.90"},
    "ssd-8c-32gb": {"package_id": 59, "cpu": 8, "ram_mb": 32768, "disk_gb": 64, "line": "ssd", "name": "SSD VPS - Business", "daily_price": "1.78"},
    "ssd-16c-64gb": {"package_id": 60, "cpu": 16, "ram_mb": 65536, "disk_gb": 128, "line": "ssd", "name": "SSD VPS - Enterprise", "daily_price": "3.54"},
    "hdd-1c-4gb": {"package_id": 36, "cpu": 1, "ram_mb": 4096, "disk_gb": 8, "line": "hdd", "name": "HDD VPS - Starter", "daily_price": "0.24"},
    "hdd-2c-8gb": {"package_id": 37, "cpu": 2, "ram_mb": 8192, "disk_gb": 16, "line": "hdd", "name": "HDD VPS - Standard", "daily_price": "0.46"},
    "hdd-4c-16gb": {"package_id": 38, "cpu": 4, "ram_mb": 16384, "disk_gb": 32, "line": "hdd", "name": "HDD VPS - Professional", "daily_price": "0.90"},
    "hdd-8c-32gb": {"package_id": 39, "cpu": 8, "ram_mb": 32768, "disk_gb": 64, "line": "hdd", "name": "HDD VPS - Business", "daily_price": "1.78"},
    "hdd-16c-64gb": {"package_id": 40, "cpu": 16, "ram_mb": 65536, "disk_gb": 128, "line": "hdd", "name": "HDD VPS - Enterprise", "daily_price": "3.53"},
    "dev-1c-4gb": {"package_id": 80, "cpu": 1, "ram_mb": 4096, "disk_gb": 8, "line": "dev", "name": "Dev VPS - Starter", "daily_price": "0.24"},
    "dev-2c-8gb": {"package_id": 81, "cpu": 2, "ram_mb": 8192, "disk_gb": 16, "line": "dev", "name": "Dev VPS - Standard", "daily_price": "0.46"},
    "dev-4c-16gb": {"package_id": 82, "cpu": 4, "ram_mb": 16384, "disk_gb": 32, "line": "dev", "name": "Dev VPS - Professional", "daily_price": "0.90"},
    "dev-8c-32gb": {"package_id": 83, "cpu": 8, "ram_mb": 32768, "disk_gb": 64, "line": "dev", "name": "Dev VPS - Business", "daily_price": "1.78"},
    "dev-16c-64gb": {"package_id": 84, "cpu": 16, "ram_mb": 65536, "disk_gb": 128, "line": "dev", "name": "Dev VPS - Enterprise", "daily_price": "3.54"},
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
        raise ValueError(f"Unknown size \"{size}\". Valid sizes: {valid}")
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
    23: 55,  # nvme-1c-4gb
    26: 56,  # nvme-2c-8gb
    29: 57,  # nvme-4c-16gb
    32: 58,  # nvme-8c-32gb
    35: 59,  # nvme-16c-64gb
    56: 147,  # ssd-1c-4gb
    57: 151,  # ssd-2c-8gb
    58: 155,  # ssd-4c-16gb
    59: 159,  # ssd-8c-32gb
    60: 163,  # ssd-16c-64gb
    36: 67,  # hdd-1c-4gb
    37: 71,  # hdd-2c-8gb
    38: 75,  # hdd-4c-16gb
    39: 79,  # hdd-8c-32gb
    40: 83,  # hdd-16c-64gb
    80: 241,  # dev-1c-4gb
    81: 245,  # dev-2c-8gb
    82: 249,  # dev-4c-16gb
    83: 253,  # dev-8c-32gb
    84: 257,  # dev-16c-64gb
}
