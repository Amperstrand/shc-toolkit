"""Tests for the ansible/ integration shipped in this repo.

Two layers:

1. YAML sanity — every playbook, role task list, and group_vars file under
   ``ansible/`` parses as valid YAML. This is the lightest meaningful check
   we can run without depending on ``ansible-lint`` (which is not installed
   locally or in CI). Catches tab/indent/syntax drift the moment a PR lands.

2. ``shc_inventory.py`` behaviour — the dynamic inventory script's
   ``build_inventory()`` is a pure function over VmSummary dicts. Mock the
   data, assert the emitted inventory shape. This is where the audit found
   a stale docstring and missing tests.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ANSIBLE_DIR = REPO_ROOT / "ansible"
INVENTORY_SCRIPT = ANSIBLE_DIR / "shc_inventory.py"

# Playbooks and role files that must parse as YAML. Use paths relative to
# ansible/ so the per-role `main.yml` files don't collide.
_YAML_REL = sorted(
    str(p.relative_to(ANSIBLE_DIR))
    for p in (
        list(ANSIBLE_DIR.glob("*.yml"))
        + list(ANSIBLE_DIR.glob("roles/*/tasks/*.yml"))
        + list(ANSIBLE_DIR.glob("group_vars/*.yml"))
    )
)


def test_all_ansible_yaml_files_parse() -> None:
    """Every shipped YAML file must be syntactically valid."""
    assert _YAML_REL, "expected to find ansible YAML files; glob pattern drifted"
    errors: list[str] = []
    for rel in _YAML_REL:
        path = ANSIBLE_DIR / rel
        try:
            yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: {exc}")
    assert not errors, "YAML parse failures:\n" + "\n".join(errors)


def test_inventory_script_file_exists() -> None:
    """The dynamic inventory script is referenced by README; it must exist."""
    assert INVENTORY_SCRIPT.is_file(), f"missing {INVENTORY_SCRIPT}"


def _load_inventory_module():
    """Import shc_inventory.py as an isolated module (it has no package)."""
    spec = importlib.util.spec_from_file_location("shc_inventory", INVENTORY_SCRIPT)
    assert spec and spec.loader, "could not build module spec for shc_inventory"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fake_vms() -> list[dict]:
    """Return a deterministic cross-tier VM list covering every code branch."""
    return [
        {
            "id": 1001,
            "hostname": "nvme-box",
            "provisioning_state": "ready",
            "package": "NVMe VPS - Standard",
            "ips": [{"ip": "10.0.0.1"}],
        },
        {
            "id": 1002,
            "hostname": "dev-box",
            "provisioning_state": "pending",
            "package": "Dev VPS - 2c/4gb",
            "ips": [{"ip": "10.0.0.2"}],
        },
        {
            "id": 1003,
            "hostname": "ssd-box",
            "provisioning_state": "ready",
            "package": "SSD VPS - Pro",
            "ips": [{"ip": "10.0.0.3"}],
        },
        {
            "id": 1004,
            "hostname": "hdd-box",
            "provisioning_state": "ready",
            "package": "HDD VPS - Starter",
            "ips": [{"ip": "10.0.0.4"}],
        },
        # No IP -> must be skipped.
        {
            "id": 1005,
            "hostname": "no-ip",
            "provisioning_state": "ready",
            "package": "NVMe VPS - X",
            "ips": [],
        },
        # Tier falls back to "dev" when no recognised token is in package.
        {
            "id": 1006,
            "hostname": "unknown-tier",
            "provisioning_state": "ready",
            "package": "Mystery Plan",
            "ips": [{"ip": "10.0.0.6"}],
        },
    ]


def test_build_inventory_groups_and_hostvars() -> None:
    """Tier groups, ready group, hostvars, and the no-IP skip all hold."""
    mod = _load_inventory_module()
    inv = mod.build_inventory(_fake_vms())

    # Total hosts: 5 (no-ip skipped).
    assert len(inv["shc"]["hosts"]) == 5
    # Ready group excludes pending and the skipped no-ip.
    assert sorted(inv["shc_ready"]["hosts"]) == [
        "hdd-box",
        "nvme-box",
        "ssd-box",
        "unknown-tier",
    ]
    # Tier groups.
    assert inv["shc_nvme"]["hosts"] == ["nvme-box"]
    assert sorted(inv["shc_dev"]["hosts"]) == ["dev-box", "unknown-tier"]
    assert inv["shc_ssd"]["hosts"] == ["ssd-box"]
    assert inv["shc_hdd"]["hosts"] == ["hdd-box"]
    # Hostvars carry connection details.
    nvme_vars = inv["_meta"]["hostvars"]["nvme-box"]
    assert nvme_vars["ansible_host"] == "10.0.0.1"
    assert nvme_vars["shc_service_id"] == "1001"
    assert nvme_vars["shc_state"] == "ready"
    # Default ansible_user is baked into the shc group.
    assert inv["shc"]["vars"]["ansible_user"] == "debian"


def test_build_inventory_empty_input() -> None:
    """An empty VM list yields a valid, empty inventory."""
    mod = _load_inventory_module()
    inv = mod.build_inventory([])
    assert inv["shc"]["hosts"] == []
    assert inv["shc_ready"]["hosts"] == []
    assert inv["_meta"]["hostvars"] == {}
    # Tier groups are NOT created when no VMs match.
    assert "shc_nvme" not in inv
    assert "shc_dev" not in inv


def test_build_inventory_hostname_falls_back_to_service_id() -> None:
    """VMs with missing/empty hostname use shc-<id>."""
    mod = _load_inventory_module()
    inv = mod.build_inventory(
        [
            {
                "id": 777,
                "hostname": "",
                "provisioning_state": "ready",
                "package": "NVMe",
                "ips": [{"ip": "10.0.0.9"}],
            }
        ]
    )
    assert inv["shc"]["hosts"] == ["shc-777"]
    assert inv["_meta"]["hostvars"]["shc-777"]["shc_hostname"] == ""


# --------------------------------------------------------------------------------------
# Docstring / comment contracts.
# --------------------------------------------------------------------------------------

def test_inventory_docstring_does_not_promise_os_groups() -> None:
    """The script must NOT advertise OS-based groups (e.g. shc_debian13) in
    its docstring while not implementing them. Audit found this mismatch —
    the VmSummary API has no template field, so OS grouping would require
    N+1 calls per inventory run."""
    src = INVENTORY_SCRIPT.read_text()
    assert "shc_<os>" not in src, "docstring still promises unimplemented OS groups"
    assert "shc_debian13" not in src
    assert "shc_ubuntu2404" not in src


@pytest.mark.parametrize("rel_path", _YAML_REL)
def test_no_stale_inventory_ini_references(rel_path: str) -> None:
    """The non-existent inventory/shc-hosts.ini was referenced from comments
    in playbook.yml and teardown.yml. They must point at the actual
    `-i localhost,` usage documented in README.md."""
    path = ANSIBLE_DIR / rel_path
    content = path.read_text()
    assert "inventory/shc-hosts.ini" not in content, (
        f"{rel_path} still references the non-existent inventory/shc-hosts.ini"
    )
