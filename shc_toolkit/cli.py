"""CLI for SHC VM management."""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid

from typing import Any

from .client import SHCClient, SHCError
from .benchmark import run_full_suite, print_results as print_bench_results

try:
    from .nodns import NoDNSKeyPair, provision_dns_for_vm, publish_dns_records, publish_acme_challenge, verify_dns
except ImportError:
    NoDNSKeyPair = None
    provision_dns_for_vm = None
    verify_dns = None


def _client(args) -> SHCClient:
    from shc_toolkit import create_client
    return create_client(
        api_key=args.api_key or os.environ.get("SHC_API_KEY", "") or None,
    )


def _print(data):
    print(json.dumps(data, indent=2, default=str))


# ── VM Lifecycle ──────────────────────────────────────────

def cmd_list(args):
    c = _client(args)
    vms = c.list_vms()
    if not vms:
        print("No VMs found.")
        return
    for vm in vms:
        ip = vm.get("ips", [{}])[0].get("ip", "no-ip") if vm.get("ips") else "no-ip"
        print(f"  id={vm['id']:>5}  {vm['hostname']:30s}  {vm['service_status']:10s}  {vm.get('runtime_status', '?'):10s}  {ip}")


def cmd_info(args):
    c = _client(args)
    _print(c.get_vm_summary(args.service_id))


def cmd_metrics(args):
    c = _client(args)
    _print(c.get_vm_metrics(args.service_id))


def cmd_bandwidth(args):
    c = _client(args)
    _print(c.get_vm_bandwidth(args.service_id))


def cmd_detail(args):
    c = _client(args)
    _print(c.get_vm_detail(args.service_id))


def cmd_start(args):
    c = _client(args)
    _print(c.start_vm(args.service_id))


def cmd_stop(args):
    c = _client(args)
    _print(c.stop_vm(args.service_id))


def cmd_shutdown(args):
    c = _client(args)
    _print(c.shutdown_vm(args.service_id))


def cmd_reset(args):
    c = _client(args)
    _print(c.reset_vm(args.service_id))


def cmd_restart(args):
    c = _client(args)
    _print(c.restart_vm(args.service_id))


def cmd_health(args):
    c = _client(args)
    import json as _json
    health = c.check_vm_health(args.service_id)
    print(_json.dumps(health, indent=2, default=str))


def cmd_reinstall(args):
    c = _client(args)
    _print(c.reinstall_vm(args.service_id, args.template))


def cmd_cancel(args):
    c = _client(args)
    _print(c.cancel_vm(args.service_id))


# ── Ordering ──────────────────────────────────────────────

def cmd_order(args):
    c = _client(args)
    ssh_key = None
    if args.ssh_key:
        if os.path.isfile(os.path.expanduser(args.ssh_key)):
            ssh_key = open(os.path.expanduser(args.ssh_key)).read().strip()
        else:
            ssh_key = args.ssh_key

    kwargs: dict[str, Any] = {
        "hostname": args.hostname,
        "package_id": args.package_id,
        "pricing_id": args.pricing_id,
    }
    if args.module_group_id:
        kwargs["module_group_id"] = args.module_group_id
    if ssh_key:
        kwargs["ssh_key"] = ssh_key

    if args.dry_run:
        _print(c.preview_order(**kwargs))
        return

    idem = args.idempotency_key or f"order-{uuid.uuid4().hex[:24]}"
    result = c.submit_order(idempotency_key=idem, **kwargs)

    if args.pay or args.pay_qr:
        invoice = result.get("invoice", {})
        invoice_id = invoice.get("invoice_id")
        service_ids = result.get("service_ids", [])
        service_id = service_ids[0] if service_ids else None

        if not invoice_id:
            print("Could not find invoice ID in order result:")
            _print(result)
            return

        # Trigger BTCPay checkout
        pay_result = c._confirmed_request(
            "POST", f"/payment/{invoice_id}/checkout",
            confirm=True,
            json={"gateway": "btcpay_server", "idempotency_key": f"pay-{idem}"},
        )

        checkout_url = pay_result.get("checkout_url", "")
        btcpay_id = pay_result.get("btcpay_invoice_id", "")

        if pay_result.get("status") == "paid":
            print(f"Invoice #{invoice_id} already paid.")
        elif args.pay_qr and checkout_url:
            from .jit_pay import jit_pay
            paid = jit_pay(c, invoice_id, checkout_url, btcpay_id)
            if not paid:
                print(f"\nPayment not received. Pay manually: {checkout_url}")
                return
        elif checkout_url:
            print(f"Pay at: {checkout_url}")
        else:
            _print(pay_result)
            return

        if service_id:
            print(f"\nWaiting for VM {service_id} to provision...")
            try:
                c.wait_for_provisioning(service_id, timeout=300)
                print(f"VM {service_id} is ready!\n")
                vm = c.get_vm(service_id)
                ips = vm.get("ips", [])
                ip = ips[0]["ip"] if ips else "no-ip"
                print(f"  Hostname: {vm.get('hostname', '?')}")
                print(f"  IP:       {ip}")
                print(f"  User:     {vm.get('os_user', 'debian')}")
                print(f"  Status:   {vm.get('service_status', '?')}")
                print(f"\n  SSH: ssh {vm.get('os_user', 'debian')}@{ip}")
            except Exception as e:
                print(f"Provisioning check: {e}")
                _print(c.get_vm(service_id))
        return

    _print(result)


