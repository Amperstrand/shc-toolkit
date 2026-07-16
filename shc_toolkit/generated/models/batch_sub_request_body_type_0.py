from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.batch_sub_request_body_type_0_additional_property_type_4 import (
        BatchSubRequestBodyType0AdditionalPropertyType4,
    )


T = TypeVar("T", bound="BatchSubRequestBodyType0")


@_attrs_define
class BatchSubRequestBodyType0:
    """Optional JSON request body for this sub-request. Unknown fields are validated against the target operation schema
    before dispatch.

    """

    additional_properties: dict[
        str,
        BatchSubRequestBodyType0AdditionalPropertyType4
        | bool
        | float
        | int
        | list[str]
        | None
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_sub_request_body_type_0_additional_property_type_4 import (
            BatchSubRequestBodyType0AdditionalPropertyType4,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, BatchSubRequestBodyType0AdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_sub_request_body_type_0_additional_property_type_4 import (
            BatchSubRequestBodyType0AdditionalPropertyType4,
        )

        d = dict(src_dict)
        batch_sub_request_body_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                BatchSubRequestBodyType0AdditionalPropertyType4
                | bool
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
                        BatchSubRequestBodyType0AdditionalPropertyType4.from_dict(data)
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
                    BatchSubRequestBodyType0AdditionalPropertyType4
                    | bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        batch_sub_request_body_type_0.additional_properties = additional_properties
        return batch_sub_request_body_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        BatchSubRequestBodyType0AdditionalPropertyType4
        | bool
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
        value: BatchSubRequestBodyType0AdditionalPropertyType4
        | bool
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
