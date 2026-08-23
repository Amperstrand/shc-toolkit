"""Named profiles (aws/gcloud-style) unifying the two prior credential
stores: legacy ``contexts.json`` (name -> api_key) and register's
``contexts/<name>.json`` (full credential set incl. the account nsec).

Layout: ``~/.config/shc/profiles/<name>.json`` (0600), same schema as
register contexts — the npub IS the account identity, surfaced in
listings. Resolution precedence (aws-style): flag > ``SHC_PROFILE`` env
> ``SHC_API_KEY`` env > active profile pointer. Migration from both
legacy stores happens lazily and non-destructively on first use.
"""
from __future__ import annotations

import json
import os
import stat
from pathlib import Path

PROFILES_DIR = Path.home() / ".config" / "shc" / "profiles"
ACTIVE_PTR = Path.home() / ".config" / "shc" / "active_profile"
_LEGACY_KEYS = Path.home() / ".config" / "shc" / "contexts.json"
_LEGACY_CTX_DIR = Path.home() / ".config" / "shc" / "contexts"

# credential fields (register schema); legacy key-only profiles get the
# rest as None and remain perfectly usable
FIELDS = ("email", "password", "client_id", "api_key", "nsec", "npub")


def _read(path: Path) -> dict | None:
    try:
        d = json.loads(path.read_text())
        return d if isinstance(d, dict) else None
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def migrate_legacy() -> int:
    """One-time, non-destructive: copy legacy stores into profiles/.
    Returns the number migrated. Sources are left in place."""
    n = 0
    if not PROFILES_DIR.exists():
        # register's full-credential contexts
        if _LEGACY_CTX_DIR.is_dir():
            for p in _LEGACY_CTX_DIR.glob("*.json"):
                d = _read(p)
                if d and d.get("api_key"):
                    _write(PROFILES_DIR / p.name, d)
                    n += 1
        # legacy name->api_key map (only names not already taken)
        legacy = _read(_LEGACY_KEYS)
        if isinstance(legacy, dict):
            for name, key in legacy.items():
                tgt = PROFILES_DIR / f"{name}.json"
                if not tgt.exists() and isinstance(key, str) and key:
                    _write(tgt, {"api_key": key,
                                 **{f: None for f in FIELDS if f != "api_key"}})
                    n += 1
    return n


def list_profiles() -> list[dict]:
    """[{name, npub|None, email|None, client_id|None, active}]."""
    migrate_legacy()
    active = active_profile()
    out = []
    for p in sorted(PROFILES_DIR.glob("*.json")):
        d = _read(p) or {}
        out.append({
            "name": p.stem,
            "npub": d.get("npub"),
            "email": d.get("email"),
            "client_id": d.get("client_id"),
            "active": p.stem == active,
        })
    return out


def get_profile(name: str) -> dict | None:
    migrate_legacy()
    return _read(PROFILES_DIR / f"{name}.json")


def set_active(name: str) -> None:
    ACTIVE_PTR.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_PTR.write_text(name)


def active_profile() -> str | None:
    try:
        return ACTIVE_PTR.read_text().strip() or None
    except FileNotFoundError:
        return None


def resolve_key(flag_key: str | None = None) -> tuple[str | None, str | None]:
    """(api_key, profile_name) by precedence:
    flag > SHC_PROFILE (profile lookup) > SHC_API_KEY > active pointer."""
    if flag_key:
        return flag_key, None
    env_profile = os.environ.get("SHC_PROFILE", "").strip()
    if env_profile:
        d = get_profile(env_profile)
        if d and d.get("api_key"):
            return d["api_key"], env_profile
        return None, env_profile  # named but broken — surface the name
    env_key = os.environ.get("SHC_API_KEY", "").strip()
    if env_key:
        return env_key, None
    act = active_profile()
    if act:
        d = get_profile(act)
        if d and d.get("api_key"):
            return d["api_key"], act
    return None, None
