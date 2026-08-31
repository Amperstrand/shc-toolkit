"""Reap billing-semantics tests: stopped-but-billable zombies get reaped.

SHC bills by service existence — a stopped VM accrues its full daily price
until cancelled (clboss-soak incident, 2026-08-26: VM shut down after a
drain contract, left billing ~13h until owner-caught). These tests pin
that reap catches that class even for non-test hostnames, while never
cancelling running non-test VMs or protected hostnames.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from shc_toolkit.client import SHCClient

OLD = (datetime.now(UTC) - timedelta(hours=5)).isoformat()
YOUNG = (datetime.now(UTC) - timedelta(minutes=10)).isoformat()


def _vm(vm_id, hostname, created=OLD, status="active"):
    return {
        "id": vm_id,
        "hostname": hostname,
        "service_status": status,
        "date_created": created,
        "package": "starter",
    }


def _stopped_runtime():
    return {"runtime": {"raw_status": "stopped"}}


def _running_runtime():
    return {"runtime": {"raw_status": "running"}}


class TestStoppedButBillable:
    def test_reaps_stopped_non_test_vm(self):
        """The zombie class: stopped, old, prefix-less hostname → cancelled."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(
                SHCClient, "list_vms", return_value=[_vm(1, "billing-zombie")]
            ),
            patch.object(SHCClient, "get_vm_summary", return_value=_stopped_runtime()),
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert [o["hostname"] for o in orphans] == ["billing-zombie"]
        assert orphans[0]["reason"] == "stopped-but-billable"
        cancel.assert_called_once_with(1, immediate=True)

    def test_spares_running_non_test_vm(self):
        """Old but RUNNING non-test VMs are not reap's business."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(
                SHCClient, "list_vms", return_value=[_vm(3, "production-server")]
            ),
            patch.object(SHCClient, "get_vm_summary", return_value=_running_runtime()),
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert orphans == []
        cancel.assert_not_called()

    def test_spares_young_stopped_vm(self):
        """A recently stopped VM may still be mid-workflow (or draining)."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(
                SHCClient,
                "list_vms",
                return_value=[_vm(1, "clboss-soak", created=YOUNG)],
            ),
            patch.object(
                SHCClient, "get_vm_summary", return_value=_stopped_runtime()
            ) as summary,
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert orphans == []
        summary.assert_not_called()
        cancel.assert_not_called()

    def test_excluded_hostname_survives_even_stopped(self):
        c = SHCClient(api_key="test-key")
        with (
            patch.object(
                SHCClient, "list_vms", return_value=[_vm(1, "europa-vpn-vps")]
            ),
            patch.object(
                SHCClient, "get_vm_summary", return_value=_stopped_runtime()
            ) as summary,
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert orphans == []
        summary.assert_not_called()
        cancel.assert_not_called()

    def test_keep_pattern_survives_even_stopped(self):
        c = SHCClient(api_key="test-key")
        with (
            patch.object(
                SHCClient, "list_vms", return_value=[_vm(1, "tollgate-main-node-1")]
            ),
            patch.object(
                SHCClient, "get_vm_summary", return_value=_stopped_runtime()
            ) as summary,
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert orphans == []
        summary.assert_not_called()
        cancel.assert_not_called()

    def test_probe_failure_never_cancels(self):
        """Fail-open: an uninspectable VM is skipped, not cancelled."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(SHCClient, "list_vms", return_value=[_vm(1, "mystery-box")]),
            patch.object(
                SHCClient,
                "get_vm_summary",
                side_effect=RuntimeError("summary unavailable"),
            ),
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert orphans == []
        cancel.assert_not_called()

    def test_shutdown_dialect_also_reaped(self):
        """Some hypervisors report 'shutdown' rather than 'stopped'."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(SHCClient, "list_vms", return_value=[_vm(7, "some-lab-box")]),
            patch.object(
                SHCClient,
                "get_vm_summary",
                return_value={"runtime": {"state": "shutdown"}},
            ),
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=False)
        assert [o["reason"] for o in orphans] == ["stopped-but-billable"]
        cancel.assert_called_once_with(7, immediate=True)


class TestPrefixesAndReasons:
    def test_test_pattern_vm_gets_reason_field(self):
        c = SHCClient(api_key="test-key")
        with (
            patch.object(SHCClient, "list_vms", return_value=[_vm(2, "ci-runner-9")]),
            patch.object(SHCClient, "cancel_vm"),
        ):
            orphans = c.reap_orphans(dry_run=True)
        assert orphans[0]["reason"] == "test-pattern"

    def test_clboss_prefix_now_matches(self):
        """'clboss-' added to defaults: a forgotten RUNNING lab VM is reaped too."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(SHCClient, "list_vms", return_value=[_vm(4, "clboss-soak-2")]),
            patch.object(SHCClient, "get_vm_summary") as summary,
            patch.object(SHCClient, "cancel_vm"),
        ):
            orphans = c.reap_orphans(dry_run=True)
        assert [o["reason"] for o in orphans] == ["test-pattern"]
        summary.assert_not_called()
