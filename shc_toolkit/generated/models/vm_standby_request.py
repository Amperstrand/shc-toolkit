from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmStandbyRequest")


@_attrs_define
class VmStandbyRequest:
    """
    Attributes:
        keep_ip (bool | Unset): When true, keep the currently assigned IP through standby. Default false releases the IP
            while parked. Default: False.
    """

    keep_ip: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        keep_ip = self.keep_ip

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if keep_ip is not UNSET:
            field_dict["keep_ip"] = keep_ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keep_ip = d.pop("keep_ip", UNSET)

        vm_standby_request = cls(
            keep_ip=keep_ip,
        )

        return vm_standby_request
