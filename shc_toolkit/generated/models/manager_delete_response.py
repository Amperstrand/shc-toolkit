from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.manager_delete_response_status import (
    ManagerDeleteResponseStatus,
    check_manager_delete_response_status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ManagerDeleteResponse")


@_attrs_define
class ManagerDeleteResponse:
    """Result of revoking an active manager (returns contact_id) or declining a pending invitation (returns
    status=declined).

    """

    revoked: bool
    contact_id: int | Unset = UNSET
    """ Present when an active manager (numeric ref) was revoked. """
    status: ManagerDeleteResponseStatus | Unset = UNSET
    """ Present (value `declined`) when a pending invitation (token ref) was cancelled. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        revoked = self.revoked

        contact_id = self.contact_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "revoked": revoked,
            }
        )
        if contact_id is not UNSET:
            field_dict["contact_id"] = contact_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        revoked = d.pop("revoked")

        contact_id = d.pop("contact_id", UNSET)

        _status = d.pop("status", UNSET)
        status: ManagerDeleteResponseStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = check_manager_delete_response_status(_status)

        manager_delete_response = cls(
            revoked=revoked,
            contact_id=contact_id,
            status=status,
        )

        manager_delete_response.additional_properties = d
        return manager_delete_response

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
