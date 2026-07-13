"""gcloud-compute-compatible CLI backed by SHC (Sovereign Hybrid Compute).

Provides drop-in replacement commands for the subset of `gcloud compute`
used by the tollgate cloud lab:

  shc-compute compute instances create <name> --machine-type <type> ...
  shc-compute compute instances list --format=json
  shc-compute compute instances describe <name> --format=json
  shc-compute compute instances delete <name> --quiet
  shc-compute compute instances start <name>
  shc-compute compute instances add-metadata <name> --metadata=k=v,...
  shc-compute compute snapshots create <name> --snapshot-names <name>
  shc-compute compute snapshots list --format=json
  shc-compute compute ssh <name> --command=<cmd>
  shc-compute config get-value project

Output formats match gcloud: --format=json, --format=value(field), --format=get(field).

Machine type mapping:
  n1-standard-2  → Dev VPS Standard  (pkg 81, 2C/8GB)
  n1-standard-4  → Dev VPS Professional (pkg 82, 4C/16GB)
  custom-*       → parsed as vCPU-memory pairs

Metadata: SHC has no native instance metadata. Stored locally in
~/.shc-compute/metadata.json keyed by hostname. Filter queries
(metadata.key=value) check this local store.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from .client import SHCClient, SHCError

# create_client is the transport-aware factory (respects SHC_TRANSPORT env).
# Imported lazily to avoid circular import at package init time.
def _create_client(api_key: str | None = None):
    from shc_toolkit import create_client
    return create_client(api_key=api_key)

MACHINE_TYPE_MAP = {
    "n1-standard-2": {"package_id": 81, "pricing_id": 245, "name": "Dev VPS - Standard"},
    "n1-standard-4": {"package_id": 82, "pricing_id": 249, "name": "Dev VPS - Professional"},
    "n1-standard-8": {"package_id": 83, "pricing_id": 253, "name": "Dev VPS - Business"},
}

DEV_VPS_ORDER_FORM = 11
DEV_VPS_DEBIAN_OPTION = 126
DEV_VPS_SSH_KEY_OPTION = 108
DEV_VPS_IPV4_OPTION = 167
METADATA_FILE = Path.home() / ".shc-compute" / "metadata.json"


def _load_metadata() -> dict:
    if METADATA_FILE.exists():
        return json.loads(METADATA_FILE.read_text())
    return {}


def _save_metadata(data: dict) -> None:
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    METADATA_FILE.write_text(json.dumps(data, indent=2))


def _get_client() -> SHCClient:
    key = os.environ.get("SHC_API_KEY")
    if not key:
        print("ERROR: SHC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return _create_client(api_key=key)


def _vm_to_gcloud_format(vm: dict, metadata: dict | None = None) -> dict:
    """Convert SHC VM to gcloud-compatible instance JSON."""
    service_id = vm.get("id") or vm.get("service_id", "")
    hostname = vm.get("hostname", "")
    ip = vm.get("ipv4") or vm.get("ip") or vm.get("primary_ip", "")
    status_raw = str(vm.get("status", "")).lower()
    status = "RUNNING" if "active" in status_raw or "running" in status_raw else "TERMINATED"

    md = metadata or _load_metadata()
    vm_meta = md.get(hostname, {})

    return {
        "name": hostname,
        "id": str(service_id),
        "status": status,
        "creationTimestamp": vm.get("created_at", ""),
        "zone": "us-central1-a",
        "machineType": "projects/shc/zones/us-central1-a/machineTypes/n1-standard-2",
        "metadata": {
            "fingerprint": "",
            "items": [{"key": k, "value": v} for k, v in vm_meta.items()],
        },
        "networkInterfaces": [{
            "network": "default",
            "subnetwork": "default",
            "networkIP": ip,
            "accessConfigs": [{"natIP": ip, "type": "ONE_TO_ONE_NAT"}],
        }],
        "tags": {"items": vm_meta.get("tags", "").split(",") if vm_meta.get("tags") else []},
        "labels": {k.replace("-", "_"): v for k, v in vm_meta.items() if k.startswith("tollgate")},
    }


def _find_vm_by_name(client: SHCClient, name: str) -> dict | None:
    for vm in client.list_vms():
        if vm.get("hostname") == name:
            return vm
    return None


def _output(data, fmt: str | None):
    if not fmt or fmt == "json":
        print(json.dumps(data, indent=2))
    elif fmt.startswith("get("):
        path = fmt[4:-1]
        obj = data if isinstance(data, dict) else (data[0] if data else {})
        for part in path.replace("[", ".[").split("."):
            if not part:
                continue
            if part.startswith("["):
                idx = int(part[1:-1])
                obj = obj[idx] if isinstance(obj, list) and idx < len(obj) else None
            elif isinstance(obj, dict):
                obj = obj.get(part)
            else:
                obj = None
            if obj is None:
                break
        print(obj if obj is not None else "")
    elif fmt.startswith("value("):
        field = fmt[6:-1]
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict):
                print(item.get(field, ""))
    else:
        print(json.dumps(data, indent=2))


def _parse_metadata_flag(metadata_str: str) -> dict:
    result = {}
    for pair in metadata_str.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k.strip()] = v.strip()
    return result


def _parse_filter(filter_str: str) -> dict:
    filters = {}
    for part in filter_str.split(" "):
        if "=" in part:
            k, v = part.split("=", 1)
            filters[k.strip()] = v.strip()
    return filters


def _vm_matches_filters(vm_gcloud: dict, filters: dict) -> bool:
    for key, val in filters.items():
        if key.startswith("metadata."):
            mk = key[len("metadata."):]
            items = vm_gcloud.get("metadata", {}).get("items", [])
            found = any(i.get("key") == mk and i.get("value") == val for i in items)
            if not found:
                return False
        elif key.startswith("labels."):
            lk = key[len("labels."):]
            if vm_gcloud.get("labels", {}).get(lk) != val:
                return False
        elif key == "name":
            if val not in vm_gcloud.get("name", ""):
                return False
    return True


def _firewall_rules_to_gcloud(fw: dict, instance_name: str = "") -> list[dict]:
    rules_out = []
    for rule in fw.get("rules", []):
        dport = rule.get("dport", "")
        ports = [str(dport)] if str(dport) and str(dport) != "*" else []
        action_raw = str(rule.get("action", "pass")).lower()
        direction_raw = str(rule.get("direction", rule.get("type", "in"))).lower()
        rules_out.append({
            "name": rule.get("comment") or "rule-{rule.get('pos', '?')}",
            "network": "default",
            "direction": "EGRESS" if direction_raw.startswith("out") else "INGRESS",
            "action": "ALLOW" if action_raw in ("pass", "accept", "allow") else "DENY",
            "sourceRanges": [rule["source"]] if rule.get("source") else ["0.0.0.0/0"],
            "allowed": [{"IPProtocol": rule.get("proto", "tcp"), "ports": ports}],
            "instance": instance_name,
            "position": rule.get("pos", ""),
        })
    return rules_out


def cmd_instances(args):
    client = _get_client()
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]

    sub = args[0] if args else ""

    if sub == "list":
        vms = client.list_vms()
        md = _load_metadata()
        instances = [_vm_to_gcloud_format(vm, md) for vm in vms]

        filter_str = ""
        for a in args:
            if a.startswith("--filter="):
                filter_str = a.split("=", 1)[1]
        if filter_str:
            filters = _parse_filter(filter_str)
            instances = [i for i in instances if _vm_matches_filters(i, filters)]

        _output(instances, fmt)

    elif sub == "describe":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if not vm:
            print(json.dumps({"error": "Instance {name} not found"}))
            sys.exit(1)
        md = _load_metadata()
        instance = _vm_to_gcloud_format(vm, md)
        sid = vm.get("id") or vm.get("service_id")
        try:
            detail = client.get_vm_detail(sid)
            power_state = detail.get("power_state") or detail.get("status", {})
            if isinstance(power_state, dict):
                instance["powerState"] = power_state.get("state", str(power_state))
            else:
                instance["powerState"] = str(power_state)
        except Exception:
            instance["powerState"] = instance.get("status", "")
        try:
            fw = client.get_firewall(sid)
            instance["firewalls"] = _firewall_rules_to_gcloud(fw, instance["name"])
        except Exception:
            instance["firewalls"] = []
        _output(instance, fmt)

    elif sub == "create":
        name = args[1] if len(args) > 1 else "shc-vm-{int(time.time())}"
        machine_type = "n1-standard-2"
        snapshot_name = None  # noqa: F841
        metadata = {}
        ssh_key = os.path.expanduser("~/.ssh/id_ed25519.pub")
        disk_size = 16  # noqa: F841

        i = 2
        while i < len(args):
            a = args[i]
            if a.startswith("--machine-type="):
                machine_type = a.split("=", 1)[1]
            elif a.startswith("--source-snapshot="):
                snapshot_name = a.split("=", 1)[1]  # noqa: F841
            elif a.startswith("--metadata="):
                metadata.update(_parse_metadata_flag(a.split("=", 1)[1]))
            elif a.startswith("--metadata-from-file"):
                i += 1
                if i < len(args):
                    fname = args[i]
                    if "=" in fname:
                        k, fp = fname.split("=", 1)
                        metadata[k] = Path(fp).read_text().strip()
            elif a.startswith("--disk="):
                disk_parts = a.split("=", 1)[1]
                for dp in disk_parts.split(","):
                    if dp.startswith("size="):
                        try:
                            disk_size = int(dp[5:]) // 1024  # noqa: F841
                        except ValueError:
                            pass
            elif a.startswith("--tags="):
                metadata["tags"] = a.split("=", 1)[1]
            i += 1

        mt = MACHINE_TYPE_MAP.get(machine_type, MACHINE_TYPE_MAP["n1-standard-2"])

        ssh_key_content = ""
        if Path(ssh_key).exists():
            ssh_key_content = Path(ssh_key).read_text().strip()

        order_kwargs = {
            "package_id": mt["package_id"],
            "pricing_id": mt["pricing_id"],
            "order_form_id": DEV_VPS_ORDER_FORM,
            "hostname": name,
            "options": {
                str(DEV_VPS_SSH_KEY_OPTION): ssh_key_content,
                str(DEV_VPS_DEBIAN_OPTION): "debian12-cloud",
                str(DEV_VPS_IPV4_OPTION): "none",
            },
            "pay": False,
        }

        try:
            result = client.submit_order(**order_kwargs)
            service_id = result.get("service_id") or result.get("id")
        except SHCError:
            print("ERROR ordering VM: {e}", file=sys.stderr)
            sys.exit(1)

        md = _load_metadata()
        md[name] = metadata
        md[name]["service_id"] = str(service_id)
        _save_metadata(md)

        deadline = time.time() + 300
        vm = None
        while time.time() < deadline:
            try:
                vm = client.get_vm(service_id)
                if vm.get("ipv4") or vm.get("ip"):
                    break
            except Exception:
                pass
            time.sleep(10)

        if vm:
            instance = _vm_to_gcloud_format(vm, md)
            _output(instance, fmt)
        else:
            print("Created {name} (service_id={service_id}) but IP not ready yet", file=sys.stderr)

    elif sub == "delete":
        quiet = "--quiet" in args or "-q" in args
        for name in [a for a in args[1:] if not a.startswith("-")]:
            vm = _find_vm_by_name(client, name)
            if vm:
                sid = vm.get("id") or vm.get("service_id")
                client.cancel_vm(sid)
                md = _load_metadata()
                md.pop(name, None)
                _save_metadata(md)
                if not quiet:
                    print("Deleted [{name}]")
            else:
                if not quiet:
                    print("Instance {name} not found")

    elif sub == "start":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if vm:
            sid = vm.get("id") or vm.get("service_id")
            client.start_vm(sid)
            print("Started [{name}]")

    elif sub == "stop":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if vm:
            sid = vm.get("id") or vm.get("service_id")
            client.stop_vm(sid)
            print("Stopped [{name}]")

    elif sub == "reset":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if vm:
            sid = vm.get("id") or vm.get("service_id")
            client.reset_vm(sid)
            print("Reset [{name}]")

    elif sub == "set-machine-type":
        name = args[1] if len(args) > 1 else ""
        machine_type = ""
        for a in args[2:]:
            if a.startswith("--machine-type="):
                machine_type = a.split("=", 1)[1]
        if "/" in machine_type:
            machine_type = machine_type.rstrip("/").split("/")[-1]
        vm = _find_vm_by_name(client, name)
        if not vm:
            print("Instance {name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        mt = MACHINE_TYPE_MAP.get(machine_type)
        if not mt:
            available = ", ".join(sorted(MACHINE_TYPE_MAP))  # noqa: F841
            print("Unknown machine type '{machine_type}'. Available: {available}", file=sys.stderr)
            sys.exit(1)
        client.upgrade_vm(sid, mt["package_id"])
        print("Machine type changed for [{name}] -> {machine_type} ({mt['name']})")

    elif sub == "add-metadata":
        name = args[1] if len(args) > 1 else ""
        metadata = {}
        for a in args[2:]:
            if a.startswith("--metadata="):
                metadata.update(_parse_metadata_flag(a.split("=", 1)[1]))
        md = _load_metadata()
        if name in md:
            md[name].update(metadata)
        else:
            md[name] = metadata
        _save_metadata(md)
        print("Updated metadata for [{name}]")

    elif sub == "restart":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if not vm:
            print("Instance {name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        client.restart_vm(sid)
        print("Restarted [{name}]")

    elif sub == "suspend":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if not vm:
            print("Instance {name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        client.stop_vm(sid)
        print("Suspended [{name}]")

    elif sub == "resume":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if not vm:
            print("Instance {name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        client.start_vm(sid)
        print("Resumed [{name}]")

    elif sub == "shutdown":
        name = args[1] if len(args) > 1 else ""
        vm = _find_vm_by_name(client, name)
        if not vm:
            print("Instance {name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        client.shutdown_vm(sid)
        print("Shutting down [{name}]")

    elif sub == "reinstall":
        name = args[1] if len(args) > 1 else ""
        template = "debian13-cloud"
        for a in args[2:]:
            if a.startswith("--template="):
                template = a.split("=", 1)[1]
            elif a.startswith("--image="):
                template = a.split("=", 1)[1]
        vm = _find_vm_by_name(client, name)
        if not vm:
            print("Instance {name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        client.reinstall_vm(sid, template=template)
        print("Reinstalling [{name}] with template {template}")

    else:
        print("Unknown instances subcommand: {sub}", file=sys.stderr)
        sys.exit(1)


def cmd_snapshots(args):
    client = _get_client()
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]

    sub = args[0] if args else ""

    if sub == "list":
        md = _load_metadata()
        all_snapshots = []
        for hostname, meta in md.items():
            sid = meta.get("service_id")
            if sid:
                try:
                    snaps = client.list_snapshots(int(sid))
                    for s in snaps:
                        all_snapshots.append({
                            "name": s.get("name", s.get("id", "")),
                            "id": str(s.get("id", "")),
                            "status": "READY",
                            "sourceDisk": hostname,
                            "creationTimestamp": s.get("created_at", ""),
                        })
                except Exception:
                    pass
        _output(all_snapshots, fmt)

    elif sub == "create":
        snapshot_name = None  # noqa: F841
        for a in args[1:]:
            if a.startswith("--snapshot-names="):
                snapshot_name = a.split("=", 1)[1]  # noqa: F841
            elif a.startswith("--name="):
                snapshot_name = a.split("=", 1)[1]  # noqa: F841

        name_arg = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        vm_name = name_arg

        vm = _find_vm_by_name(client, vm_name)
        if vm:
            sid = vm.get("id") or vm.get("service_id")
            result = client.create_snapshot(int(sid), name=snapshot_name)
            print(json.dumps({
                "name": snapshot_name or result.get("name", ""),
                "status": "READY",
            }, indent=2))
        else:
            print("Instance {vm_name} not found", file=sys.stderr)
            sys.exit(1)

    elif sub == "delete":
        snapshot_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""  # noqa: F841
        quiet = "--quiet" in args or "-q" in args
        md = _load_metadata()
        deleted = False
        for hostname, meta in md.items():
            sid = meta.get("service_id")
            if sid:
                try:
                    snaps = client.list_snapshots(int(sid))
                    for s in snaps:
                        sname = s.get("name", s.get("id", ""))
                        if sname == snapshot_name or str(s.get("id", "")) == snapshot_name:
                            client._post("/vm/{sid}/snapshots/delete",
                                         {"backup_id": s.get("id", sname)})
                            if not quiet:
                                print("Deleted [{snapshot_name}]")
                            deleted = True
                            break
                except Exception:
                    pass
            if deleted:
                break
        if not deleted and not quiet:
            print("Snapshot {snapshot_name} not found", file=sys.stderr)

    elif sub == "describe":
        snapshot_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""  # noqa: F841
        md = _load_metadata()
        found = None
        for hostname, meta in md.items():
            sid = meta.get("service_id")
            if sid:
                try:
                    snaps = client.list_snapshots(int(sid))
                    for s in snaps:
                        sname = s.get("name", s.get("id", ""))
                        if sname == snapshot_name or str(s.get("id", "")) == snapshot_name:
                            found = {
                                "name": sname,
                                "id": str(s.get("id", "")),
                                "status": "READY",
                                "sourceDisk": hostname,
                                "sourceDiskId": str(sid),
                                "creationTimestamp": s.get("created_at", ""),
                                "diskSizeGb": str(s.get("size", s.get("disk_size", ""))),
                                "storageBytes": str(s.get("storage_bytes", "")),
                                "description": s.get("description", ""),
                            }
                            break
                except Exception:
                    pass
            if found:
                break
        if not found:
            found = {"error": "Snapshot {snapshot_name} not found"}
        _output(found, fmt)

    else:
        print("Unknown snapshots subcommand: {sub}", file=sys.stderr)
        sys.exit(1)


def cmd_ssh(args):
    name = args[0] if args else ""
    command = ""
    for a in args[1:]:
        if a.startswith("--command="):
            command = a.split("=", 1)[1]
        elif a.startswith("--zone="):
            pass
        elif a.startswith("--project="):
            pass

    client = _get_client()
    vm = _find_vm_by_name(client, name)
    if not vm:
        print("Instance {name} not found", file=sys.stderr)
        sys.exit(1)

    ip = vm.get("ipv4") or vm.get("ip", "")
    if not ip:
        print("No IP for {name}", file=sys.stderr)
        sys.exit(1)

    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
               "-o", "LogLevel=ERROR", "root@{ip}"]
    if command:
        ssh_cmd.extend(["--", command])
    os.execvp("ssh", ssh_cmd)


def cmd_firewall_rules(args):
    client = _get_client()
    sub = args[0] if args else ""
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]

    if sub == "list":
        md = _load_metadata()
        all_rules = []
        for hostname, meta in md.items():
            sid = meta.get("service_id")
            if sid:
                try:
                    fw = client.get_firewall(int(sid))
                    all_rules.extend(_firewall_rules_to_gcloud(fw, hostname))
                except Exception:
                    pass
        _output(all_rules, fmt)

    elif sub == "describe":
        vm_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        rule_pos = ""
        for a in args[2:]:
            if not a.startswith("-"):
                rule_pos = a
        vm = _find_vm_by_name(client, vm_name)
        if not vm:
            print("Instance {vm_name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        fw = client.get_firewall(int(sid))
        rules = _firewall_rules_to_gcloud(fw, vm_name)
        if rule_pos:
            pos_int = int(rule_pos) if rule_pos.lstrip("-").isdigit() else -1
            matched = [r for r in rules if str(r.get("position")) == rule_pos or r.get("position") == pos_int]
            _output(matched[0] if matched else {"error": "Rule {rule_pos} not found on {vm_name}"}, fmt)
        else:
            _output(rules[0] if rules else {"error": "No rules found"}, fmt)

    elif sub == "create":
        rule_name = ""
        action = "allow"
        protocol = "tcp"
        ports = ""
        source = "0.0.0.0/0"
        vm_name = ""
        for a in args[1:]:
            if a.startswith("--action=") and "deny" in a: action = "drop"
            elif a.startswith("--rules="):
                parts = a.split("=", 1)[1].split(":")
                if len(parts) >= 2:
                    protocol = parts[0]
                    ports = parts[1]
            elif a.startswith("--source-ranges="):
                source = a.split("=", 1)[1]
            elif not a.startswith("-") and not vm_name:
                vm_name = a
        vm = _find_vm_by_name(client, vm_name)
        if vm:
            sid = vm.get("id") or vm.get("service_id")
            client.create_firewall_rule(int(sid), {
                "action": action,
                "direction": "in",
                "name": rule_name or "rule-{ports}",
                "source": source,
                "dest_port": ports,
                "protocol": protocol,
            })
            print("Firewall rule created for [{vm_name}]: {protocol}:{ports} from {source}")
        else:
            print("Instance {vm_name} not found", file=sys.stderr)
            sys.exit(1)

    elif sub == "delete":
        vm_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        rule_pos = ""
        for a in args[2:]:
            if not a.startswith("-"):
                rule_pos = a
        vm = _find_vm_by_name(client, vm_name)
        if vm:
            sid = vm.get("id") or vm.get("service_id")
            pos = int(rule_pos) if rule_pos.isdigit() else 0
            client.delete_firewall_rule(int(sid), pos)
            print("Deleted firewall rule {rule_pos} for [{vm_name}]")
        else:
            print("Instance {vm_name} not found", file=sys.stderr)

    elif sub == "update":
        vm_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        rule_pos = ""
        updates = {}
        i = 2
        while i < len(args):
            a = args[i]
            if a.startswith("--position="):
                rule_pos = a.split("=", 1)[1]
            elif a.startswith("--action="):
                updates["action"] = "pass" if "allow" in a or "pass" in a else "drop"
            elif a.startswith("--source-ranges="):
                updates["source"] = a.split("=", 1)[1]
            elif a.startswith("--source="):
                updates["source"] = a.split("=", 1)[1]
            elif a.startswith("--rules="):
                parts = a.split("=", 1)[1].split(":")
                if len(parts) >= 2:
                    updates["protocol"] = parts[0]
                    updates["dport"] = parts[1]
            elif a.startswith("--protocol="):
                updates["protocol"] = a.split("=", 1)[1]
            elif a.startswith("--dport="):
                updates["dport"] = a.split("=", 1)[1]
            elif a.startswith("--comment="):
                updates["comment"] = a.split("=", 1)[1]
            elif not a.startswith("-") and not rule_pos:
                rule_pos = a
            i += 1
        vm = _find_vm_by_name(client, vm_name)
        if not vm:
            print("Instance {vm_name} not found", file=sys.stderr)
            sys.exit(1)
        sid = vm.get("id") or vm.get("service_id")
        pos = int(rule_pos) if rule_pos.lstrip("-").isdigit() else 0
        client.edit_firewall_rule(int(sid), pos, **updates)
        print("Updated firewall rule {rule_pos} for [{vm_name}]")


def cmd_images(args):
    client = _get_client()
    sub = args[0] if args else ""
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]
    if sub == "list":
        try:
            templates = client.list_templates()
            images = []
            for t in templates:
                images.append({
                    "name": t.get("name", t.get("id", "")),
                    "family": t.get("family", ""),
                    "status": "READY",
                    "arch": "x86_64",
                })
            _output(images, fmt)
        except Exception:
            _output([], fmt)

    elif sub == "describe":
        image_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        found = None
        try:
            templates = client.list_templates()
            for t in templates:
                tname = t.get("name", t.get("id", ""))
                if tname == image_name:
                    found = {
                        "name": tname,
                        "id": str(t.get("id", "")),
                        "family": t.get("family", ""),
                        "status": "READY",
                        "arch": "x86_64",
                        "creationTimestamp": t.get("created_at", ""),
                        "description": t.get("description", ""),
                    }
                    break
        except Exception:
            pass
        if not found:
            found = {"error": "Image {image_name} not found"}
        _output(found, fmt)


def cmd_config(args):
    sub = args[0] if args else ""
    key = args[1] if len(args) > 1 else ""
    if sub == "get-value":
        if key == "project":
            print("shc-tollgate")


SHC_ZONES = [
    {"name": "us-central1-a", "region": "us-central1", "status": "UP", "description": "Katy, Texas"},
    {"name": "us-central1-b", "region": "us-central1", "status": "UP", "description": "Cherryvale, Kansas"},
]

SHC_REGIONS = [
    {"name": "us-central1", "status": "UP"},
]


def _cmd_machine_types(args):
    client = _get_client()
    sub = args[0] if args else "list"
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]

    if sub == "describe":
        mt_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        if "/" in mt_name:
            mt_name = mt_name.rstrip("/").split("/")[-1]
        mt = MACHINE_TYPE_MAP.get(mt_name)
        if not mt:
            _output({"error": "Machine type {mt_name} not found"}, fmt)
            return
        _output(_machine_type_to_gcloud(mt_name, mt), fmt)
        return

    machine_types = []
    for name, mt in sorted(MACHINE_TYPE_MAP.items()):
        machine_types.append(_machine_type_to_gcloud(name, mt))
    try:
        catalog = client.get_catalog()
        for item in catalog:
            pkg_id = item.get("id") or item.get("package_id")
            if pkg_id and not any(m["id"] == str(pkg_id) for m in machine_types):
                machine_types.append({
                    "name": item.get("name", "pkg-{pkg_id}"),
                    "id": str(pkg_id),
                    "zone": "us-central1-a",
                    "guestCpus": item.get("cpu", ""),
                    "memoryMb": item.get("ram", ""),
                    "description": item.get("description", ""),
                    "selfLink": "projects/shc/zones/us-central1-a/machineTypes/{item.get('name', pkg_id)}",
                })
    except Exception:
        pass
    _output(machine_types, fmt)


def _machine_type_to_gcloud(name: str, mt: dict) -> dict:
    return {
        "name": name,
        "id": str(mt.get("package_id", "")),
        "description": mt.get("name", ""),
        "zone": "us-central1-a",
        "guestCpus": name.split("-")[-1] if name.startswith("n1-standard-") else "",
        "memoryMb": "",
        "selfLink": "projects/shc/zones/us-central1-a/machineTypes/{name}",
    }


def _cmd_zones(args):
    sub = args[0] if args else "list"
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]
    if sub == "list":
        _output([dict(z) for z in SHC_ZONES], fmt)
    elif sub == "describe":
        zone_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        matched = [z for z in SHC_ZONES if z["name"] == zone_name]
        _output(matched[0] if matched else {"error": "Zone {zone_name} not found"}, fmt)


def _cmd_regions(args):
    sub = args[0] if args else "list"
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]
    if sub == "list":
        _output([dict(r) for r in SHC_REGIONS], fmt)
    elif sub == "describe":
        region_name = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        matched = [r for r in SHC_REGIONS if r["name"] == region_name]
        _output(matched[0] if matched else {"error": "Region {region_name} not found"}, fmt)


def _cmd_operations(args):
    client = _get_client()
    sub = args[0] if args else "list"
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]

    if sub == "list":
        vm_name = next((a for a in args[1:] if not a.startswith("-")), "")
        all_ops = []
        if vm_name:
            vm = _find_vm_by_name(client, vm_name)
            if not vm:
                print("Instance {vm_name} not found", file=sys.stderr)
                sys.exit(1)
            sid = vm.get("id") or vm.get("service_id")
            try:
                for job in client.list_jobs(int(sid)):
                    all_ops.append(_job_to_gcloud(job, vm_name, sid))
            except Exception:
                pass
        else:
            md = _load_metadata()
            for hostname, meta in md.items():
                sid = meta.get("service_id")
                if sid:
                    try:
                        for job in client.list_jobs(int(sid)):
                            all_ops.append(_job_to_gcloud(job, hostname, sid))
                    except Exception:
                        pass
        _output(all_ops, fmt)

    elif sub == "describe":
        op_id = args[1] if len(args) > 1 and not args[1].startswith("-") else ""
        vm_name = next((a for a in args[2:] if not a.startswith("-")), "")
        md = _load_metadata()
        found = None
        targets = []
        if vm_name:
            vm = _find_vm_by_name(client, vm_name)
            if vm:
                sid = vm.get("id") or vm.get("service_id")
                targets = [(vm_name, sid)]
        else:
            for hostname, meta in md.items():
                sid = meta.get("service_id")
                if sid:
                    targets.append((hostname, sid))
        for hostname, sid in targets:
            try:
                job = client.get_job(int(sid), op_id)
                found = _job_to_gcloud(job, hostname, sid)
                break
            except Exception:
                pass
        if not found:
            found = {"error": "Operation {op_id} not found"}
        _output(found, fmt)

    else:
        print("Unknown operations subcommand: {sub}", file=sys.stderr)
        sys.exit(1)


def _job_to_gcloud(job: dict, hostname: str, sid) -> dict:
    status_raw = str(job.get("status", job.get("state", ""))).lower()
    if status_raw in ("done", "complete", "completed", "success"):
        op_status = "DONE"
    elif status_raw in ("running", "active", "pending", "queued"):
        op_status = "RUNNING"
    else:
        op_status = status_raw.upper() or "DONE"
    return {
        "name": "operation-{job.get('id', job.get('job_id', ''))}",
        "id": str(job.get("id", job.get("job_id", ""))),
        "operationType": job.get("type", job.get("action", "")),
        "status": op_status,
        "targetId": str(sid),
        "targetLink": "projects/shc/zones/us-central1-a/instances/{hostname}",
        "creationTimestamp": job.get("created_at", job.get("started_at", "")),
        "startTime": job.get("started_at", ""),
        "endTime": job.get("finished_at", job.get("completed_at", "")),
        "progress": job.get("progress", 100 if op_status == "DONE" else 0),
        "description": job.get("message", job.get("detail", "")),
    }


def _cmd_project_info(args):
    client = _get_client()
    sub = args[0] if args else "describe"
    fmt = None
    for a in args:
        if a.startswith("--format="):
            fmt = a.split("=", 1)[1]

    info = {}
    try:
        account = client.get_account()
        info = {
            "projectNumber": str(account.get("id", account.get("client_id", ""))),
            "projectId": "shc-tollgate",
            "name": account.get("name", account.get("company", "")),
            "lifecycleState": "ACTIVE",
            "createTime": account.get("date_created", account.get("created_at", "")),
            "email": account.get("email", ""),
            "x_Platform": "Sovereign Hybrid Compute",
        }
    except Exception:
        info = {"projectId": "shc-tollgate", "lifecycleState": "ACTIVE"}

    if sub == "list":
        _output([info], fmt)
    else:
        _output(info, fmt)


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: shc-compute <command> [args]", file=sys.stderr)
        sys.exit(1)

    cmd = args[0]
    rest = args[1:]

    if cmd == "compute":
        if not rest:
            print("Usage: shc-compute compute <resource> ...", file=sys.stderr)
            sys.exit(1)
        resource = rest[0]
        rest = rest[1:]
        if resource == "instances":
            cmd_instances(rest)
        elif resource == "snapshots":
            cmd_snapshots(rest)
        elif resource == "ssh":
            cmd_ssh(rest)
        elif resource == "firewall-rules":
            cmd_firewall_rules(rest)
        elif resource == "images":
            cmd_images(rest)
        elif resource == "machine-types":
            _cmd_machine_types(rest)
        elif resource == "zones":
            _cmd_zones(rest)
        elif resource == "regions":
            _cmd_regions(rest)
        elif resource == "operations":
            _cmd_operations(rest)
        elif resource == "project-info":
            _cmd_project_info(rest)
        else:
            print("Unknown resource: {resource}", file=sys.stderr)
            sys.exit(1)
    elif cmd == "config":
        cmd_config(rest)
    else:
        print("Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