def cmd_catalog(args):
    c = _client(args)
    for pkg in c.get_catalog():
        cpu = pkg.get("cpu", "?")
        mem = pkg.get("memory_mb", "?")
        disk = pkg.get("disk_gb", "?")
        daily = next((p for p in pkg.get("pricing", []) if p.get("period") == "day"), None)
        price = daily["price"] if daily else "?"
        print(f"  pkg={pkg['package_id']:>3}  {pkg['name']:35s}  {cpu}C/{mem}MB/{disk}GB  ${price}/day")


def cmd_pricing(args):
    c = _client(args)
    catalog = c.get_catalog()
    for pkg in catalog:
        name = pkg.get("name", "?")
        daily = next((p for p in pkg.get("pricing", []) if p.get("period") == "day"), {})
        weekly = next((p for p in pkg.get("pricing", []) if p.get("period") == "week"), {})
        monthly = next((p for p in pkg.get("pricing", []) if p.get("period") == "month"), {})
        print(f"  pkg={pkg['package_id']:>3}  {name:35s}  ${daily.get('price','?')}/day  ${weekly.get('price','?')}/wk  ${monthly.get('price','?')}/mo")


# ── Support Tickets ───────────────────────────────────────

def cmd_tickets(args):
    c = _client(args)
    if args.subcommand == "list":
        result = c.list_support_tickets(limit=args.limit or 20)
        items = result.get("items", result) if isinstance(result, dict) else result
        if not items:
            print("No tickets.")
            return
        for t in items:
            print(f"  #{t.get('id','?'):>5}  [{t.get('status','?'):10s}]  {t.get('subject','?')[:60]}")
    elif args.subcommand == "get":
        _print(c.get_support_ticket(args.ticket_id))
    elif args.subcommand == "create":
        msg_text = args.body
        if args.body_file:
            msg_text = open(args.body_file).read()
        result = c.create_support_ticket(
            subject=args.subject,
            message=msg_text,
            department_id=args.department,
            priority=args.priority,
            service_id=args.service_id,
        )
        ticket_id = result.get("id") or result.get("ticket_id", "?")
        print(f"Created ticket #{ticket_id}: {args.subject}")
        _print(result)
    elif args.subcommand == "reply":
        _print(c.reply_support_ticket(args.ticket_id, args.body))
    elif args.subcommand == "close":
        _print(c.close_support_ticket(args.ticket_id))
    elif args.subcommand == "departments":
        for d in c.list_support_departments():
            print(f"  id={d.get('id','?')}  {d.get('name','?')}")
    else:
        print("Usage: shc tickets {list|get|create|reply|close|departments}")
        sys.exit(1)


# ── Billing ───────────────────────────────────────────────

def cmd_balance(args):
    c = _client(args)
    _print(c.get_billing_balance())


def cmd_invoices(args):
    c = _client(args)
    if args.invoice_id:
        _print(c.get_invoice(args.invoice_id))
    else:
        result = c.list_invoices()
        items = result.get("items", result) if isinstance(result, dict) else result
        if not items:
            print("No invoices.")
            return
        for inv in items:
            print(f"  #{inv.get('id','?'):>5}  ${inv.get('total','?'):>8s}  {inv.get('status','?'):10s}  {inv.get('date_created','?')[:10]}")


