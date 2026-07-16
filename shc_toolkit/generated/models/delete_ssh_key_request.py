from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delete_ssh_key_request_additional_property_type_4 import (
        DeleteSshKeyRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="DeleteSshKeyRequest")


@_attrs_define
class DeleteSshKeyRequest:
    """
    Example:
        {'service_id': 353, 'key_fingerprint': 'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}

    Attributes:
        service_id (int):  Example: 353.
        key_fingerprint (str): Fingerprint of the stored SSH public key to remove. `SHA256:` and `MD5:` forms are
            accepted. Example: SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU.
    """

    service_id: int
    key_fingerprint: str
    additional_properties: dict[
        str,
        bool
        | DeleteSshKeyRequestAdditionalPropertyType4
        | float
        | int
        | list[str]
        | None
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.delete_ssh_key_request_additional_property_type_4 import (
            DeleteSshKeyRequestAdditionalPropertyType4,
        )

        service_id = self.service_id

        key_fingerprint = self.key_fingerprint

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, DeleteSshKeyRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "service_id": service_id,
                "key_fingerprint": key_fingerprint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delete_ssh_key_request_additional_property_type_4 import (
            DeleteSshKeyRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        key_fingerprint = d.pop("key_fingerprint")

        delete_ssh_key_request = cls(
            service_id=service_id,
            key_fingerprint=key_fingerprint,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                bool
                | DeleteSshKeyRequestAdditionalPropertyType4
                | float
                | int
                | list[str]
                | None
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        DeleteSshKeyRequestAdditionalPropertyType4.from_dict(data)
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
                    | DeleteSshKeyRequestAdditionalPropertyType4
                    | float
                    | int
                    | list[str]
                    | None
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        delete_ssh_key_request.additional_properties = additional_properties
        return delete_ssh_key_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        bool
        | DeleteSshKeyRequestAdditionalPropertyType4
        | float
        | int
        | list[str]
        | None
        | str
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: bool
        | DeleteSshKeyRequestAdditionalPropertyType4
        | float
        | int
        | list[str]
        | None
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
