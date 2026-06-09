"""CLI for SHC VM management."""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid

from .client import SHCClient, SHCError
from .nodns import NoDNSKeyPair, provision_dns_for_vm, publish_dns_records, publish_acme_challenge, verify_dns


def _client(args) -> SHCClient:
    return SHCClient(api_key=args.api_key or os.environ.get("SHC_API_KEY", ""))


def cmd_list(args):
    c = _client(args)
    vms = c.list_vms()
    if not vms:
        print("No VMs found.")
        return
    for vm in vms:
        ip = vm.get("ips", [{}])[0].get("ip", "no-ip") if vm.get("ips") else "no-ip"
        print(
            f"  id={vm['id']:>5}  {vm['hostname']:30s}  {vm['service_status']:10s}  "
            f"{vm.get('runtime_status', '?'):10s}  {ip}"
        )


def cmd_info(args):
    c = _client(args)
    vm = c.get_vm_summary(args.service_id)
    print(json.dumps(vm, indent=2, default=str))


def cmd_order(args):
    c = _client(args)
    ssh_key = None
    if args.ssh_key:
        if os.path.isfile(os.path.expanduser(args.ssh_key)):
            ssh_key = open(os.path.expanduser(args.ssh_key)).read().strip()
        else:
            ssh_key = args.ssh_key

    config = {}
    for opt in args.option or []:
        key, val = opt.split("=", 1)
        config[key] = val

    kwargs: dict = {
        "hostname": args.hostname,
        "package_id": args.package_id,
        "pricing_id": args.pricing_id,
        "config_options": config,
    }
    if args.module_group_id:
        kwargs["module_group_id"] = args.module_group_id
    if ssh_key:
        kwargs["ssh_key"] = ssh_key

    if args.dry_run:
        result = c.preview_order(**kwargs)
        print(json.dumps(result, indent=2, default=str))
        return

    result = c.submit_order(**kwargs)
    print(json.dumps(result, indent=2, default=str))

    # Auto-pay if requested
    if args.pay:
        invoice_id = result.get("invoice", {}).get("invoice_id")
        if invoice_id:
            payment = c.pay_invoice(invoice_id, str(uuid.uuid4()))
            print(f"\nPayment: {json.dumps(payment, indent=2)}")

        # Wait for provisioning
        service_ids = result.get("service_ids", [])
        if service_ids:
            print(f"\nWaiting for VM {service_ids[0]} to provision...")
            vm = c.wait_for_provisioning(service_ids[0])
            ips = vm.get("ips", [])
            ip = ips[0].get("ip", "?") if ips else "?"
            user = vm.get("os_user", "debian")
            print(f"\nVM ready! SSH: ssh {user}@{ip}")


def cmd_pay(args):
    c = _client(args)
    result = c.pay_invoice(args.invoice_id, args.idempotency_key or str(uuid.uuid4()))
    print(json.dumps(result, indent=2, default=str))


def cmd_start(args):
    c = _client(args)
    print(json.dumps(c.start_vm(args.service_id), indent=2, default=str))


def cmd_stop(args):
    c = _client(args)
    print(json.dumps(c.stop_vm(args.service_id), indent=2, default=str))


def cmd_restart(args):
    c = _client(args)
    print(json.dumps(c.restart_vm(args.service_id), indent=2, default=str))


def cmd_cancel(args):
    c = _client(args)
    print(json.dumps(c.cancel_vm(args.service_id), indent=2, default=str))


def cmd_snapshots(args):
    c = _client(args)
    snapshots = c.list_snapshots(args.service_id)
    if not snapshots:
        print("No snapshots.")
        return
    for s in snapshots:
        print(f"  {s.get('id', '?'):20s}  {s.get('name', '(unnamed)'):30s}  {s.get('created_at', '?')}")


def cmd_create_snapshot(args):
    c = _client(args)
    result = c.create_snapshot(args.service_id, args.name)
    print(json.dumps(result, indent=2, default=str))


def cmd_restore_snapshot(args):
    c = _client(args)
    result = c.restore_snapshot(args.service_id, args.snapshot_id)
    print(json.dumps(result, indent=2, default=str))


