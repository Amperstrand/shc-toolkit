from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmOrderProvisioningPreview")


@_attrs_define
class VmOrderProvisioningPreview:
    """
    Attributes:
        hostname (str):  Example: demo1.example.net.
        user (str):  Example: debian.
        template (None | str):  Example: debian13-cloud.
        supports_ssh_key (bool):  Example: True.
        supports_user_override (bool):  Example: True.
        module_group_id (int | None):  Example: 4.
    """

    hostname: str
    user: str
    template: None | str
    supports_ssh_key: bool
    supports_user_override: bool
    module_group_id: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hostname = self.hostname

        user = self.user

        template: None | str
        template = self.template

        supports_ssh_key = self.supports_ssh_key

        supports_user_override = self.supports_user_override

        module_group_id: int | None
        module_group_id = self.module_group_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hostname": hostname,
                "user": user,
                "template": template,
                "supports_ssh_key": supports_ssh_key,
                "supports_user_override": supports_user_override,
                "module_group_id": module_group_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hostname = d.pop("hostname")

        user = d.pop("user")

        def _parse_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        template = _parse_template(d.pop("template"))

        supports_ssh_key = d.pop("supports_ssh_key")

        supports_user_override = d.pop("supports_user_override")

        def _parse_module_group_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        module_group_id = _parse_module_group_id(d.pop("module_group_id"))

        vm_order_provisioning_preview = cls(
            hostname=hostname,
            user=user,
            template=template,
            supports_ssh_key=supports_ssh_key,
            supports_user_override=supports_user_override,
            module_group_id=module_group_id,
        )

        vm_order_provisioning_preview.additional_properties = d
        return vm_order_provisioning_preview

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
