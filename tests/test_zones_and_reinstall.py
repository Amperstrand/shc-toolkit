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

from shc_toolkit.cli import apply_reap_tag, cmd_reinstall
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
