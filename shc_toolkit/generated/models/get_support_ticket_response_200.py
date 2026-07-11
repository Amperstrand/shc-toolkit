from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.get_support_ticket_response_200_data import (
        GetSupportTicketResponse200Data,
    )


T = TypeVar("T", bound="GetSupportTicketResponse200")


@_attrs_define
class GetSupportTicketResponse200:
    """
    Attributes:
        data (GetSupportTicketResponse200Data):
    """

    data: GetSupportTicketResponse200Data

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_support_ticket_response_200_data import (
            GetSupportTicketResponse200Data,
        )

        d = dict(src_dict)
        data = GetSupportTicketResponse200Data.from_dict(d.pop("data"))

        get_support_ticket_response_200 = cls(
            data=data,
        )

        return get_support_ticket_response_200
