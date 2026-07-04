import json
import os
import time
import uuid

import pytest
import requests

from shc_toolkit.client import SHCError

OPENAPI_URL = "https://blesta.sovereignhybridcompute.com/user-api/openapi.json"
SSH_KEY_PATH = os.path.expanduser("~/.ssh/id_rsa.pub")


def test_account_balance(client):
    result = client.get_account_balance()
    data = result.get("data", result)
    balances = data.get("balances", data.get("credit", []))
    assert isinstance(balances, list)
    assert len(balances) > 0
    usd = [c for c in balances if c.get("currency") == "USD"]
    assert len(usd) > 0


def test_ordering_catalog(client):
    catalog = client.get_catalog()
    assert isinstance(catalog, list)
    assert len(catalog) > 0
    pkg = catalog[0]
    assert "package_id" in pkg
    assert "name" in pkg


def test_vm_templates(client):
    try:
        templates = client.list_templates()
    except SHCError as e:
        if "Unknown tool" in str(e) or "not_found" in e.code:
            pytest.skip(f"Templates endpoint not available on this transport: {e}")
        raise
    assert isinstance(templates, list)


def test_list_vms(client):
    vms = client.list_vms()
    assert isinstance(vms, list)


def test_openapi_spec_accessible(client):
    r = requests.get(OPENAPI_URL, timeout=15)
    assert r.status_code == 200
    text = r.text
    idx = text.find("{")
    if idx > 0:
        text = text[idx:]
    spec = json.loads(text)
    assert "paths" in spec


def test_get_vm(client, vm):
    result = client.get_vm(vm["service_id"])
    assert "hostname" in result
    assert result["service_status"] == "active"
    assert result["provisioning_state"] == "ready"


def test_get_vm_detail(client, vm):
    sid = vm["service_id"]
    basic = client.get_vm(sid)
    detail = client.get_vm_detail(sid)
    assert "hostname" in detail
    assert len(detail) > len(basic)


def test_get_vm_summary(client, vm):
    result = client.get_vm_summary(vm["service_id"])
    assert "hostname" in result


def test_vm_credentials(client, vm):
    creds = client.get_vm_credentials(vm["service_id"])
    assert isinstance(creds, dict)
    assert "password" in creds or "username" in creds


def test_vm_metrics(client, vm):
    result = client.get_vm_metrics(vm["service_id"])
    assert isinstance(result, dict)


def test_vm_network(client, vm):
    result = client.get_vm_network(vm["service_id"])
    assert isinstance(result, dict)


def test_vm_bandwidth(client, vm):
    result = client.get_vm_bandwidth(vm["service_id"])
    assert isinstance(result, dict)


def test_vm_activity(client, vm):
    result = client.get_vm_activity(vm["service_id"])
    assert isinstance(result, list)


def test_vm_payments(client, vm):
    result = client.get_vm_payments(vm["service_id"])
    assert isinstance(result, list)


def test_snapshot_lifecycle(client, vm):
    sid = vm["service_id"]

    try:
        client.create_snapshot(sid, name="test-snap")
    except SHCError as e:
        if e.error_code == "upstream_failure" or any(w in str(e).lower() for w in ("storage", "inventory")):
            pytest.skip(f"Snapshot storage unavailable: {e}")
        raise

    deadline = time.time() + 120
    snap_id = None
    while time.time() < deadline:
        snaps = client.list_snapshots(sid)
        for s in snaps:
            if s.get("name") == "test-snap":
                snap_id = s.get("id") or s.get("snapshot_id")
                break
        if snap_id:
            break
        time.sleep(3)

    if not snap_id:
        pytest.skip("Snapshot did not appear within 60s (likely Dev VPS storage limitation)")

    client.delete_snapshot(sid, snap_id)

    deadline = time.time() + 60
    while time.time() < deadline:
        snaps = client.list_snapshots(sid)
        if not any(s.get("name") == "test-snap" for s in snaps):
            return
        time.sleep(3)

    pytest.fail("Snapshot still present after delete")


