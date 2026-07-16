from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.set_ssh_key_request_additional_property_type_4 import (
        SetSshKeyRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="SetSshKeyRequest")


@_attrs_define
class SetSshKeyRequest:
    """
    Example:
        {'service_id': 353, 'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}

    Attributes:
        service_id (int):  Example: 353.
        ssh_key (str): Single-line ssh-rsa, ssh-ed25519, or ecdsa-sha2-nistp256/384/521 public key. Example: ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAA... user@host.
    """

    service_id: int
    ssh_key: str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | SetSshKeyRequestAdditionalPropertyType4
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.set_ssh_key_request_additional_property_type_4 import (
            SetSshKeyRequestAdditionalPropertyType4,
        )

        service_id = self.service_id

        ssh_key = self.ssh_key

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, SetSshKeyRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "service_id": service_id,
                "ssh_key": ssh_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_ssh_key_request_additional_property_type_4 import (
            SetSshKeyRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        ssh_key = d.pop("ssh_key")

        set_ssh_key_request = cls(
            service_id=service_id,
            ssh_key=ssh_key,
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
                | SetSshKeyRequestAdditionalPropertyType4
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        SetSshKeyRequestAdditionalPropertyType4.from_dict(data)
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
                    | SetSshKeyRequestAdditionalPropertyType4
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        set_ssh_key_request.additional_properties = additional_properties
        return set_ssh_key_request

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
        | SetSshKeyRequestAdditionalPropertyType4
        | str
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
        | SetSshKeyRequestAdditionalPropertyType4
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
