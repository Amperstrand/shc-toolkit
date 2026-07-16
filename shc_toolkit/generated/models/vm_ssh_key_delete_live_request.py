from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_ssh_key_delete_live_request_additional_property_type_4 import (
        VmSshKeyDeleteLiveRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmSshKeyDeleteLiveRequest")


@_attrs_define
class VmSshKeyDeleteLiveRequest:
    """Live-remove an SSH key from the running VM by fingerprint, and scrub it from the persisted set.

    Example:
        {'key_fingerprint': 'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}

    Attributes:
        key_fingerprint (str): Fingerprint of the key to remove. `SHA256:` and `MD5:` forms are accepted. Example:
            SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU.
    """

    key_fingerprint: str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmSshKeyDeleteLiveRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_ssh_key_delete_live_request_additional_property_type_4 import (
            VmSshKeyDeleteLiveRequestAdditionalPropertyType4,
        )

        key_fingerprint = self.key_fingerprint

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmSshKeyDeleteLiveRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "key_fingerprint": key_fingerprint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_ssh_key_delete_live_request_additional_property_type_4 import (
            VmSshKeyDeleteLiveRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        key_fingerprint = d.pop("key_fingerprint")

        vm_ssh_key_delete_live_request = cls(
            key_fingerprint=key_fingerprint,
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
                | VmSshKeyDeleteLiveRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmSshKeyDeleteLiveRequestAdditionalPropertyType4.from_dict(data)
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
                    | VmSshKeyDeleteLiveRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_ssh_key_delete_live_request.additional_properties = additional_properties
        return vm_ssh_key_delete_live_request

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
        | VmSshKeyDeleteLiveRequestAdditionalPropertyType4
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
        | VmSshKeyDeleteLiveRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
