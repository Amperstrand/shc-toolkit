from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_contact_response_200_data_contact_type import (
    GetContactResponse200DataContactType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_contact_response_200_data_numbers_item import (
        GetContactResponse200DataNumbersItem,
    )


T = TypeVar("T", bound="GetContactResponse200Data")


@_attrs_define
class GetContactResponse200Data:
    """
    Attributes:
        id (int):  Example: 88.
        contact_type (GetContactResponse200DataContactType):
        first_name (None | str):
        last_name (None | str):
        email (None | str):
        has_login (bool):
        numbers (list[GetContactResponse200DataNumbersItem]):
        permissions (list[str]):  Example: ['client_invoices', 'client_services'].
        company (None | str | Unset):
        title (None | str | Unset):
        address1 (None | str | Unset):
        address2 (None | str | Unset):
        city (None | str | Unset):
        state (None | str | Unset):
        zip_ (None | str | Unset):
        country (None | str | Unset):
        date_added (datetime.datetime | None | Unset):
    """

    id: int
    contact_type: GetContactResponse200DataContactType
    first_name: None | str
    last_name: None | str
    email: None | str
    has_login: bool
    numbers: list[GetContactResponse200DataNumbersItem]
    permissions: list[str]
    company: None | str | Unset = UNSET
    title: None | str | Unset = UNSET
    address1: None | str | Unset = UNSET
    address2: None | str | Unset = UNSET
    city: None | str | Unset = UNSET
    state: None | str | Unset = UNSET
    zip_: None | str | Unset = UNSET
    country: None | str | Unset = UNSET
    date_added: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        contact_type = self.contact_type.value

        first_name: None | str
        first_name = self.first_name

        last_name: None | str
        last_name = self.last_name

        email: None | str
        email = self.email

        has_login = self.has_login

        numbers = []
        for numbers_item_data in self.numbers:
            numbers_item = numbers_item_data.to_dict()
            numbers.append(numbers_item)

        permissions = self.permissions

        company: None | str | Unset
        if isinstance(self.company, Unset):
            company = UNSET
        else:
            company = self.company

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        address1: None | str | Unset
        if isinstance(self.address1, Unset):
            address1 = UNSET
        else:
            address1 = self.address1

        address2: None | str | Unset
        if isinstance(self.address2, Unset):
            address2 = UNSET
        else:
            address2 = self.address2

        city: None | str | Unset
        if isinstance(self.city, Unset):
            city = UNSET
        else:
            city = self.city

        state: None | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        zip_: None | str | Unset
        if isinstance(self.zip_, Unset):
            zip_ = UNSET
        else:
            zip_ = self.zip_

        country: None | str | Unset
        if isinstance(self.country, Unset):
            country = UNSET
        else:
            country = self.country

        date_added: None | str | Unset
        if isinstance(self.date_added, Unset):
            date_added = UNSET
        elif isinstance(self.date_added, datetime.datetime):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "contact_type": contact_type,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "has_login": has_login,
                "numbers": numbers,
                "permissions": permissions,
            }
        )
        if company is not UNSET:
            field_dict["company"] = company
        if title is not UNSET:
            field_dict["title"] = title
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
        if date_added is not UNSET:
            field_dict["date_added"] = date_added

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_contact_response_200_data_numbers_item import (
            GetContactResponse200DataNumbersItem,
        )

        d = dict(src_dict)
        id = d.pop("id")

        contact_type = GetContactResponse200DataContactType(d.pop("contact_type"))

        def _parse_first_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        first_name = _parse_first_name(d.pop("first_name"))

        def _parse_last_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_name = _parse_last_name(d.pop("last_name"))

        def _parse_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        email = _parse_email(d.pop("email"))

        has_login = d.pop("has_login")

        numbers = []
        _numbers = d.pop("numbers")
        for numbers_item_data in _numbers:
            numbers_item = GetContactResponse200DataNumbersItem.from_dict(
                numbers_item_data
            )

            numbers.append(numbers_item)

        permissions = cast(list[str], d.pop("permissions"))

        def _parse_company(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        company = _parse_company(d.pop("company", UNSET))

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_address1(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        address1 = _parse_address1(d.pop("address1", UNSET))

        def _parse_address2(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        address2 = _parse_address2(d.pop("address2", UNSET))

        def _parse_city(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        city = _parse_city(d.pop("city", UNSET))

        def _parse_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        state = _parse_state(d.pop("state", UNSET))

        def _parse_zip_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        zip_ = _parse_zip_(d.pop("zip", UNSET))

        def _parse_country(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        country = _parse_country(d.pop("country", UNSET))

        def _parse_date_added(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.datetime.fromisoformat(data)

                return date_added_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_added = _parse_date_added(d.pop("date_added", UNSET))

        get_contact_response_200_data = cls(
            id=id,
            contact_type=contact_type,
            first_name=first_name,
            last_name=last_name,
            email=email,
            has_login=has_login,
            numbers=numbers,
            permissions=permissions,
            company=company,
            title=title,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_=zip_,
            country=country,
            date_added=date_added,
        )

        return get_contact_response_200_data
