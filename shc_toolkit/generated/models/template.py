from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Template")


@_attrs_define
class Template:
    """Reinstallable operating system image exposed for the customer's eligible VM scope.

    Example:
        {'name': 'debian13-cloud', 'display_name': 'Debian 13 Cloud', 'default_user': 'debian', 'cloudinit': True}

    Attributes:
        name (str): Machine-stable template identifier used for reinstall requests and returned by GET /image and GET
            /vm/templates. Examples (current live /ordering/catalog set): debian13-cloud, debian12-cloud, ubuntu2404-cloud,
            ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud, alpine323-cloud, devuan5-cloud,
            openbsd79-cloud, windows2022-byol. Example: debian13-cloud.
        display_name (str): Human-readable template label suitable for UI display. Example: Debian 13 Cloud.
        default_user (str): Default login user typically provided by the image. Example: debian.
        cloudinit (bool): Whether the template is intended for cloud-init style provisioning. Example: True.
    """

    name: str
    display_name: str
    default_user: str
    cloudinit: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        display_name = self.display_name

        default_user = self.default_user

        cloudinit = self.cloudinit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "display_name": display_name,
                "default_user": default_user,
                "cloudinit": cloudinit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        display_name = d.pop("display_name")

        default_user = d.pop("default_user")

        cloudinit = d.pop("cloudinit")

        template = cls(
            name=name,
            display_name=display_name,
            default_user=default_user,
            cloudinit=cloudinit,
        )

        template.additional_properties = d
        return template

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
