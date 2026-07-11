from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_ssh_key_delete_live_response import VmSshKeyDeleteLiveResponse


T = TypeVar("T", bound="DeleteLiveServiceSshKeyResponse200")


@_attrs_define
class DeleteLiveServiceSshKeyResponse200:
    """
    Attributes:
        data (VmSshKeyDeleteLiveResponse): Result of a live SSH-key removal. Idempotent: `removed` is false when the
            fingerprint was not present.
    """

    data: VmSshKeyDeleteLiveResponse
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
        from ..models.vm_ssh_key_delete_live_response import VmSshKeyDeleteLiveResponse

        d = dict(src_dict)
        data = VmSshKeyDeleteLiveResponse.from_dict(d.pop("data"))

        delete_live_service_ssh_key_response_200 = cls(
            data=data,
        )

        delete_live_service_ssh_key_response_200.additional_properties = d
        return delete_live_service_ssh_key_response_200

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
