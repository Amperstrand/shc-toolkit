from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_contact_response_200_data_numbers_item_location import (
    GetContactResponse200DataNumbersItemLocation,
)
from ..models.get_contact_response_200_data_numbers_item_type import (
    GetContactResponse200DataNumbersItemType,
)

T = TypeVar("T", bound="GetContactResponse200DataNumbersItem")


@_attrs_define
class GetContactResponse200DataNumbersItem:
    """
    Attributes:
        number (None | str):  Example: +15125550100.
        type_ (GetContactResponse200DataNumbersItemType):  Example: phone.
        location (GetContactResponse200DataNumbersItemLocation):  Example: work.
    """

    number: None | str
    type_: GetContactResponse200DataNumbersItemType
    location: GetContactResponse200DataNumbersItemLocation

    def to_dict(self) -> dict[str, Any]:
        number: None | str
        number = self.number

        type_ = self.type_.value

        location = self.location.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "number": number,
                "type": type_,
                "location": location,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        number = _parse_number(d.pop("number"))

        type_ = GetContactResponse200DataNumbersItemType(d.pop("type"))

        location = GetContactResponse200DataNumbersItemLocation(d.pop("location"))

        get_contact_response_200_data_numbers_item = cls(
            number=number,
            type_=type_,
            location=location,
        )

        return get_contact_response_200_data_numbers_item
