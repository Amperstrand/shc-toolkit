from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_init_delete_result import CloudInitDeleteResult


T = TypeVar("T", bound="DeleteVirtualMachineCloudInitResponse200")


@_attrs_define
class DeleteVirtualMachineCloudInitResponse200:
    """
    Attributes:
        data (CloudInitDeleteResult):
    """

    data: CloudInitDeleteResult

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_init_delete_result import CloudInitDeleteResult

        d = dict(src_dict)
        data = CloudInitDeleteResult.from_dict(d.pop("data"))

        delete_virtual_machine_cloud_init_response_200 = cls(
            data=data,
        )

        return delete_virtual_machine_cloud_init_response_200
