from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="VmPciSummaryPrimaryType0")


@_attrs_define
class VmPciSummaryPrimaryType0:
    """
    Attributes:
        short (str):  Example: B50.
        label (str):  Example: Intel Arc Pro B50 GPU.
    """

    short: str
    label: str

    def to_dict(self) -> dict[str, Any]:
        short = self.short

        label = self.label

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "short": short,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        short = d.pop("short")

        label = d.pop("label")

        vm_pci_summary_primary_type_0 = cls(
            short=short,
            label=label,
        )

        return vm_pci_summary_primary_type_0