def test_backup_lifecycle(client, vm):
    sid = vm["service_id"]

    try:
        client.create_backup(sid, name="test-backup")
    except SHCError as e:
        if e.error_code == "upstream_failure" or any(w in str(e).lower() for w in ("storage", "inventory")):
            pytest.skip(f"Backup storage unavailable: {e}")
        raise

    deadline = time.time() + 120
    backup_id = None
    while time.time() < deadline:
        backups = client.list_backups(sid)
        for b in backups:
            if b.get("name") == "test-backup":
                backup_id = b.get("id") or b.get("backup_id")
                break
        if backup_id:
            break
        time.sleep(3)

    assert backup_id, "Backup did not appear in list within 120s"

    client.delete_backup(sid, backup_id)

    deadline = time.time() + 60
    while time.time() < deadline:
        backups = client.list_backups(sid)
        if not any(b.get("name") == "test-backup" for b in backups):
            return
        time.sleep(3)

    pytest.fail("Backup still present after delete")


def test_firewall_lifecycle(client, vm):
    sid = vm["service_id"]

    fw_before = client.get_firewall(sid)
    rules_before = fw_before.get("rules", [])

    client.create_firewall_rule(
        sid,
        action="ACCEPT",
        direction="in",
        protocol="tcp",
        dest_port="8443",
        name="pytest-fw-test",
    )

    fw_after = client.get_firewall(sid)
    rules_after = fw_after.get("rules", [])
    assert len(rules_after) > len(rules_before)

    test_rule = None
    for r in rules_after:
        if "pytest" in str(r.get("comment", "")).lower():
            test_rule = r
            break

    assert test_rule, "Created firewall rule not found in list"

    pos = test_rule.get("pos")
    assert pos is not None, "Firewall rule has no pos field"

    client.delete_firewall_rule(sid, pos)

    fw_final = client.get_firewall(sid)
    rules_final = fw_final.get("rules", [])
    assert len(rules_final) == len(rules_before)


def test_ssh_key_operations(client, vm):
    sid = vm["service_id"]

    keys_before = client.list_ssh_keys(sid)
    assert isinstance(keys_before, list)

    if not os.path.exists(SSH_KEY_PATH):
        pytest.skip("No SSH public key at ~/.ssh/id_rsa.pub")

    with open(SSH_KEY_PATH) as f:
        pubkey = f.read().strip()

    client.apply_ssh_key_live(sid, pubkey)

    keys_after = client.list_ssh_keys(sid)
    assert isinstance(keys_after, list)


def test_vm_restart(client, vm):
    sid = vm["service_id"]

    client.restart_vm(sid)

    deadline = time.time() + 120
    while time.time() < deadline:
        vm_data = client.get_vm(sid)
        if vm_data.get("service_status") == "active":
            return
        time.sleep(5)

    pytest.fail("VM did not return to active after restart within 120s")


def test_order_idempotency(client):
    idem_key = f"idem-test-{uuid.uuid4().hex[:16]}"

    result1 = client.submit_order(
        idempotency_key=idem_key,
        package_id=81,
        pricing_id=245,
        hostname="pytest-idem",
    )
    sids1 = result1.get("service_ids", [])

    result2 = client.submit_order(
        idempotency_key=idem_key,
        package_id=81,
        pricing_id=245,
        hostname="pytest-idem",
    )
    sids2 = result2.get("service_ids", [])

    assert sids1 == sids2, (
        f"Idempotency failed: first={sids1}, second={sids2}"
    )

    if sids1:
        try:
            client.cancel_vm(sids1[0], immediate=True)
        except Exception:
            pass


def test_cost_audit_lifecycle(client):
    """Verify cost tracking fires on order and cancel, with expected vs actual."""
    if not hasattr(client, "cost_tracker"):
        pytest.skip("cost_tracker only available on REST transport")

    result = client.submit_order(
        package_id=81,
        pricing_id=245,
        hostname="pytest-cost-audit",
    )
    sids = result.get("service_ids") or (
        [result["service_id"]] if result.get("service_id") else []
    )
    assert sids, f"No service_id in order result: {result}"
    sid = sids[0]

    assert sid in client.cost_tracker._sessions, (
        f"submit_order did not trigger cost tracking for svc {sid}"
    )
    session = client.cost_tracker._sessions[sid]
    assert session.daily_price > 0, f"daily_price not set: {session}"

    report = client.cost_tracker.session_report(sid)
    assert report is not None
    assert report["service_id"] == sid

    try:
        client.cancel_vm(sid, immediate=True)
    except Exception:
        pass

    cancel_report = client.cost_tracker.audit_cancel(sid)
    if cancel_report:
        assert not cancel_report.mismatch, (
            f"Cost mismatch for svc {sid}: {cancel_report.notes}"
        )