def cmd_catalog(args):
    c = _client(args)
    catalog = c.get_catalog()
    for pkg in catalog:
        cpu = pkg.get("cpu", "?")
        mem = pkg.get("memory_mb", "?")
        disk = pkg.get("disk_gb", "?")
        daily = next(
            (p for p in pkg.get("pricing", []) if p.get("period") == "day"), None
        )
        price = daily["price"] if daily else "?"
        print(f"  pkg={pkg['package_id']:>3}  {pkg['name']:35s}  {cpu}C/{mem}MB/{disk}GB  ${price}/day")


def main():
    parser = argparse.ArgumentParser(
        prog="shc", description="Sovereign Hybrid Compute CLI"
    )
    parser.add_argument("--api-key", help="SHC API key (or set SHC_API_KEY)")

    sub = parser.add_subparsers(dest="command")

    # list
    p = sub.add_parser("list", help="List VMs")
    p.set_defaults(func=cmd_list)

    # info
    p = sub.add_parser("info", help="VM summary")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_info)

    # catalog
    p = sub.add_parser("catalog", help="List available plans")
    p.set_defaults(func=cmd_catalog)

    # order
    p = sub.add_parser("order", help="Order a new VM")
    p.add_argument("--hostname", required=True)
    p.add_argument("--package-id", type=int, required=True)
    p.add_argument("--pricing-id", type=int, required=True)
    p.add_argument("--module-group-id", type=int)
    p.add_argument("--ssh-key", help="Path to pub key or raw key string")
    p.add_argument("--option", "-o", action="append", help="config key=val (repeatable)")
    p.add_argument("--dry-run", action="store_true", help="Preview only")
    p.add_argument("--pay", action="store_true", help="Auto-pay and wait for provisioning")
    p.set_defaults(func=cmd_order)

    # pay
    p = sub.add_parser("pay", help="Pay an invoice")
    p.add_argument("invoice_id", type=int)
    p.add_argument("--idempotency-key")
    p.set_defaults(func=cmd_pay)

    # start/stop/restart/cancel
    for name, func in [
        ("start", cmd_start),
        ("stop", cmd_stop),
        ("restart", cmd_restart),
        ("cancel", cmd_cancel),
    ]:
        p = sub.add_parser(name, help=f"{name} VM")
        p.add_argument("service_id", type=int)
        p.set_defaults(func=func)

    # snapshots
    p = sub.add_parser("snapshots", help="List snapshots")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_snapshots)

    p = sub.add_parser("snapshot-create", help="Create snapshot")
    p.add_argument("service_id", type=int)
    p.add_argument("--name")
    p.set_defaults(func=cmd_create_snapshot)

    p = sub.add_parser("snapshot-restore", help="Restore snapshot")
    p.add_argument("service_id", type=int)
    p.add_argument("snapshot_id")
    p.set_defaults(func=cmd_restore_snapshot)

    # nodns: DNS provisioning via Nostr
    p = sub.add_parser("nodns", help="Provision DNS via nodns.shop (Nostr)")
    p.add_argument("--ip", required=True, help="VM IP address")
    p.add_argument("--nsec", help="Existing nsec key (generates ephemeral if omitted)")
    p.add_argument("--subdomain", help="Subdomain label (default: root @)")
    p.add_argument("--wait", type=int, default=15, help="Seconds to wait for DNS propagation")
    p.add_argument("--verify", action="store_true", help="Verify DNS resolution after publish")
    p.set_defaults(func=cmd_nodns)

    # dns-verify
    p = sub.add_parser("dns-verify", help="Verify DNS resolution")
    p.add_argument("fqdn", help="Fully qualified domain name")
    p.add_argument("--type", default="A", help="Record type (default: A)")
    p.add_argument("--nameserver", default="ns1.nodns.shop", help="Nameserver to query")
    p.set_defaults(func=cmd_dns_verify)

    def cmd_dns_verify(args):
    result = verify_dns(args.fqdn, args.type, args.nameserver)
    print(json.dumps(result, indent=2))


def cmd_nodns(args):
    keypair = NoDNSKeyPair.from_nsec(args.nsec) if args.nsec else None
    result = provision_dns_for_vm(
        ip=args.ip,
        subdomain=args.subdomain,
        wait_seconds=args.wait,
        keypair=keypair,
    )
    print(json.dumps(result, indent=2, default=str))
    if result["success"]:
        print(f"\nFQDN: {result['fqdn']}")
        print(f"nsec: {result['keypair']['nsec']}")
        print("Save the nsec to update this DNS record later!")


args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except SHCError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
