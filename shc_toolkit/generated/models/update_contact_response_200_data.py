from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateContactResponse200Data")


@_attrs_define
class UpdateContactResponse200Data:
    """
    Attributes:
        id (int): Updated contact id.
        contact_type (str): Existing non-primary contact type.
        has_login (bool): Whether the contact has a login after the update.
        email_verification_pending (bool): True when the submitted email changed and verification is pending.
        updated_at (datetime.datetime): Server timestamp when the update completed.
    """

    id: int
    contact_type: str
    has_login: bool
    email_verification_pending: bool
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        contact_type = self.contact_type

        has_login = self.has_login

        email_verification_pending = self.email_verification_pending

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "contact_type": contact_type,
                "has_login": has_login,
                "email_verification_pending": email_verification_pending,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        contact_type = d.pop("contact_type")

        has_login = d.pop("has_login")

        email_verification_pending = d.pop("email_verification_pending")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        update_contact_response_200_data = cls(
            id=id,
            contact_type=contact_type,
            has_login=has_login,
            email_verification_pending=email_verification_pending,
            updated_at=updated_at,
        )

        return update_contact_response_200_data
