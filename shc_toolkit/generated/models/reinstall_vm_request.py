from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReinstallVmRequest")


@_attrs_define
class ReinstallVmRequest:
    """
    Example:
        {'template': 'debian13-cloud'}

    Attributes:
        template (str): Machine-stable OS template identifier to reinstall onto the VM. Must be one the customer's plan
            offers in the live /ordering/catalog `template` option (e.g. debian13-cloud, debian12-cloud, ubuntu2404-cloud,
            ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud, alpine323-cloud, devuan5-cloud,
            openbsd79-cloud, windows2022-byol). Example: debian13-cloud.
    """

    template: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        template = self.template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "template": template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        template = d.pop("template")

        reinstall_vm_request = cls(
            template=template,
        )

        reinstall_vm_request.additional_properties = d
        return reinstall_vm_request

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
