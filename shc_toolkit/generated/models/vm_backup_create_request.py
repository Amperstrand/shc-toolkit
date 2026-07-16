from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_backup_create_request_mode import VmBackupCreateRequestMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_backup_create_request_additional_property_type_4 import (
        VmBackupCreateRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmBackupCreateRequest")


@_attrs_define
class VmBackupCreateRequest:
    """
    Example:
        {'name': 'nightly-demo', 'mode': 'suspend'}

    Attributes:
        name (str | Unset):  Example: nightly-demo.
        mode (VmBackupCreateRequestMode | Unset):  Example: suspend.
        encryption_key (str | Unset): Reserved — client-side backup encryption is not yet available; a non-empty value
            returns 501.
    """

    name: str | Unset = UNSET
    mode: VmBackupCreateRequestMode | Unset = UNSET
    encryption_key: str | Unset = UNSET
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmBackupCreateRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_backup_create_request_additional_property_type_4 import (
            VmBackupCreateRequestAdditionalPropertyType4,
        )

        name = self.name

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        encryption_key = self.encryption_key

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmBackupCreateRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if mode is not UNSET:
            field_dict["mode"] = mode
        if encryption_key is not UNSET:
            field_dict["encryption_key"] = encryption_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_backup_create_request_additional_property_type_4 import (
            VmBackupCreateRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: VmBackupCreateRequestMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = VmBackupCreateRequestMode(_mode)

        encryption_key = d.pop("encryption_key", UNSET)

        vm_backup_create_request = cls(
            name=name,
            mode=mode,
            encryption_key=encryption_key,
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
                | VmBackupCreateRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmBackupCreateRequestAdditionalPropertyType4.from_dict(data)
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
                    | VmBackupCreateRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_backup_create_request.additional_properties = additional_properties
        return vm_backup_create_request

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
        | VmBackupCreateRequestAdditionalPropertyType4
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
        | VmBackupCreateRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
