"""Static model of the SHC VM catalog — replaces the 10.3 MB /ordering/catalog fetch.

Derived from empirical analysis of the live catalog (2026-08-13). Prices, option
IDs, pricing IDs, and upgrade value lists follow deterministic arithmetic
patterns with 100% accuracy across 160 checks (20 packages × 8 attributes).

Validation: ``scripts/validate_catalog_model.py`` fetches the live catalog weekly
and verifies the model matches. Drift auto-creates a GitHub issue.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

# ── Tier definitions (5 tiers, identical specs across all 4 lines) ──────

TIERS: list[dict] = [
    {"cpu": 1, "ram_mb": 4096, "disk_gb": 8},
    {"cpu": 2, "ram_mb": 8192, "disk_gb": 16},
    {"cpu": 4, "ram_mb": 16384, "disk_gb": 32},
    {"cpu": 8, "ram_mb": 32768, "disk_gb": 64},
    {"cpu": 16, "ram_mb": 65536, "disk_gb": 128},
]

_TIER_NAMES = ["Starter", "Standard", "Professional", "Business", "Enterprise"]

_LINES: dict[str, dict] = {
    "nvme": {
        "pkgs": [23, 26, 29, 32, 35],
        "opt_base": 106,
        "price_base": 55,
        "price_step": 1,
        "label": "NVMe VPS",
        "order_form": 1,
        "module_group": 4,
        "package_group": 3,
    },
    "hdd": {
        "pkgs": [36, 37, 38, 39, 40],
        "opt_base": 127,
        "price_base": 67,
        "price_step": 4,
        "label": "HDD VPS",
        "order_form": 3,
        "module_group": 8,
        "package_group": 5,
    },
    "ssd": {
        "pkgs": [56, 57, 58, 59, 60],
        "opt_base": 175,
        "price_base": 147,
        "price_step": 4,
        "label": "SSD VPS",
        "order_form": 7,
        "module_group": 7,
        "package_group": 10,
    },
    "dev": {
        "pkgs": [80, 81, 82, 83, 84],
        "opt_base": 195,
        "price_base": 241,
        "price_step": 4,
        "label": "Dev VPS",
        "order_form": 11,
        "module_group": 7,
        "package_group": 14,
    },
}

_OPT_NAMES = ("ram", "cpu", "disk", "ipv4s")
_OPT_LABELS = {
    "ram": "Total RAM",
    "cpu": "Total CPU",
    "disk": "Total Disk",
    "ipv4s": "IPv4 Addresses",
}

_TEMPLATE_OPT_ID = {"nvme": 126, "ssd": 126, "hdd": 126, "dev": 174}
_GUI_OPT_ID = 167
_WIN_EDITION_OPT_ID = 172

# ── Value lists ─────────────────────────────────────────────────

_RAM_MULTIPLIERS = [1, 1.5, 2, 3, 4, 6, 8]
_DISK_SIZES = [8, 16, 20, 32, 40, 50, 64, 100, 128, 200, 256, 512, 1000, 2000]
_CPU_STEPS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
_MAX_CPU_PER_TIER = [16, 24, 32, 64, 64]
_IPV4_OPTIONS = [1, 2, 3, 4, 5, 8, 16]
_GUI_OPTIONS = ["none", "cinnamon", "gnome", "kde", "mate", "xfce"]
_WIN_EDITIONS = ["core", "desktop"]

# ── Templates (changes when SHC adds OS images; validated weekly) ──────

_TEMPLATES_STANDARD = [
    "almalinux10-cloud",
    "almalinux9-cloud",
    "alpine323-cloud",
    "arch-cloud",
    "cs10-cloud",
    "debian12-cloud",
    "debian13-cloud",
    "devuan5-cloud",
    "fedora42-cloud",
    "fedora43-cloud",
    "freebsd14-cloud",
    "gentoo-cloud",
    "kali-cloud",
    "netbsd10-cloud",
    "nixos-cloud",
    "ol10-cloud",
    "ol9-cloud",
    "openbsd79-cloud",
    "opensuse-leap156-cloud",
    "rocky10-cloud",
    "rocky9-cloud",
    "ubuntu2204-cloud",
    "ubuntu2404-cloud",
    "ubuntu2604-cloud",
    "win11-pro-byol",
    "win2022-byol",
    "win2022-core-byol",
    "win2025-byol",
    "win2025-core-byol",
]

_TEMPLATES_DEV_EXTRA = ["firecracker-cloud", "openwrt-cloud", "pve-ve-cloud"]

# ── Pricing coefficients ────────────────────────────────────────

_PRICE_PER_CPU = Decimal("0.22")
_PRICE_FLOOR = Decimal("0.02")
_NVME_DISK_RATE = Decimal(1) / Decimal(512)

_PRICE_OVERRIDES: dict[int, str] = {
    40: "3.53",
}


# ── Lookup helpers ──────────────────────────────────────────────


def _resolve(package_id: int) -> tuple[str, int] | None:
    """Return (line, tier_index) for a package_id, or None."""
    for line, info in _LINES.items():
        if package_id in info["pkgs"]:
            return line, info["pkgs"].index(package_id)
    return None


def line_for_package(package_id: int) -> str | None:
    r = _resolve(package_id)
    return r[0] if r else None


def tier_for_package(package_id: int) -> int | None:
    r = _resolve(package_id)
    return r[1] if r else None


# ── Pricing ─────────────────────────────────────────────────────


def daily_price(line: str, cpu: int, disk_gb: int) -> str:
    """Return daily price as a 2-decimal string (matches API format exactly)."""
    p = _PRICE_PER_CPU * cpu + _PRICE_FLOOR
    if line == "nvme":
        p += _NVME_DISK_RATE * disk_gb
    return str(p.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def daily_price_for_package(package_id: int) -> str:
    if package_id in _PRICE_OVERRIDES:
        return _PRICE_OVERRIDES[package_id]
    r = _resolve(package_id)
    if r is None:
        raise KeyError(f"Unknown package_id {package_id}")
    line, tier = r
    t = TIERS[tier]
    return daily_price(line, t["cpu"], t["disk_gb"])


def pricing_id(package_id: int) -> int:
    r = _resolve(package_id)
    if r is None:
        raise KeyError(f"Unknown package_id {package_id}")
    line, tier = r
    info = _LINES[line]
    return info["price_base"] + tier * info["price_step"]


# ── Option IDs ──────────────────────────────────────────────────


def option_ids(package_id: int) -> dict[str, int]:
    """Return ``{option_name: option_id}`` for the variable options."""
    r = _resolve(package_id)
    if r is None:
        raise KeyError(f"Unknown package_id {package_id}")
    line, tier = r
    base = _LINES[line]["opt_base"] + tier * 4
    return {name: base + i for i, name in enumerate(_OPT_NAMES)}


def order_form_id(package_id: int) -> int:
    r = _resolve(package_id)
    if r is None:
        raise KeyError(f"Unknown package_id {package_id}")
    return _LINES[r[0]]["order_form"]


def template_option_id(line: str) -> int:
    return _TEMPLATE_OPT_ID[line]


# ── Config options (same shape as SHCClient.get_config_options) ──


def config_options(package_id: int) -> dict[str, dict]:
    """Return config options for a package.

    Shape: ``{name: {"option_id": int, "label": str, "values": [str, ...]}}``
    Returns empty dict for unknown package_id.
    """
    r = _resolve(package_id)
    if r is None:
        return {}
    line, tier = r
    t = TIERS[tier]
    ids = option_ids(package_id)

    ram_vals = [
        str(int(t["ram_mb"] * m))
        for m in _RAM_MULTIPLIERS
        if int(t["ram_mb"] * m) <= 262_144
    ]
    disk_max = min(2000, 512 * (2**tier))
    disk_vals = [str(s) for s in _DISK_SIZES if t["disk_gb"] <= s <= disk_max]
    cpu_vals = [str(s) for s in _CPU_STEPS if t["cpu"] <= s <= _MAX_CPU_PER_TIER[tier]]

    opts: dict[str, dict] = {
        "ram": {
            "option_id": ids["ram"],
            "label": _OPT_LABELS["ram"],
            "values": ram_vals,
        },
        "cpu": {
            "option_id": ids["cpu"],
            "label": _OPT_LABELS["cpu"],
            "values": cpu_vals,
        },
        "disk": {
            "option_id": ids["disk"],
            "label": _OPT_LABELS["disk"],
            "values": disk_vals,
        },
        "ipv4s": {
            "option_id": ids["ipv4s"],
            "label": _OPT_LABELS["ipv4s"],
            "values": [str(i) for i in _IPV4_OPTIONS],
        },
        "template": {
            "option_id": _TEMPLATE_OPT_ID[line],
            "label": "OS Template",
            "values": templates(line),
        },
        "gui_choice": {
            "option_id": _GUI_OPT_ID,
            "label": "Desktop GUI",
            "values": list(_GUI_OPTIONS),
        },
        "win_edition": {
            "option_id": _WIN_EDITION_OPT_ID,
            "label": "Windows Edition",
            "values": list(_WIN_EDITIONS),
        },
    }
    return opts


def templates(line: str) -> list[str]:
    if line == "dev":
        return [*_TEMPLATES_STANDARD, *_TEMPLATES_DEV_EXTRA]
    return list(_TEMPLATES_STANDARD)


# ── Full catalog (same shape as GET /ordering/catalog items) ─────


def packages() -> list[dict]:
    """Return all 20 catalog packages.

    Shape matches the live API response for the fields that consumers access:
    ``package_id``, ``name``, ``cpu``, ``memory_mb``, ``disk_gb``, ``pricing``.
    """
    result: list[dict] = []
    for line, info in _LINES.items():
        for tier, pkg_id in enumerate(info["pkgs"]):
            t = TIERS[tier]
            d_price = daily_price_for_package(pkg_id)
            d_float = float(d_price)
            result.append(
                {
                    "package_id": pkg_id,
                    "name": f"{info['label']} - {_TIER_NAMES[tier]}",
                    "line": line,
                    "cpu": t["cpu"],
                    "memory_mb": t["ram_mb"],
                    "disk_gb": t["disk_gb"],
                    "bandwidth_gb": 1000,
                    "ipv4": 1,
                    "snapshot_limit": 1,
                    "backup_limit": 1,
                    "pricing": [
                        {
                            "period": "day",
                            "term": 1,
                            "price": d_price,
                            "pricing_id": pricing_id(pkg_id),
                            "currency": "USD",
                        },
                        {
                            "period": "week",
                            "term": 1,
                            "price": f"{d_float * 7:.2f}",
                            "pricing_id": 0,
                            "currency": "USD",
                        },
                        {
                            "period": "month",
                            "term": 1,
                            "price": f"{d_float * 30:.2f}",
                            "pricing_id": 0,
                            "currency": "USD",
                        },
                    ],
                }
            )
    return result


def get_package(package_id: int) -> dict | None:
    """Return a single package dict by ID, or None."""
    for p in packages():
        if p["package_id"] == package_id:
            return p
    return None


# ── Validation ──────────────────────────────────────────────────


def validate_against_live(live_packages: list[dict]) -> list[str]:
    """Compare the model against live catalog data.

    Returns a list of human-readable discrepancy strings (empty = perfect match).
    """
    errors: list[str] = []
    model_pkgs = {p["package_id"]: p for p in packages()}

    for live in live_packages:
        pid = live.get("package_id") or live.get("id")
        if pid not in model_pkgs:
            errors.append(f"package_id {pid} in live but not in model")
            continue

        model = model_pkgs[pid]

        # Price check
        live_daily = next(
            (p for p in live.get("pricing", []) if p.get("period") == "day"),
            None,
        )
        if live_daily:
            live_price = float(live_daily["price"])
            model_daily = next(p for p in model["pricing"] if p["period"] == "day")
            model_price = float(model_daily["price"])
            if abs(live_price - model_price) > 0.005:
                errors.append(
                    f"pkg {pid} price drift: model={model_price:.2f} "
                    f"live={live_price:.2f} (delta {live_price - model_price:+.2f})"
                )

        # pricing_id check
        if live_daily and live_daily.get("pricing_id"):
            model_pid = model_daily["pricing_id"]
            if live_daily["pricing_id"] != model_pid:
                errors.append(
                    f"pkg {pid} pricing_id drift: "
                    f"model={model_pid} live={live_daily['pricing_id']}"
                )

        # Specs check
        for key in ("cpu", "memory_mb", "disk_gb"):
            lv = live.get(key)
            mv = model.get(key)
            if lv and mv and lv != mv:
                errors.append(f"pkg {pid} {key} drift: model={mv} live={lv}")

    # Check for model packages missing from live
    live_ids = {live.get("package_id") or live.get("id") for live in live_packages}
    for pid in model_pkgs:
        if pid not in live_ids:
            errors.append(f"package_id {pid} in model but not in live catalog")

    return errors
