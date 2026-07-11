from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_upgrade_preview_response import VmUpgradePreviewResponse


T = TypeVar("T", bound="PreviewServiceUpgradeResponse200")


@_attrs_define
class PreviewServiceUpgradeResponse200:
    """
    Attributes:
        data (VmUpgradePreviewResponse): Prorated quote (no charge). amount_due_now already includes any setup fee.
            applies is always "queued" (the change is created queued, awaiting payment).
    """

    data: VmUpgradePreviewResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgrade_preview_response import VmUpgradePreviewResponse

        d = dict(src_dict)
        data = VmUpgradePreviewResponse.from_dict(d.pop("data"))

        preview_service_upgrade_response_200 = cls(
            data=data,
        )

        preview_service_upgrade_response_200.additional_properties = d
        return preview_service_upgrade_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
