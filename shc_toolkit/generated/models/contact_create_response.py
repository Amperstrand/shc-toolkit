from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.contact_create_response_contact_type import (
    ContactCreateResponseContactType,
    check_contact_create_response_contact_type,
)

T = TypeVar("T", bound="ContactCreateResponse")


@_attrs_define
class ContactCreateResponse:
    id: int
    contact_type: ContactCreateResponseContactType
    has_login: bool
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        contact_type: str = self.contact_type

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        contact_type = check_contact_create_response_contact_type(d.pop("contact_type"))

        has_login = d.pop("has_login")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        contact_create_response = cls(
            id=id,
            contact_type=contact_type,
            has_login=has_login,
            created_at=created_at,
        )

        return contact_create_response
