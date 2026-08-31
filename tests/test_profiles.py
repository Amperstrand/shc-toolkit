"""Offline tests for the profiles system (aws/gcloud-style multi-account).

Run: python3 -m pytest tests/test_profiles.py -v
"""

import json

import pytest

from shc_toolkit import profiles as P


@pytest.fixture()
def home(tmp_path, monkeypatch):
    monkeypatch.setattr(P.Path, "home", lambda: tmp_path)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    # reset module-level paths for the tmp home
    monkeypatch.setattr(P, "PROFILES_DIR", tmp_path / ".config/shc/profiles")
    monkeypatch.setattr(P, "ACTIVE_PTR", tmp_path / ".config/shc/active_profile")
    monkeypatch.setattr(P, "_LEGACY_KEYS", tmp_path / ".config/shc/contexts.json")
    monkeypatch.setattr(P, "_LEGACY_CTX_DIR", tmp_path / ".config/shc/contexts")
    return tmp_path


def _write_profile(home, name, npub=None, key=None, client=None):
    d = home / ".config/shc/profiles"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{name}.json"
    p.write_text(
        json.dumps(
            {
                "email": f"{npub}@nomail.name" if npub else None,
                "password": "pw",
                "client_id": client,
                "api_key": key or f"shc_live_{name}",
                "nsec": None,
                "npub": npub,
            }
        )
    )
    return p


def test_migrate_from_register_contexts(home):
    ctx = home / ".config/shc/contexts"
    ctx.mkdir(parents=True)
    (ctx / "acct1.json").write_text(
        json.dumps(
            {
                "email": "a@nomail.name",
                "password": "p",
                "client_id": 1,
                "api_key": "shc_live_a",
                "nsec": "nsec1x",
                "npub": "npub1a",
            }
        )
    )
    n = P.migrate_legacy()
    assert n == 1
    got = P.get_profile("acct1")
    assert got["api_key"] == "shc_live_a" and got["npub"] == "npub1a"


def test_migrate_from_legacy_keymap(home):
    (home / ".config/shc").mkdir(parents=True)
    (home / ".config/shc/contexts.json").write_text(
        json.dumps({"prod": "shc_live_prod", "old": "shc_live_old"})
    )
    n = P.migrate_legacy()
    assert n == 2
    assert P.get_profile("prod")["api_key"] == "shc_live_prod"
    assert P.get_profile("prod")["npub"] is None  # key-only import


def test_list_shows_npub_and_active(home):
    _write_profile(home, "a", npub="npub1aaa", client=111)
    _write_profile(home, "b", npub="npub1bbb", client=222)
    P.set_active("b")
    listing = {p["name"]: p for p in P.list_profiles()}
    assert listing["a"]["npub"] == "npub1aaa" and not listing["a"]["active"]
    assert listing["b"]["active"] is True and listing["b"]["client_id"] == 222


def test_resolution_precedence(home, monkeypatch):
    _write_profile(home, "p1", npub="npub1x", key="shc_live_one")
    _write_profile(home, "p2", npub="npub2x", key="shc_live_two")
    P.set_active("p2")
    # flag beats everything
    assert P.resolve_key("shc_live_flag")[0] == "shc_live_flag"
    # SHC_PROFILE beats active pointer and SHC_API_KEY
    monkeypatch.setenv("SHC_PROFILE", "p1")
    monkeypatch.setenv("SHC_API_KEY", "shc_live_env")
    assert P.resolve_key()[0] == "shc_live_one"
    # SHC_API_KEY beats active pointer
    monkeypatch.delenv("SHC_PROFILE")
    assert P.resolve_key()[0] == "shc_live_env"
    # active pointer last
    monkeypatch.delenv("SHC_API_KEY")
    assert P.resolve_key()[0] == "shc_live_two"


def test_broken_env_profile_surfaces_name(home, monkeypatch):
    monkeypatch.setenv("SHC_PROFILE", "ghost")
    key, prof = P.resolve_key()
    assert key is None and prof == "ghost"


def test_file_modes_are_0600(home):
    # go through the library writer — the enforcement under test
    P._write(P.PROFILES_DIR / "sec.json", {"api_key": "k", "npub": "npub1s"})
    assert (P.PROFILES_DIR / "sec.json").stat().st_mode & 0o777 == 0o600
