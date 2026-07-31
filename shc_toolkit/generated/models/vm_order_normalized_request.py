from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="VmOrderNormalizedRequest")


@_attrs_define
class VmOrderNormalizedRequest:
    package_id: int
    pricing_id: int
    hostname: str
    user: str
    ssh_key_present: bool
    module_group_id: int | None
    order_form_id: int
    package_group_id: int
    coupon_present: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        package_id = self.package_id

        pricing_id = self.pricing_id

        hostname = self.hostname

        user = self.user

        ssh_key_present = self.ssh_key_present

        module_group_id: int | None
        module_group_id = self.module_group_id

        order_form_id = self.order_form_id

        package_group_id = self.package_group_id

        coupon_present = self.coupon_present

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "package_id": package_id,
                "pricing_id": pricing_id,
                "hostname": hostname,
                "user": user,
                "ssh_key_present": ssh_key_present,
                "module_group_id": module_group_id,
                "order_form_id": order_form_id,
                "package_group_id": package_group_id,
                "coupon_present": coupon_present,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        package_id = d.pop("package_id")

        pricing_id = d.pop("pricing_id")

        hostname = d.pop("hostname")

        user = d.pop("user")

        ssh_key_present = d.pop("ssh_key_present")

        def _parse_module_group_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        module_group_id = _parse_module_group_id(d.pop("module_group_id"))

        order_form_id = d.pop("order_form_id")

        package_group_id = d.pop("package_group_id")

        coupon_present = d.pop("coupon_present")

        vm_order_normalized_request = cls(
            package_id=package_id,
            pricing_id=pricing_id,
            hostname=hostname,
            user=user,
            ssh_key_present=ssh_key_present,
            module_group_id=module_group_id,
            order_form_id=order_form_id,
            package_group_id=package_group_id,
            coupon_present=coupon_present,
        )

        vm_order_normalized_request.additional_properties = d
        return vm_order_normalized_request

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
