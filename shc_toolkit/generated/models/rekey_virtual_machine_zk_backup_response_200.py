from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cancel_vm_response_data import CancelVmResponseData


T = TypeVar("T", bound="RekeyVirtualMachineZkBackupResponse200")


@_attrs_define
class RekeyVirtualMachineZkBackupResponse200:
    """
    Attributes:
        data (CancelVmResponseData): VmDetail extended with `cancel_credit` when the cancel was immediate. End-of-term
            cancels return the bare VmDetail shape (no `cancel_credit`). v2.4.0: top-level expected_refund + transaction_id
            mirrors are always present on cancel responses.
    """

    data: CancelVmResponseData
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
        from ..models.cancel_vm_response_data import CancelVmResponseData

        d = dict(src_dict)
        data = CancelVmResponseData.from_dict(d.pop("data"))

        rekey_virtual_machine_zk_backup_response_200 = cls(
            data=data,
        )

        rekey_virtual_machine_zk_backup_response_200.additional_properties = d
        return rekey_virtual_machine_zk_backup_response_200

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
