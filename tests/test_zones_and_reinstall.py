"""Zone/facility visibility + reap-tag idempotency + reinstall kwarg pin.

Earned 2026-09-01 (lightning-playground #96 fuzz campaign): the ssd/dev
catalog lines land in the Cherryvale, Kansas facility, which was
unreachable from the EU lab route — two fresh orders died with port 22
closed and the bootstrap signal unfired while the diagnosis blamed
cloud-init. The facility map, the order-time warning, and the stock
output exist so nobody re-derives that by burning another order.
"""

from unittest.mock import patch

import pytest

from shc_toolkit.cli import apply_reap_tag, cmd_order, cmd_reinstall
from shc_toolkit.client import SHCClient
from shc_toolkit.sizes import FACILITIES, SIZE_MAP


class TestFacilities:
    def test_every_line_has_a_facility(self):
        lines = {e["line"] for e in SIZE_MAP.values()}
        assert lines == set(FACILITIES), "unmapped catalog line — extend FACILITIES"

    def test_size_map_entries_carry_facility_fields(self):
        for entry in SIZE_MAP.values():
            assert entry["module_group_id"] == FACILITIES[entry["line"]]["module_group_id"]
            assert entry["facility"] == FACILITIES[entry["line"]]["facility"]

    def test_cherryvale_lines_are_flagged_unreachable(self):
        # The trap itself: ssd/dev live in Cherryvale, nvme/hdd in Katy.
        assert FACILITIES["ssd"]["module_group_id"] == 7
        assert FACILITIES["dev"]["module_group_id"] == 7
        for line in ("ssd", "dev"):
            assert FACILITIES[line]["reachability"].startswith("unreachable")
        for line in ("nvme", "hdd"):
            assert FACILITIES[line]["reachability"] == "ok"
            assert FACILITIES[line]["module_group_id"] in (4, 8)


class TestApplyReapTag:
    def test_appends_when_absent(self):
        assert apply_reap_tag("tg-x", "8h") == ("tg-x-reap8h", True)
        assert apply_reap_tag("tg-x", "90m") == ("tg-x-reap90m", True)

    def test_no_double_tag(self):
        # The 2026-09-01 burn: x-reap8h + --reap 8h → x-reap8h-reap8h
        assert apply_reap_tag("tg-x-reap8h", "8h") == ("tg-x-reap8h", False)

    def test_existing_other_tag_wins(self):
        # An existing tag (any value) is authoritative — never stack a second
        assert apply_reap_tag("tg-x-reap48h", "2h") == ("tg-x-reap48h", False)

    def test_no_reap_is_noop(self):
        assert apply_reap_tag("tg-x", None) == ("tg-x", False)

    def test_epoch_tag_not_stacked(self):
        assert apply_reap_tag("tg-x-reap1788280215", "1h") == ("tg-x-reap1788280215", False)

    def test_bad_tag_raises(self):
        with pytest.raises(ValueError):
            apply_reap_tag("tg-x", "nonsense")


class TestReinstallKwarg:
    def test_template_travels_as_kwarg(self):
        # 2026-09-01: cmd_reinstall passed the template POSITIONALLY and
        # reinstall_vm is keyword-only — every `shc reinstall` was a
        # TypeError. This pin fails if the call shape regresses.
        with patch.object(SHCClient, "reinstall_vm", return_value={"ok": True}) as m:
            cmd_reinstall(_ns())
        m.assert_called_once_with(2345, template="debian13-cloud")

    def test_stop_first_conflict_is_actionable(self):
        from shc_toolkit.client import SHCError

        with patch.object(
            SHCClient,
            "reinstall_vm",
            side_effect=SHCError("conflict", "VM must be stopped before reinstall"),
        ):
            with pytest.raises(SystemExit):
                cmd_reinstall(_ns())


class _Args:
    """Minimal argparse namespace for cmd_reinstall (network-free)."""

    service_id = 2345
    template = None
    api_key = "test-key"
    context = None
    format = "json"


