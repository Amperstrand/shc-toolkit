#!/usr/bin/env python3
"""SHC dynamic inventory script for Ansible.

Reads SHC_API_KEY from environment, lists all VMs, and outputs Ansible
inventory JSON. Each VM becomes a host with its IP as ansible_host.

Usage in ansible.cfg or CLI:
    ansible all -i ansible/shc_inventory.py -m ping

Groups:
    - shc: all SHC VMs
    - shc_ready: VMs with provisioning_state == "ready"
    - shc_<tier>: e.g. shc_nvme, shc_dev, shc_ssd, shc_hdd

    OS-based grouping is intentionally NOT implemented: VmSummary (returned
    by GET /vm) does not include a template/OS field, and per-VM detail
    lookups would add one API call per host per inventory run. Add a
    `get_vm_detail()` call here only if you accept that cost.

Requires: shc-toolkit installed (pip install -e .) and SHC_API_KEY set.
"""
from __future__ import annotations

import json
import os
import sys


def build_inventory(vms: list[dict]) -> dict:
    """Pure function: turn a list of VmSummary dicts into an Ansible
    inventory payload. No I/O — testable without SHC access.

    Skips VMs with no IPv4. Tier group falls back to "dev" when the package
    name does not contain one of nvme/ssd/hdd.
    """
    inventory: dict[str, dict] = {
        "shc": {"hosts": [], "vars": {"ansible_user": "debian"}},
        "shc_ready": {"hosts": []},
        "_meta": {"hostvars": {}},
    }

    for vm in vms:
        sid = str(vm.get("id", ""))
        hostname = vm.get("hostname", sid)
        state = vm.get("provisioning_state", "unknown")
        ips = vm.get("ips", [])
        ip = ips[0]["ip"] if ips else ""

        if not ip:
            continue

        host_name = hostname or f"shc-{sid}"

        inventory["shc"]["hosts"].append(host_name)
        inventory["_meta"]["hostvars"][host_name] = {
            "ansible_host": ip,
            "shc_service_id": sid,
            "shc_hostname": hostname,
            "shc_state": state,
        }

        if state == "ready":
            inventory["shc_ready"]["hosts"].append(host_name)

        package_name = vm.get("package", "").lower()
        tier = "dev"
        if "nvme" in package_name:
            tier = "nvme"
        elif "ssd" in package_name:
            tier = "ssd"
        elif "hdd" in package_name:
            tier = "hdd"

        tier_group = f"shc_{tier}"
        inventory.setdefault(tier_group, {"hosts": []})["hosts"].append(host_name)

    return inventory


def main() -> None:
    list_mode = len(sys.argv) == 1 or sys.argv[1] == "--list"

    if not list_mode:
        if sys.argv[1] == "--host":
            print(json.dumps({}))
            return

    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from shc_toolkit import SHCClient

        client = SHCClient()
        vms = client.list_vms()
    except Exception as exc:
        print(
            json.dumps(
                {
                    "_meta": {"hostvars": {}},
                    "all": {"hosts": []},
                    "shc": {"hosts": [], "children": []},
                }
            )
        )
        print(f"ERROR: {exc}", file=sys.stderr)
        return

    print(json.dumps(build_inventory(vms), indent=2))


if __name__ == "__main__":
    main()
