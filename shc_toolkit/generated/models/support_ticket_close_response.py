from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SupportTicketCloseResponse")


@_attrs_define
class SupportTicketCloseResponse:
    """
    Attributes:
        ticket_id (int):  Example: 501.
        code (str):  Example: ABC-123456.
        status (str):  Example: closed.
    """

    ticket_id: int
    code: str
    status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket_id = self.ticket_id

        code = self.code

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket_id": ticket_id,
                "code": code,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket_id = d.pop("ticket_id")

        code = d.pop("code")

        status = d.pop("status")

        support_ticket_close_response = cls(
            ticket_id=ticket_id,
            code=code,
            status=status,
        )

        support_ticket_close_response.additional_properties = d
        return support_ticket_close_response

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
