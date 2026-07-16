from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitSupportTicketFeedbackBody")


@_attrs_define
class SubmitSupportTicketFeedbackBody:
    """
    Attributes:
        rating (int | str): Required 1 through 5 ticket rating; numeric strings are accepted by the handler.
        rating_comment (None | str | Unset): Optional feedback comment; omitted, null, or empty clears the stored
            comment.
    """

    rating: int | str
    rating_comment: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        rating: int | str
        rating = self.rating

        rating_comment: None | str | Unset
        if isinstance(self.rating_comment, Unset):
            rating_comment = UNSET
        else:
            rating_comment = self.rating_comment

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "rating": rating,
            }
        )
        if rating_comment is not UNSET:
            field_dict["rating_comment"] = rating_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rating(data: object) -> int | str:
            return cast(int | str, data)

        rating = _parse_rating(d.pop("rating"))

        def _parse_rating_comment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rating_comment = _parse_rating_comment(d.pop("rating_comment", UNSET))

        submit_support_ticket_feedback_body = cls(
            rating=rating,
            rating_comment=rating_comment,
        )

        return submit_support_ticket_feedback_body
