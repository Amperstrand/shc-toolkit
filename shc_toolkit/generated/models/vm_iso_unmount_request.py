from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_iso_unmount_request_additional_property_type_4 import (
        VmIsoUnmountRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmIsoUnmountRequest")


@_attrs_define
class VmIsoUnmountRequest:
    """Unmount a mounted ISO CD-ROM drive. Idempotent: an absent/already-unmounted drive returns 200 with the refreshed
    list.

        Example:
            {'drive': 'ide2'}

        Attributes:
            drive (str): QEMU IDE cdrom drive key to detach (from the `mounted` list of GET /vm/{service_id}/iso), e.g.
                ide2. Example: ide2.
    """

    drive: str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmIsoUnmountRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_iso_unmount_request_additional_property_type_4 import (
            VmIsoUnmountRequestAdditionalPropertyType4,
        )

        drive = self.drive

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmIsoUnmountRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "drive": drive,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_iso_unmount_request_additional_property_type_4 import (
            VmIsoUnmountRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        drive = d.pop("drive")

        vm_iso_unmount_request = cls(
            drive=drive,
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
                | VmIsoUnmountRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmIsoUnmountRequestAdditionalPropertyType4.from_dict(data)
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
                    | VmIsoUnmountRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_iso_unmount_request.additional_properties = additional_properties
        return vm_iso_unmount_request

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
        | VmIsoUnmountRequestAdditionalPropertyType4
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
        | VmIsoUnmountRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
