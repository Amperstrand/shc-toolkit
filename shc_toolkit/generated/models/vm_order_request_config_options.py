from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmOrderRequestConfigOptions")


@_attrs_define
class VmOrderRequestConfigOptions:
    """Optional package configurable options / add-ons to apply to the order, as a map of package-option ID (a positive
    integer, sent as the string key) to the selected value. The available option IDs, labels, and allowed values for
    each plan are listed under `config_options` in GET /ordering/catalog. Example: selecting the +1 TB disk add-on whose
    option ID is 15 → {"15": "1024"}. Omit to take the plan defaults. The Operating System and Desktop Environment are
    themselves configurable options: the `template` option (label "Operating System") selects the OS image (e.g.
    debian13-cloud, debian12-cloud, ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud,
    almalinux9-cloud, alpine323-cloud, devuan5-cloud, openbsd79-cloud, windows2022-byol), and the `gui_choice` option
    (label "Desktop Environment", AlmaLinux 9) selects an optional desktop (none, gnome, kde, xfce, cinnamon, mate).
    Their option IDs and allowed values are listed under `config_options` in GET /ordering/catalog. IMPORTANT: a VM
    order requires a resolved operating-system template. If the selected package does not define a default OS template,
    you MUST include the `template` option in config_options (use the option ID and an allowed value from GET
    /ordering/catalog); otherwise the order is rejected at submission with 400 error code `template_required` (no
    pending service/invoice is created). If the package defines a default OS template, `template` is optional and the
    default is used.

        Example:
            {'15': '1024'}

    """

    additional_properties: dict[str, bool | float | str] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vm_order_request_config_options = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> bool | float | str:
                return cast(bool | float | str, data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_order_request_config_options.additional_properties = additional_properties
        return vm_order_request_config_options

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> bool | float | str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: bool | float | str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