def cmd_transactions(args):
    c = _client(args)
    result = c.list_transactions()
    items = result.get("items", result) if isinstance(result, dict) else result
    if not items:
        print("No transactions.")
        return
    for t in items:
        print(f"  {t.get('date','?')[:10]}  ${t.get('amount','?'):>8s}  {t.get('type','?'):15s}  {t.get('description','')[:40]}")


def cmd_activity(args):
    c = _client(args)
    if getattr(args, "service_id", None):
        _print(c.get_vm_activity(args.service_id))
        return
    result = c.get_account_activity(limit=args.limit or 20)
    items = result.get("items", result) if isinstance(result, dict) else result
    for a in items:
        print(f"  {str(a.get('created_at','?'))[:19]}  {a.get('type','?'):15s}  {str(a.get('description', a.get('summary','')))[:60]}")


def cmd_emails(args):
    c = _client(args)
    result = c.list_emails()
    items = result.get("items", result) if isinstance(result, dict) else result
    for e in items:
        print(f"  {str(e.get('date','?'))[:10]}  {e.get('subject','?')[:60]}")


def cmd_pay(args):
    c = _client(args)
    _print(c.pay_invoice(args.invoice_id, args.idempotency_key or str(uuid.uuid4())))


# ── Snapshots ─────────────────────────────────────────────

def cmd_snapshots(args):
    c = _client(args)
    for s in c.list_snapshots(args.service_id):
        print(f"  {s.get('id', '?'):20s}  {s.get('name', '(unnamed)'):30s}  {s.get('created_at', '?')}")


def cmd_create_snapshot(args):
    c = _client(args)
    _print(c.create_snapshot(args.service_id, args.name))


def cmd_restore_snapshot(args):
    c = _client(args)
    _print(c.restore_snapshot(args.service_id, args.snapshot_id))


def cmd_delete_snapshot(args):
    c = _client(args)
    _print(c.delete_snapshot(args.service_id, args.snapshot_id))


# ── Backups ───────────────────────────────────────────────

def cmd_backup_list(args):
    c = _client(args)
    backups = c.list_backups(args.service_id)
    if not backups:
        print("No backups found.")
        return
    for b in backups:
        bid = b.get("id", b.get("backup_id", "?"))
        name = b.get("name", "(unnamed)")
        protected = "🔒" if b.get("protected") else ""
        created = b.get("created_at", b.get("date_created", "?"))
        print(f"  {str(bid):30s}  {name:25s}  {protected:2s}  {created}")


def cmd_backup_create(args):
    c = _client(args)
    result = c.create_backup(args.service_id, name=args.name)
    _print(result)


def cmd_backup_restore(args):
    c = _client(args)
    _print(c.restore_backup(args.service_id, args.backup_id))


def cmd_backup_delete(args):
    c = _client(args)
    _print(c.delete_backup(args.service_id, args.backup_id))


def cmd_backup_protect(args):
    c = _client(args)
    protected = not args.off
    _print(c.set_backup_protection(args.service_id, args.backup_id, protected))


# ── Bench ─────────────────────────────────────────────────

def cmd_bench(args):
    c = _client(args)
    vm = c.get_vm_summary(args.service_id)
    ips = vm.get("ips", [])
    if not ips:
        print(f"Error: VM {args.service_id} has no IP assigned yet.", file=sys.stderr)
        sys.exit(1)
    host = ips[0]["ip"]
    user = vm.get("os_user", "debian")
    print(f"Benchmarking VM {args.service_id} ({host})...\n")
    results = run_full_suite(host, user=user, skip_disk=args.skip_disk, skip_network=args.skip_network)
    print_bench_results(results)


# ── NoDNS ─────────────────────────────────────────────────

def cmd_nodns(args):
    keypair = NoDNSKeyPair.from_nsec(args.nsec) if args.nsec else None
    result = provision_dns_for_vm(ip=args.ip, subdomain=args.subdomain, wait_seconds=args.wait, keypair=keypair)
    _print(result)
    if result["success"]:
        print(f"\nFQDN: {result['fqdn']}")
        print(f"nsec: {result['keypair']['nsec']}")


def cmd_dns_verify(args):
    _print(verify_dns(args.fqdn, args.type, args.nameserver))


# ── Firewall ──────────────────────────────────────────────

