from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitSupportTicketFeedbackBody")


@_attrs_define
class SubmitSupportTicketFeedbackBody:
    """
    Attributes:
        rating (int):
        comment (str | Unset):
    """

    rating: int
    comment: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        rating = self.rating

        comment = self.comment

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "rating": rating,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rating = d.pop("rating")

        comment = d.pop("comment", UNSET)

        submit_support_ticket_feedback_body = cls(
            rating=rating,
            comment=comment,
        )

        return submit_support_ticket_feedback_body
