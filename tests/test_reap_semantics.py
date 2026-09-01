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


class TestReapDeadlineTag:
    """'-reap<deadline>' hostname tags: spared until the deadline, reaped
    at it, overriding max-age in both directions and opting non-prefix
    hostnames in. Earned 2026-09-01: the overnight reaper ate a VM with
    hours of un-exfiltrated campaign results (lightning-playground
    LESSONS-2026-09-01-VM-PIVOT-SELF-REVIEW.md)."""

    def test_parses_relative_tag_from_creation(self):
        from shc_toolkit.client import parse_reap_deadline

        created = datetime.now(UTC) - timedelta(hours=1)
        deadline = parse_reap_deadline("tg-vls-reap6h", created)
        assert deadline is not None
        assert 4.9 < (deadline - datetime.now(UTC)).total_seconds() / 3600 < 5.1

    def test_parses_absolute_epoch_tag_without_creation(self):
        from shc_toolkit.client import parse_reap_deadline

        ep = int((datetime.now(UTC) + timedelta(hours=12)).timestamp())
        deadline = parse_reap_deadline(f"lab-box-reap{ep}", None)
        assert deadline is not None and deadline > datetime.now(UTC)

    def test_name_collision_is_not_a_tag(self):
        from shc_toolkit.client import parse_reap_deadline

        now = datetime.now(UTC)
        assert parse_reap_deadline("ci-runner-r2d2", now) is None
        assert parse_reap_deadline("tg-vls-reap6h-extra", now) is None
        assert parse_reap_deadline("tg-vls-reap6x", now) is None
        assert parse_reap_deadline("tg-vls-reap6", now) is None

    def test_spares_tagged_test_vm_past_max_age(self):
        """THE incident class: old test VM, deadline not yet reached → spared."""
        c = SHCClient(api_key="test-key")
        with (
            patch.object(
                SHCClient,
                "list_vms",
                return_value=[_vm(9, "tg-vls-splice-reap48h")],
            ),
            patch.object(SHCClient, "cancel_vm") as cancel,
        ):
            orphans = c.reap_orphans(dry_run=True)
        assert orphans == []
        cancel.assert_not_called()

    def test_reaps_tagged_vm_at_deadline_despite_young_age(self):
        """Past-deadline beats young age too (the override is bidirectional)."""
        c = SHCClient(api_key="test-key")
        past = (datetime.now(UTC) - timedelta(hours=3)).isoformat()
        with (
            patch.object(
                SHCClient,
                "list_vms",
                return_value=[_vm(10, "tg-batch-reap1h", created=past)],
            ),
            patch.object(SHCClient, "cancel_vm"),
        ):
            orphans = c.reap_orphans(dry_run=True)
        assert [o["reason"] for o in orphans] == ["reap-deadline"]

    def test_tag_opts_in_non_prefix_hostname(self):
        """A tagged VM with no test prefix is reapable at its deadline —
        the tag is an explicit self-declared ephemerality, running or not."""
        c = SHCClient(api_key="test-key")
        past = (datetime.now(UTC) - timedelta(hours=30)).isoformat()
        with (
            patch.object(
                SHCClient,
                "list_vms",
                return_value=[_vm(11, "vls-lab-reap1d", created=past)],
            ),
            patch.object(SHCClient, "get_vm_summary") as summary,
            patch.object(SHCClient, "cancel_vm"),
        ):
            orphans = c.reap_orphans(dry_run=True)
        assert [o["reason"] for o in orphans] == ["reap-deadline"]
        summary.assert_not_called()  # no runtime probe needed: explicit intent

    def test_absolute_past_epoch_reaps_immediately(self):
        from datetime import datetime as _dt

        c = SHCClient(api_key="test-key")
        long_past = str(int((_dt.now(UTC) - timedelta(days=1)).timestamp()))
        with (
            patch.object(
                SHCClient,
                "list_vms",
                return_value=[_vm(12, f"tg-oops-reap{long_past}")],
            ),
            patch.object(SHCClient, "cancel_vm"),
        ):
            orphans = c.reap_orphans(dry_run=True)
        assert [o["reason"] for o in orphans] == ["reap-deadline"]
