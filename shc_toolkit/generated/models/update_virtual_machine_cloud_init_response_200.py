from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_init_apply_result import CloudInitApplyResult


T = TypeVar("T", bound="UpdateVirtualMachineCloudInitResponse200")


@_attrs_define
class UpdateVirtualMachineCloudInitResponse200:
    """
    Attributes:
        data (CloudInitApplyResult):
    """

    data: CloudInitApplyResult

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
        from ..models.cloud_init_apply_result import CloudInitApplyResult

        d = dict(src_dict)
        data = CloudInitApplyResult.from_dict(d.pop("data"))

        update_virtual_machine_cloud_init_response_200 = cls(
            data=data,
        )

        return update_virtual_machine_cloud_init_response_200
