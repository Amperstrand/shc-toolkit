from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetVirtualMachineReverseDnsResponse200DataRecordsItem")


@_attrs_define
class GetVirtualMachineReverseDnsResponse200DataRecordsItem:
    """
    Attributes:
        ip (str | Unset):
        ptr (None | str | Unset): Live PTR (null if none set).
        pending (None | str | Unset): Queued-but-not-yet-live PTR, else null.
        zone (str | Unset):  Example: 128.182.23.in-addr.arpa.
        pending_public (bool | Unset): True when the reverse block is authoritative on SHC nameservers but not yet
            publicly delegated (e.g. Kansas 204.92.66).
    """

    ip: str | Unset = UNSET
    ptr: None | str | Unset = UNSET
    pending: None | str | Unset = UNSET
    zone: str | Unset = UNSET
    pending_public: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip = self.ip

        ptr: None | str | Unset
        if isinstance(self.ptr, Unset):
            ptr = UNSET
        else:
            ptr = self.ptr

        pending: None | str | Unset
        if isinstance(self.pending, Unset):
            pending = UNSET
        else:
            pending = self.pending

        zone = self.zone

        pending_public = self.pending_public

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ip is not UNSET:
            field_dict["ip"] = ip
        if ptr is not UNSET:
            field_dict["ptr"] = ptr
        if pending is not UNSET:
            field_dict["pending"] = pending
        if zone is not UNSET:
            field_dict["zone"] = zone
        if pending_public is not UNSET:
            field_dict["pending_public"] = pending_public

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ip = d.pop("ip", UNSET)

        def _parse_ptr(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ptr = _parse_ptr(d.pop("ptr", UNSET))

        def _parse_pending(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pending = _parse_pending(d.pop("pending", UNSET))

        zone = d.pop("zone", UNSET)

        pending_public = d.pop("pending_public", UNSET)

        get_virtual_machine_reverse_dns_response_200_data_records_item = cls(
            ip=ip,
            ptr=ptr,
            pending=pending,
            zone=zone,
            pending_public=pending_public,
        )

        get_virtual_machine_reverse_dns_response_200_data_records_item.additional_properties = d
        return get_virtual_machine_reverse_dns_response_200_data_records_item

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