def _ns():
    return _Args()


def _order_ns(**over):
    """argparse.Namespace for cmd_order (network-free via _client stub)."""
    import argparse

    defaults = dict(
        hostname="tg-test",
        reap=None,
        ssh_key=None,
        size=None,
        cpu=None,
        ram=None,
        disk=None,
        package_id=None,
        pricing_id=None,
        module_group_id=None,
        tag=None,
        template=None,
        dry_run=False,
        pay=False,
        pay_qr=False,
        idempotency_key=None,
        allow_unstable_zone=False,
        api_key="test-key",
        context=None,
        format="json",
    )
    defaults.update(over)
    return argparse.Namespace(**defaults)


class TestUnstableFacilityRefusal:
    """`shc order` must FAIL EARLY into a flagged facility (2026-09-04).

    A stderr warning was not enough: an order into the flagged Cherryvale
    facility goes billing-active and then never attaches to the network
    (issue #39, live-FAIL again 2026-09-04) — waiting 300s cannot help.
    Default = refuse before spending; --dry-run and --allow-unstable-zone
    are the debugging paths.
    """

    def _client_stub(self, monkeypatch):
        from unittest.mock import MagicMock

        import shc_toolkit.cli as cli

        client = MagicMock()
        client.get_config_options.return_value = {}
        client.preview_order.return_value = {"preview": True}
        client.submit_order.return_value = {"service_ids": [1]}
        monkeypatch.setattr(cli, "_client", lambda args: client)
        return client

    def test_dev_size_refused_by_default(self, monkeypatch, capsys):
        client = self._client_stub(monkeypatch)
        with pytest.raises(SystemExit) as excinfo:
            cmd_order(_order_ns(size="dev-1c-4gb"))
        assert excinfo.value.code == 1
        err = capsys.readouterr().err
        assert "--allow-unstable-zone" in err, "refusal must name the opt-in"
        assert "Cherryvale" in err
        client.submit_order.assert_not_called()
        client.preview_order.assert_not_called()

    def test_dev_size_allowed_with_opt_in(self, monkeypatch):
        client = self._client_stub(monkeypatch)
        cmd_order(_order_ns(size="dev-1c-4gb", allow_unstable_zone=True))
        client.submit_order.assert_called_once()

    def test_dry_run_warns_but_previews(self, monkeypatch, capsys):
        client = self._client_stub(monkeypatch)
        cmd_order(_order_ns(size="dev-1c-4gb", dry_run=True))
        client.preview_order.assert_called_once()
        err = capsys.readouterr().err
        assert "flagged" in err, "dry-run keeps the warning"

    def test_nvme_size_never_refused(self, monkeypatch):
        client = self._client_stub(monkeypatch)
        cmd_order(_order_ns(size="nvme-2c-8gb"))
        client.submit_order.assert_called_once()

    def test_refusal_helper_gates_on_allow_and_dry_run(self):
        from shc_toolkit.sizes import unstable_order_refusal

        dev_pkg = next(
            e["package_id"] for e in SIZE_MAP.values() if e["line"] == "dev"
        )
        nvme_pkg = next(
            e["package_id"] for e in SIZE_MAP.values() if e["line"] == "nvme"
        )
        assert unstable_order_refusal(dev_pkg, allow=False) is not None
        assert "--allow-unstable-zone" in unstable_order_refusal(dev_pkg, allow=False)
        assert unstable_order_refusal(dev_pkg, allow=True) is None
        assert unstable_order_refusal(dev_pkg, allow=False, dry_run=True) is None
        assert unstable_order_refusal(nvme_pkg, allow=False) is None

    def test_unknown_package_has_no_refusal(self):
        from shc_toolkit.sizes import unstable_order_refusal

        assert unstable_order_refusal(999999, allow=False) is None

    def test_flagged_entries_carry_issue_reference(self):
        for line in ("ssd", "dev"):
            assert FACILITIES[line].get("issue"), f"{line} must reference its issue"
