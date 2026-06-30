"""Human-readable VM size mappings for SHC.

Users can specify a VM by size name instead of opaque package_id/pricing_id IDs.
Three input methods, all backward compatible:

    # Named size (simplest)
    size = "standard"

    # Resource specs (finds cheapest match)
    cpu = 2, ram_mb = 8192

    # Raw IDs (backward compat)
    package_id = 26, pricing_id = 56
"""

from __future__ import annotations

SIZE_MAP: dict[str, dict] = {
    "starter":          {"package_id": 23, "pricing_id": 55,  "cpu": 1,  "ram_mb": 4096,  "disk_gb": 8,   "line": "nvme", "name": "NVMe VPS - Starter"},
    "standard":         {"package_id": 26, "pricing_id": 56,  "cpu": 2,  "ram_mb": 8192,  "disk_gb": 16,  "line": "nvme", "name": "NVMe VPS - Standard"},
    "professional":     {"package_id": 29, "pricing_id": 57,  "cpu": 4,  "ram_mb": 16384, "disk_gb": 32,  "line": "nvme", "name": "NVMe VPS - Professional"},
    "business":         {"package_id": 32, "pricing_id": 58,  "cpu": 8,  "ram_mb": 32768, "disk_gb": 64,  "line": "nvme", "name": "NVMe VPS - Business"},
    "enterprise":       {"package_id": 35, "pricing_id": 59,  "cpu": 16, "ram_mb": 65536, "disk_gb": 128, "line": "nvme", "name": "NVMe VPS - Enterprise"},
    "dev-starter":      {"package_id": 80, "pricing_id": 241, "cpu": 1,  "ram_mb": 4096,  "disk_gb": 8,   "line": "dev",  "name": "Dev VPS - Starter"},
    "dev-standard":     {"package_id": 81, "pricing_id": 245, "cpu": 2,  "ram_mb": 8192,  "disk_gb": 16,  "line": "dev",  "name": "Dev VPS - Standard"},
    "dev-professional": {"package_id": 82, "pricing_id": 249, "cpu": 4,  "ram_mb": 16384, "disk_gb": 32,  "line": "dev",  "name": "Dev VPS - Professional"},
    "dev-business":     {"package_id": 83, "pricing_id": 253, "cpu": 8,  "ram_mb": 32768, "disk_gb": 64,  "line": "dev",  "name": "Dev VPS - Business"},
    "dev-enterprise":   {"package_id": 84, "pricing_id": 257, "cpu": 16, "ram_mb": 65536, "disk_gb": 128, "line": "dev",  "name": "Dev VPS - Enterprise"},
}


def resolve_size(size: str) -> tuple[int, int]:
    """Resolve a named size to (package_id, pricing_id).

    Args:
        size: One of: starter, standard, professional, business, enterprise,
              dev-starter, dev-standard, dev-professional, dev-business, dev-enterprise.

    Returns:
        (package_id, pricing_id) tuple.

    Raises:
        ValueError: If size name is not recognized.
    """
    entry = SIZE_MAP.get(size.lower().strip())
    if not entry:
        valid = ", ".join(SIZE_MAP.keys())
        raise ValueError(f"Unknown size '{size}'. Valid sizes: {valid}")
    return entry["package_id"], entry["pricing_id"]


def resolve_specs(cpu: int | None = None, ram_mb: int | None = None, disk_gb: int | None = None) -> tuple[int, int]:
    """Find the cheapest NVMe plan that meets or exceeds the requested specs.

    Args:
        cpu: Minimum CPU cores required.
        ram_mb: Minimum RAM in MB required.
        disk_gb: Minimum disk in GB required.

    Returns:
        (package_id, pricing_id) of the cheapest matching plan.

    Raises:
        ValueError: If no plan matches the specs.
    """
    candidates = []
    for size_name, entry in SIZE_MAP.items():
        if entry["line"] != "nvme":
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
            f"No NVMe plan matches specs: cpu>={cpu}, ram_mb>={ram_mb}, disk_gb>={disk_gb}"
        )

    cheapest = min(candidates, key=lambda e: e["pricing_id"])
    return cheapest["package_id"], cheapest["pricing_id"]


def list_sizes(line: str | None = None) -> list[dict]:
    """List all available sizes with their specs.

    Args:
        line: Filter by 'nvme' or 'dev'. None = all.

    Returns:
        List of size dicts with name, package_id, pricing_id, cpu, ram_mb, disk_gb, line.
    """
    result = []
    for name, entry in SIZE_MAP.items():
        if line and entry["line"] != line:
            continue
        result.append({"size": name, **entry})
    return result
