from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_order_request_additional_property_type_4 import (
        VmOrderRequestAdditionalPropertyType4,
    )
    from ..models.vm_order_request_config_options import VmOrderRequestConfigOptions


T = TypeVar("T", bound="VmOrderRequest")


@_attrs_define
class VmOrderRequest:
    """Order request for a new VM.

    Example:
        {'package_id': 23, 'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}

    Attributes:
        package_id (int):  Example: 23.
        pricing_id (int):  Example: 12.
        hostname (str):  Example: demo1.example.net.
        module_group_id (int | Unset): Location or module-group choice when the package is sold in multiple places.
            Example: 4.
        user (str | Unset): Optional provisioning username override. Example: debian.
        ssh_key (str | Unset): Optional SSH public key. Alias `ssh_keys` is also accepted. Example: ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example.
        ssh_keys (str | Unset): Alias for `ssh_key`. Example: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey
            user@example.
        coupon (str | Unset):  Example: SPRING10.
        order_form_id (int | Unset): Optional explicit order form override. Example: 1.
        package_group_id (int | Unset): Optional explicit package group override. Example: 3.
        config_options (VmOrderRequestConfigOptions | Unset): Optional package configurable options / add-ons to apply
            to the order, as a map of package-option ID (a positive integer, sent as the string key) to the selected value.
            The available option IDs, labels, and allowed values for each plan are listed under `config_options` in GET
            /ordering/catalog. Example: selecting the +1 TB disk add-on whose option ID is 15 → {"15": "1024"}. Omit to take
            the plan defaults. The Operating System and Desktop Environment are themselves configurable options: the
            `template` option (label "Operating System") selects the OS image (e.g. debian13-cloud, debian12-cloud,
            ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud, alpine323-cloud,
            devuan5-cloud, openbsd79-cloud, windows2022-byol), and the `gui_choice` option (label "Desktop Environment",
            AlmaLinux 9) selects an optional desktop (none, gnome, kde, xfce, cinnamon, mate). Their option IDs and allowed
            values are listed under `config_options` in GET /ordering/catalog. IMPORTANT: a VM order requires a resolved
            operating-system template. If the selected package does not define a default OS template, you MUST include the
            `template` option in config_options (use the option ID and an allowed value from GET /ordering/catalog);
            otherwise the order is rejected at submission with 400 error code `template_required` (no pending
            service/invoice is created). If the package defines a default OS template, `template` is optional and the
            default is used. Example: {'15': '1024'}.
    """

    package_id: int
    pricing_id: int
    hostname: str
    module_group_id: int | Unset = UNSET
    user: str | Unset = UNSET
    ssh_key: str | Unset = UNSET
    ssh_keys: str | Unset = UNSET
    coupon: str | Unset = UNSET
    order_form_id: int | Unset = UNSET
    package_group_id: int | Unset = UNSET
    config_options: VmOrderRequestConfigOptions | Unset = UNSET
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmOrderRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_order_request_additional_property_type_4 import (
            VmOrderRequestAdditionalPropertyType4,
        )

        package_id = self.package_id

        pricing_id = self.pricing_id

        hostname = self.hostname

        module_group_id = self.module_group_id

        user = self.user

        ssh_key = self.ssh_key

        ssh_keys = self.ssh_keys

        coupon = self.coupon

        order_form_id = self.order_form_id

        package_group_id = self.package_group_id

        config_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_options, Unset):
            config_options = self.config_options.to_dict()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmOrderRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "package_id": package_id,
                "pricing_id": pricing_id,
                "hostname": hostname,
            }
        )
        if module_group_id is not UNSET:
            field_dict["module_group_id"] = module_group_id
        if user is not UNSET:
            field_dict["user"] = user
        if ssh_key is not UNSET:
            field_dict["ssh_key"] = ssh_key
        if ssh_keys is not UNSET:
            field_dict["ssh_keys"] = ssh_keys
        if coupon is not UNSET:
            field_dict["coupon"] = coupon
        if order_form_id is not UNSET:
            field_dict["order_form_id"] = order_form_id
        if package_group_id is not UNSET:
            field_dict["package_group_id"] = package_group_id
        if config_options is not UNSET:
            field_dict["config_options"] = config_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_order_request_additional_property_type_4 import (
            VmOrderRequestAdditionalPropertyType4,
        )
        from ..models.vm_order_request_config_options import VmOrderRequestConfigOptions

        d = dict(src_dict)
        package_id = d.pop("package_id")

        pricing_id = d.pop("pricing_id")

        hostname = d.pop("hostname")

        module_group_id = d.pop("module_group_id", UNSET)

        user = d.pop("user", UNSET)

        ssh_key = d.pop("ssh_key", UNSET)

        ssh_keys = d.pop("ssh_keys", UNSET)

        coupon = d.pop("coupon", UNSET)

        order_form_id = d.pop("order_form_id", UNSET)

        package_group_id = d.pop("package_group_id", UNSET)

        _config_options = d.pop("config_options", UNSET)
        config_options: VmOrderRequestConfigOptions | Unset
        if isinstance(_config_options, Unset):
            config_options = UNSET
        else:
            config_options = VmOrderRequestConfigOptions.from_dict(_config_options)

        vm_order_request = cls(
            package_id=package_id,
            pricing_id=pricing_id,
            hostname=hostname,
            module_group_id=module_group_id,
            user=user,
            ssh_key=ssh_key,
            ssh_keys=ssh_keys,
            coupon=coupon,
            order_form_id=order_form_id,
            package_group_id=package_group_id,
            config_options=config_options,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                bool
                | float
                | int
                | list[str]
                | None
                | str
                | VmOrderRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmOrderRequestAdditionalPropertyType4.from_dict(data)
                    )

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_5 = cast(list[str], data)

                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(
                    bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str
                    | VmOrderRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_order_request.additional_properties = additional_properties
        return vm_order_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmOrderRequestAdditionalPropertyType4
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmOrderRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
