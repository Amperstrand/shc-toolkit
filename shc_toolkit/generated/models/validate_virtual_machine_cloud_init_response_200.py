from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.cloud_init_validate_result import CloudInitValidateResult


T = TypeVar("T", bound="ValidateVirtualMachineCloudInitResponse200")


@_attrs_define
class ValidateVirtualMachineCloudInitResponse200:
    data: CloudInitValidateResult

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.cloud_init_validate_result import CloudInitValidateResult

        d = dict(src_dict)
        data = CloudInitValidateResult.from_dict(d.pop("data"))

        validate_virtual_machine_cloud_init_response_200 = cls(
            data=data,
        )

        return validate_virtual_machine_cloud_init_response_200
