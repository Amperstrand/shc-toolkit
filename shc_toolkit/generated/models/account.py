from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """Primary contact profile for the authenticated customer account.

    Attributes:
        email (str):  Example: you@example.com.
        first_name (str):  Example: Jane.
        last_name (str):  Example: Doe.
        company (None | str):  Example: Acme LLC.
        address1 (None | str):  Example: 123 Main St.
        address2 (None | str):  Example: Suite 400.
        city (None | str):  Example: Austin.
        state (None | str):  Example: TX.
        zip_ (None | str):  Example: 78701.
        country (None | str): ISO 3166-1 alpha-2 uppercase country code (e.g. `US`). Example: US.
    """

    email: str
    first_name: str
    last_name: str
    company: None | str
    address1: None | str
    address2: None | str
    city: None | str
    state: None | str
    zip_: None | str
    country: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        company: None | str
        company = self.company

        address1: None | str
        address1 = self.address1

        address2: None | str
        address2 = self.address2

        city: None | str
        city = self.city

        state: None | str
        state = self.state

        zip_: None | str
        zip_ = self.zip_

        country: None | str
        country = self.country

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "address1": address1,
                "address2": address2,
                "city": city,
                "state": state,
                "zip": zip_,
                "country": country,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        def _parse_company(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        company = _parse_company(d.pop("company"))

        def _parse_address1(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        address1 = _parse_address1(d.pop("address1"))

        def _parse_address2(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        address2 = _parse_address2(d.pop("address2"))

        def _parse_city(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        city = _parse_city(d.pop("city"))

        def _parse_state(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        state = _parse_state(d.pop("state"))

        def _parse_zip_(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        zip_ = _parse_zip_(d.pop("zip"))

        def _parse_country(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        country = _parse_country(d.pop("country"))

        account = cls(
            email=email,
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

        account.additional_properties = d
        return account

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
