from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.contact_create_response_contact_type import (
    ContactCreateResponseContactType,
)

T = TypeVar("T", bound="ContactCreateResponse")


@_attrs_define
class ContactCreateResponse:
    """
    Attributes:
        id (int):  Example: 88.
        contact_type (ContactCreateResponseContactType):  Example: billing.
        has_login (bool):
        created_at (datetime.datetime):
    """

    id: int
    contact_type: ContactCreateResponseContactType
    has_login: bool
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        contact_type = self.contact_type.value

        has_login = self.has_login

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "contact_type": contact_type,
                "has_login": has_login,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        contact_type = ContactCreateResponseContactType(d.pop("contact_type"))

        has_login = d.pop("has_login")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        contact_create_response = cls(
            id=id,
            contact_type=contact_type,
            has_login=has_login,
            created_at=created_at,
        )

        return contact_create_response
