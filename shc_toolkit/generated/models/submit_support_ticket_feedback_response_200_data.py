from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.submit_support_ticket_feedback_response_200_data_status import (
    SubmitSupportTicketFeedbackResponse200DataStatus,
    check_submit_support_ticket_feedback_response_200_data_status,
)

T = TypeVar("T", bound="SubmitSupportTicketFeedbackResponse200Data")


@_attrs_define
class SubmitSupportTicketFeedbackResponse200Data:
    ticket_id: int
    code: str
    """ Customer-visible support ticket code. """
    status: SubmitSupportTicketFeedbackResponse200DataStatus
    """ Ticket status after feedback submission. """
    rating: int
    """ Stored ticket feedback rating. """
    rating_comment: None | str
    """ Stored feedback comment, or null when omitted/cleared. """

    def to_dict(self) -> dict[str, Any]:
        ticket_id = self.ticket_id

        code = self.code

        status: str = self.status

        rating = self.rating

        rating_comment: None | str
        rating_comment = self.rating_comment

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ticket_id": ticket_id,
                "code": code,
                "status": status,
                "rating": rating,
                "rating_comment": rating_comment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        ticket_id = d.pop("ticket_id")

        code = d.pop("code")

        status = check_submit_support_ticket_feedback_response_200_data_status(
            d.pop("status")
        )

        rating = d.pop("rating")

        def _parse_rating_comment(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rating_comment = _parse_rating_comment(d.pop("rating_comment"))

        submit_support_ticket_feedback_response_200_data = cls(
            ticket_id=ticket_id,
            code=code,
            status=status,
            rating=rating,
            rating_comment=rating_comment,
        )

        return submit_support_ticket_feedback_response_200_data
