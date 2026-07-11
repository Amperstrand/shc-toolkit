from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateAccountRequest")


@_attrs_define
class UpdateAccountRequest:
    """At least one supported field is required. Empty-string values are rejected on the supplied fields.

    Example:
        {'first_name': 'Jane', 'last_name': 'Smith', 'company': 'Acme LLC'}

    Attributes:
        first_name (str | Unset):
        last_name (str | Unset):
        company (str | Unset):
        address1 (str | Unset):
        address2 (str | Unset):
        city (str | Unset):
        state (str | Unset):
        zip_ (str | Unset):
        country (str | Unset): ISO 3166-1 alpha-2 uppercase country code (e.g. `US`).
    """

    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    company: str | Unset = UNSET
    address1: str | Unset = UNSET
    address2: str | Unset = UNSET
    city: str | Unset = UNSET
    state: str | Unset = UNSET
    zip_: str | Unset = UNSET
    country: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        first_name = self.first_name

        last_name = self.last_name

        company = self.company

        address1 = self.address1

        address2 = self.address2

        city = self.city

        state = self.state

        zip_ = self.zip_

        country = self.country

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if company is not UNSET:
            field_dict["company"] = company
        if address1 is not UNSET:
            field_dict["address1"] = address1
        if address2 is not UNSET:
            field_dict["address2"] = address2
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if zip_ is not UNSET:
            field_dict["zip"] = zip_
        if country is not UNSET:
            field_dict["country"] = country

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        company = d.pop("company", UNSET)

        address1 = d.pop("address1", UNSET)

        address2 = d.pop("address2", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        zip_ = d.pop("zip", UNSET)

        country = d.pop("country", UNSET)

        update_account_request = cls(
            first_name=first_name,
            last_name=last_name,
            company=company,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_=zip_,
            country=country,
        )

        update_account_request.additional_properties = d
        return update_account_request

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