def cmd_firewall(args):
    c = _client(args)
    if args.subcommand == "show":
        _print(c.get_firewall(args.service_id))
    elif args.subcommand == "policy":
        _print(c.set_firewall_policy(args.service_id, args.policy))
    elif args.subcommand == "add-rule":
        kwargs = {}
        if args.action: kwargs["action"] = args.action
        if args.protocol: kwargs["protocol"] = args.protocol
        if args.port: kwargs["port"] = args.port
        if args.src: kwargs["source"] = args.src
        _print(c.create_firewall_rule(args.service_id, **kwargs))
    elif args.subcommand == "del-rule":
        _print(c.delete_firewall_rule(args.service_id, args.position))
    else:
        print("Usage: shc firewall <service_id> {show|policy|add-rule|del-rule}")
        sys.exit(1)


# ── Account ───────────────────────────────────────────────

def cmd_account(args):
    c = _client(args)
    _print(c.get_account())


# ── VM Lifecycle extras ───────────────────────────────────

def cmd_vm_activity(args):
    c = _client(args)
    _print(c.get_vm_activity(args.service_id))


def cmd_network(args):
    c = _client(args)
    _print(c.get_vm_network(args.service_id))


def cmd_payments(args):
    c = _client(args)
    _print(c.get_vm_payments(args.service_id))


# ── Upgrades ──────────────────────────────────────────────

def cmd_upgrade_options(args):
    c = _client(args)
    _print(c.list_upgrade_options(args.service_id))


def cmd_upgrade_preview(args):
    c = _client(args)
    _print(c.preview_upgrade(args.service_id, args.package_id))


def cmd_upgrade(args):
    c = _client(args)
    _print(c.upgrade_vm(args.service_id, args.package_id))


# ── Jobs ──────────────────────────────────────────────────

def cmd_jobs(args):
    c = _client(args)
    for j in c.list_jobs(args.service_id):
        print(f"  id={j.get('id','?'):>10}  {j.get('status','?'):12s}  {str(j.get('created_at','?'))[:19]}")


def cmd_job(args):
    c = _client(args)
    _print(c.get_job(args.service_id, args.job_id))


# ── SSH Keys ──────────────────────────────────────────────

def cmd_ssh_keys(args):
    c = _client(args)
    _print(c.list_ssh_keys(args.service_id))


def cmd_ssh_key_add(args):
    c = _client(args)
    if os.path.isfile(os.path.expanduser(args.key)):
        key = open(os.path.expanduser(args.key)).read().strip()
    else:
        key = args.key
    _print(c.add_ssh_key(args.service_id, key, args.label or ""))


def cmd_ssh_key_live(args):
    c = _client(args)
    _print(c.apply_ssh_key_live(args.service_id, args.key))


# ── ISO ───────────────────────────────────────────────────

def cmd_iso(args):
    c = _client(args)
    _print(c.list_isos(args.service_id))


def cmd_iso_mount(args):
    c = _client(args)
    _print(c.mount_iso(args.service_id, args.iso_id))


def cmd_iso_unmount(args):
    c = _client(args)
    _print(c.unmount_iso(args.service_id))


# ── Reverse DNS ───────────────────────────────────────────

def cmd_rdns(args):
    c = _client(args)
    _print(c.list_rdns(args.service_id))


def cmd_rdns_set(args):
    c = _client(args)
    _print(c.set_rdns(args.service_id, args.ip, args.ptr))


def cmd_rdns_clear(args):
    c = _client(args)
    _print(c.clear_rdns(args.service_id, args.ip))


# ── Console ───────────────────────────────────────────────

def cmd_console(args):
    c = _client(args)
    _print(c.get_console_availability(args.service_id))


def cmd_console_session(args):
    c = _client(args)
    _print(c.create_console_session(args.service_id))


# ── Templates ─────────────────────────────────────────────

def cmd_templates(args):
    c = _client(args)
    _print(c.list_templates())


