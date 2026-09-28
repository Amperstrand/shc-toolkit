"""Regression tests for the cloudflared binary search/download security fix.

PR #33 Codex review (r3693462072): /tmp/cf-binary was checked FIRST in the
search path and used as the download target — any local user could plant or
swap an executable there that connect_local() then ran with the invoking
user's privileges, and the `# nosec B108` suppressed exactly that warning.
"""

import os
import stat
import subprocess

import pytest

from shc_toolkit import tunnel


def test_search_paths_have_no_world_writable_directories():
    """No trusted search location may live in a world-writable dir.

    World-writable (0o002) is the plant vector — another LOCAL USER can
    place an executable there. Group-writable convention dirs (some hosts
    ship ~/.local/bin 0775) are not in scope: the threat model is other
    users, not other groups.
    """
    for path in tunnel._CF_BINARY_PATHS:
        parent = os.path.dirname(os.path.abspath(path))
        assert os.path.isdir(parent), f"search-path parent {parent} missing"
        mode = stat.S_IMODE(os.stat(parent).st_mode)
        assert not (mode & 0o002), (
            f"cloudflared search path {path} sits in a group/world-writable "
            f"directory (mode {oct(mode)}) — another local user can plant the "
            "executable connect_local() runs"
        )


def test_cache_dir_refuses_precreated_world_writable_dir(tmp_path, monkeypatch):
    """A pre-existing cache dir that other users can write into (hostile
    pre-creation inside a shared parent, or bad historical perms) must be
    rejected loudly rather than trusted."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    hostile = tmp_path / "shc-toolkit"
    hostile.mkdir()
    os.chmod(hostile, 0o777)  # explicit: mkdir() alone is umask-stripped
    with pytest.raises(tunnel.TunnelError, match="group/world-writable"):
        tunnel._cloudflared_cache_dir()


def test_cache_dir_created_user_owned_0700(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    cache = tunnel._cloudflared_cache_dir()
    assert cache == str(tmp_path / "shc-toolkit")
    st = os.stat(cache)
    assert st.st_uid == os.geteuid()
    assert stat.S_IMODE(st.st_mode) & 0o700 == 0o700
    assert not (stat.S_IMODE(st.st_mode) & 0o077)


def test_download_lands_in_user_cache_atomically(tmp_path, monkeypatch):
    """The binary downloads into the validated user cache via
    temp-file-and-rename — never into a shared directory."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    monkeypatch.setattr(tunnel, "_CF_BINARY_PATHS", [])

    seen = {}

    def fake_wget(cmd, check, timeout):
        target = cmd[cmd.index("-O") + 1]
        seen["target"] = target
        with open(target, "wb") as f:
            f.write(b"#!/bin/sh\n# simulated cloudflared\n")

    monkeypatch.setattr(subprocess, "run", fake_wget)
    result = tunnel._find_cloudflared()

    cache = tmp_path / "shc-toolkit"
    assert result.startswith(str(cache)), (
        "downloaded binary must live in the validated user cache"
    )
    assert seen["target"].startswith(str(cache)), (
        "wget must write only inside the user cache"
    )
    assert os.path.exists(result)
    assert stat.S_IMODE(os.stat(result).st_mode) & 0o111, "binary must be executable"
    assert not os.path.exists(result + ".download"), (
        "partial download must be renamed away"
    )


def test_planted_executable_next_to_cache_is_not_returned(tmp_path, monkeypatch):
    """With trusted installs missing, a planted executable elsewhere never
    wins: the only downloadable/returnable location is the validated cache."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    monkeypatch.setattr(tunnel, "_CF_BINARY_PATHS", [])

    def no_download(*a, **kw):
        raise AssertionError("network download must not run in this test")

    monkeypatch.setattr(subprocess, "run", no_download)
    # No cached binary exists → finder must not fall back anywhere odd.
    with pytest.raises(AssertionError, match="network download"):
        tunnel._find_cloudflared()
