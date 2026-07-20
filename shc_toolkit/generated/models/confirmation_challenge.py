from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.confirmation_challenge_content_item import (
        ConfirmationChallengeContentItem,
    )
    from ..models.confirmation_challenge_structured_content import (
        ConfirmationChallengeStructuredContent,
    )


T = TypeVar("T", bound="ConfirmationChallenge")


@_attrs_define
class ConfirmationChallenge:
    """Present on a 409 whose error.code is `confirmation_required`. The action was NOT performed. Re-send the IDENTICAL
    request (same path, query, body and Idempotency-Key) with header `X-User-Api-Confirm: <confirmation_id>`. A
    confirmation_id is NOT permission: obtain an explicit human yes to THIS specific action first. The id is non-secret,
    single-use, and names an already-bound pending action.

        Attributes:
            confirmation_id (str): STABLE PATH - read this. Mirrored flat at `confirmation.confirmation_id` since v2.4.0 and
                always present. The nested copies under `structuredContent` are legacy and may be absent; do not depend on them.
                Example: cnf_9f2c1ab4d7e34c02.
            is_error (bool | Unset): Legacy MCP-envelope remnant. Always false here.
            content (list[ConfirmationChallengeContentItem] | Unset): Legacy MCP-envelope remnant: the human-facing prompt
                text.
            structured_content (ConfirmationChallengeStructuredContent | Unset): LEGACY nested copy, kept verbatim for
                existing clients. May be absent.
    """

    confirmation_id: str
    is_error: bool | Unset = UNSET
    content: list[ConfirmationChallengeContentItem] | Unset = UNSET
    structured_content: ConfirmationChallengeStructuredContent | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        confirmation_id = self.confirmation_id

        is_error = self.is_error

        content: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item = content_item_data.to_dict()
                content.append(content_item)

        structured_content: dict[str, Any] | Unset = UNSET
        if not isinstance(self.structured_content, Unset):
            structured_content = self.structured_content.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "confirmation_id": confirmation_id,
            }
        )
        if is_error is not UNSET:
            field_dict["isError"] = is_error
        if content is not UNSET:
            field_dict["content"] = content
        if structured_content is not UNSET:
            field_dict["structuredContent"] = structured_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.confirmation_challenge_content_item import (
            ConfirmationChallengeContentItem,
        )
        from ..models.confirmation_challenge_structured_content import (
            ConfirmationChallengeStructuredContent,
        )

        d = dict(src_dict)
        confirmation_id = d.pop("confirmation_id")

        is_error = d.pop("isError", UNSET)

        _content = d.pop("content", UNSET)
        content: list[ConfirmationChallengeContentItem] | Unset = UNSET
        if _content is not UNSET:
            content = []
            for content_item_data in _content:
                content_item = ConfirmationChallengeContentItem.from_dict(
                    content_item_data
                )

                content.append(content_item)

        _structured_content = d.pop("structuredContent", UNSET)
        structured_content: ConfirmationChallengeStructuredContent | Unset
        if isinstance(_structured_content, Unset):
            structured_content = UNSET
        else:
            structured_content = ConfirmationChallengeStructuredContent.from_dict(
                _structured_content
            )

        confirmation_challenge = cls(
            confirmation_id=confirmation_id,
            is_error=is_error,
            content=content,
            structured_content=structured_content,
        )

        confirmation_challenge.additional_properties = d
        return confirmation_challenge

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