# ── Main ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(prog="shc", description="Sovereign Hybrid Compute CLI")
    parser.add_argument("--api-key", help="SHC API key (or set SHC_API_KEY)")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("list", help="List VMs")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("info", help="VM summary")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("detail", help="Enriched VM detail")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_detail)

    p = sub.add_parser("metrics", help="VM time-series metrics")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_metrics)

    p = sub.add_parser("bandwidth", help="VM bandwidth usage")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_bandwidth)

    p = sub.add_parser("catalog", help="List available plans")
    p.set_defaults(func=cmd_catalog)

    p = sub.add_parser("pricing", help="Pricing table")
    p.set_defaults(func=cmd_pricing)

    p = sub.add_parser("bench", help="Run VPS benchmarks")
    p.add_argument("service_id", type=int)
    p.add_argument("--skip-disk", action="store_true")
    p.add_argument("--skip-network", action="store_true")
    p.set_defaults(func=cmd_bench)

    p = sub.add_parser("order", help="Order a new VM")
    p.add_argument("--hostname", required=True)
    p.add_argument("--package-id", type=int, required=True)
    p.add_argument("--pricing-id", type=int, required=True)
    p.add_argument("--module-group-id", type=int)
    p.add_argument("--ssh-key", help="Path to pub key or raw key string")
    p.add_argument("--idempotency-key", help="Client-generated idempotency key")
    p.add_argument("--dry-run", action="store_true", help="Preview only")
    p.add_argument("--pay", action="store_true", help="Auto-pay and wait for provisioning")
    p.add_argument("--pay-qr", action="store_true",
                   help="Show Lightning QR code for just-in-time payment (no balance needed)")
    p.set_defaults(func=cmd_order)

    p = sub.add_parser("pay", help="Pay an invoice")
    p.add_argument("invoice_id", type=int)
    p.add_argument("--idempotency-key")
    p.set_defaults(func=cmd_pay)

    for name, func in [("start", cmd_start), ("stop", cmd_stop), ("shutdown", cmd_shutdown), ("restart", cmd_restart), ("reset", cmd_reset), ("cancel", cmd_cancel)]:
        p = sub.add_parser(name, help=f"{name} VM")
        p.add_argument("service_id", type=int)
        p.set_defaults(func=func)

    p = sub.add_parser("health", help="VM health diagnostics (provisioning, network, runtime)")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_health)

    p = sub.add_parser("reinstall", help="Reinstall OS from template")
    p.add_argument("service_id", type=int)
    p.add_argument("--template", default="debian13-cloud", help="OS template name")
    p.set_defaults(func=cmd_reinstall)

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

    p = sub.add_parser("snapshot-delete", help="Delete snapshot")
    p.add_argument("service_id", type=int)
    p.add_argument("snapshot_id")
    p.set_defaults(func=cmd_delete_snapshot)

    p = sub.add_parser("backups", help="List backups")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_backup_list)

    p = sub.add_parser("backup-create", help="Create backup")
    p.add_argument("service_id", type=int)
    p.add_argument("--name")
    p.set_defaults(func=cmd_backup_create)

    p = sub.add_parser("backup-restore", help="Restore backup")
    p.add_argument("service_id", type=int)
    p.add_argument("backup_id")
    p.set_defaults(func=cmd_backup_restore)

    p = sub.add_parser("backup-delete", help="Delete backup")
    p.add_argument("service_id", type=int)
    p.add_argument("backup_id")
    p.set_defaults(func=cmd_backup_delete)

    p = sub.add_parser("backup-protect", help="Toggle backup protection")
    p.add_argument("service_id", type=int)
    p.add_argument("backup_id")
    p.add_argument("--off", action="store_true", help="Remove protection (default: add)")
    p.set_defaults(func=cmd_backup_protect)

    p = sub.add_parser("tickets", help="Support tickets")
    p.add_argument("subcommand", choices=["list", "get", "create", "reply", "close", "departments"])
    p.add_argument("--ticket-id", type=int)
    p.add_argument("--subject")
    p.add_argument("--body")
    p.add_argument("--body-file", help="Read body from file")
    p.add_argument("--department", type=int)
    p.add_argument("--priority", default="medium")
    p.add_argument("--service-id", type=int)
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_tickets)

    p = sub.add_parser("balance", help="Account balance")
    p.set_defaults(func=cmd_balance)

    p = sub.add_parser("invoices", help="List or get invoices")
    p.add_argument("invoice_id", type=int, nargs="?", default=None)
    p.set_defaults(func=cmd_invoices)

    p = sub.add_parser("transactions", help="List transactions")
    p.set_defaults(func=cmd_transactions)

    p = sub.add_parser("activity", help="Account activity log, or VM activity with service_id")
    p.add_argument("service_id", type=int, nargs="?", default=None)
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_activity)

    p = sub.add_parser("emails", help="Email/notice history")
    p.set_defaults(func=cmd_emails)

    p = sub.add_parser("account", help="Account profile")
    p.set_defaults(func=cmd_account)

    p = sub.add_parser("firewall", help="VM firewall management")
    p.add_argument("service_id", type=int)
    p.add_argument("subcommand", choices=["show", "policy", "add-rule", "del-rule"])
    p.add_argument("--policy", choices=["ACCEPT", "DROP"])
    p.add_argument("--action", choices=["accept", "drop", "reject"])
    p.add_argument("--protocol", choices=["tcp", "udp", "icmp"])
    p.add_argument("--port")
    p.add_argument("--src")
    p.add_argument("--position", type=int)
    p.set_defaults(func=cmd_firewall)

    p = sub.add_parser("nodns", help="Provision DNS via nodns.shop")
    p.add_argument("--ip", required=True)
    p.add_argument("--nsec")
    p.add_argument("--subdomain")
    p.add_argument("--wait", type=int, default=15)
    p.add_argument("--verify", action="store_true")
    p.set_defaults(func=cmd_nodns)

    p = sub.add_parser("dns-verify", help="Verify DNS resolution")
    p.add_argument("fqdn")
    p.add_argument("--type", default="A")
    p.add_argument("--nameserver", default="ns1.nodns.shop")
    p.set_defaults(func=cmd_dns_verify)

    p = sub.add_parser("network", help="VM network details")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_network)

    p = sub.add_parser("payments", help="VM payment history")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_payments)

    p = sub.add_parser("upgrade-options", help="List upgrade options for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_upgrade_options)

    p = sub.add_parser("upgrade-preview", help="Preview a VM upgrade")
    p.add_argument("service_id", type=int)
    p.add_argument("--package-id", type=int, required=True)
    p.set_defaults(func=cmd_upgrade_preview)

    p = sub.add_parser("upgrade", help="Upgrade a VM")
    p.add_argument("service_id", type=int)
    p.add_argument("--package-id", type=int, required=True)
    p.set_defaults(func=cmd_upgrade)

    p = sub.add_parser("jobs", help="List jobs for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_jobs)

    p = sub.add_parser("job", help="Get a specific job")
    p.add_argument("service_id", type=int)
    p.add_argument("job_id")
    p.set_defaults(func=cmd_job)

    p = sub.add_parser("ssh-keys", help="List SSH keys for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_ssh_keys)

    p = sub.add_parser("ssh-key-add", help="Add an SSH key to a VM")
    p.add_argument("service_id", type=int)
    p.add_argument("--key", required=True, help="Public key string or path to pubkey file")
    p.add_argument("--label")
    p.set_defaults(func=cmd_ssh_key_add)

    p = sub.add_parser("ssh-key-live", help="Apply an SSH key to a running VM")
    p.add_argument("service_id", type=int)
    p.add_argument("--key", required=True, help="Public key string")
    p.set_defaults(func=cmd_ssh_key_live)

    p = sub.add_parser("iso", help="List ISOs for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_iso)

    p = sub.add_parser("iso-mount", help="Mount an ISO on a VM")
    p.add_argument("service_id", type=int)
    p.add_argument("iso_id")
    p.set_defaults(func=cmd_iso_mount)

    p = sub.add_parser("iso-unmount", help="Unmount ISO from a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_iso_unmount)

    p = sub.add_parser("rdns", help="List reverse DNS records for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_rdns)

    p = sub.add_parser("rdns-set", help="Set reverse DNS for an IP")
    p.add_argument("service_id", type=int)
    p.add_argument("--ip", required=True)
    p.add_argument("--ptr", required=True, help="PTR hostname")
    p.set_defaults(func=cmd_rdns_set)

    p = sub.add_parser("rdns-clear", help="Clear reverse DNS for an IP")
    p.add_argument("service_id", type=int)
    p.add_argument("--ip", required=True)
    p.set_defaults(func=cmd_rdns_clear)

    p = sub.add_parser("console", help="Console availability for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_console)

    p = sub.add_parser("console-session", help="Create a console session for a VM")
    p.add_argument("service_id", type=int)
    p.set_defaults(func=cmd_console_session)

    p = sub.add_parser("templates", help="List OS templates")
    p.set_defaults(func=cmd_templates)

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
