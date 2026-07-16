from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.list_contacts_response_200_items_item_contact_type import (
    ListContactsResponse200ItemsItemContactType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListContactsResponse200ItemsItem")


@_attrs_define
class ListContactsResponse200ItemsItem:
    """
    Attributes:
        id (int):  Example: 88.
        contact_type (ListContactsResponse200ItemsItemContactType):  Example: other.
        first_name (None | str):  Example: Jane.
        last_name (None | str):  Example: Roe.
        email (None | str):
        has_login (bool):
        company (None | str | Unset):
        title (None | str | Unset):
        date_added (None | str | Unset): Blesta UTC timestamp as emitted by the v2 handler. Example: 2026-07-12
            02:50:55.
    """

    id: int
    contact_type: ListContactsResponse200ItemsItemContactType
    first_name: None | str
    last_name: None | str
    email: None | str
    has_login: bool
    company: None | str | Unset = UNSET
    title: None | str | Unset = UNSET
    date_added: None | str | Unset = UNSET

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

        date_added: None | str | Unset
        if isinstance(self.date_added, Unset):
            date_added = UNSET
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
            }
        )
        if company is not UNSET:
            field_dict["company"] = company
        if title is not UNSET:
            field_dict["title"] = title
        if date_added is not UNSET:
            field_dict["date_added"] = date_added

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        contact_type = ListContactsResponse200ItemsItemContactType(
            d.pop("contact_type")
        )

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

        def _parse_date_added(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date_added = _parse_date_added(d.pop("date_added", UNSET))

        list_contacts_response_200_items_item = cls(
            id=id,
            contact_type=contact_type,
            first_name=first_name,
            last_name=last_name,
            email=email,
            has_login=has_login,
            company=company,
            title=title,
            date_added=date_added,
        )

        return list_contacts_response_200_items_item
