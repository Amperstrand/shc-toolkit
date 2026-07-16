from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DeleteVirtualMachineCloudInitBody")


@_attrs_define
class DeleteVirtualMachineCloudInitBody:
    """ """

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        delete_virtual_machine_cloud_init_body = cls()

        return delete_virtual_machine_cloud_init_body
