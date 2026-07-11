from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.vm_pci_summary_primary_type_0 import VmPciSummaryPrimaryType0


T = TypeVar("T", bound="VmPciSummary")


@_attrs_define
class VmPciSummary:
    """GPU/PCI passthrough summary card. Only the device count and a primary label/short are exposed; per-device topology
    (pci_id, vendor:device, IOMMU group) is intentionally withheld.

        Attributes:
            count (int):  Example: 1.
            primary (None | VmPciSummaryPrimaryType0): Null when no PCI devices are assigned.
    """

    count: int
    primary: None | VmPciSummaryPrimaryType0

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_pci_summary_primary_type_0 import VmPciSummaryPrimaryType0

        count = self.count

        primary: dict[str, Any] | None
        if isinstance(self.primary, VmPciSummaryPrimaryType0):
            primary = self.primary.to_dict()
        else:
            primary = self.primary

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "count": count,
                "primary": primary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_pci_summary_primary_type_0 import VmPciSummaryPrimaryType0

        d = dict(src_dict)
        count = d.pop("count")

        def _parse_primary(data: object) -> None | VmPciSummaryPrimaryType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                primary_type_0 = VmPciSummaryPrimaryType0.from_dict(data)

                return primary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | VmPciSummaryPrimaryType0, data)

        primary = _parse_primary(d.pop("primary"))

        vm_pci_summary = cls(
            count=count,
            primary=primary,
        )

        return vm_pci_summary
