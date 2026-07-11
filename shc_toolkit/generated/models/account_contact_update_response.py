from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountContactUpdateResponse")


@_attrs_define
class AccountContactUpdateResponse:
    """
    Example:
        {'contact_updated_at': '2026-05-05T23:15:42+00:00', 'email_verification_required': True}

    Attributes:
        contact_updated_at (datetime.datetime):  Example: 2026-05-05T23:15:42+00:00.
        email_verification_required (bool | Unset): Present and true when the submitted email address changed and Blesta
            email verification is now required.
    """

    contact_updated_at: datetime.datetime
    email_verification_required: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        contact_updated_at = self.contact_updated_at.isoformat()

        email_verification_required = self.email_verification_required

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "contact_updated_at": contact_updated_at,
            }
        )
        if email_verification_required is not UNSET:
            field_dict["email_verification_required"] = email_verification_required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        contact_updated_at = datetime.datetime.fromisoformat(
            d.pop("contact_updated_at")
        )

        email_verification_required = d.pop("email_verification_required", UNSET)

        account_contact_update_response = cls(
            contact_updated_at=contact_updated_at,
            email_verification_required=email_verification_required,
        )

        return account_contact_update_response
