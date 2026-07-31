from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.unlink_nostr_identity_body_event_type_0 import (
        UnlinkNostrIdentityBodyEventType0,
    )


T = TypeVar("T", bound="UnlinkNostrIdentityBody")


@_attrs_define
class UnlinkNostrIdentityBody:
    event: str | UnlinkNostrIdentityBodyEventType0
    """ Signed NIP-98 event accepted as a JSON object or JSON string. """

    def to_dict(self) -> dict[str, Any]:
        from ..models.unlink_nostr_identity_body_event_type_0 import (
            UnlinkNostrIdentityBodyEventType0,
        )

        event: dict[str, Any] | str
        if isinstance(self.event, UnlinkNostrIdentityBodyEventType0):
            event = self.event.to_dict()
        else:
            event = self.event

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "event": event,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.unlink_nostr_identity_body_event_type_0 import (
            UnlinkNostrIdentityBodyEventType0,
        )

        d = dict(src_dict)

        def _parse_event(data: object) -> str | UnlinkNostrIdentityBodyEventType0:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_0 = UnlinkNostrIdentityBodyEventType0.from_dict(data)

                return event_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | UnlinkNostrIdentityBodyEventType0, data)

        event = _parse_event(d.pop("event"))

        unlink_nostr_identity_body = cls(
            event=event,
        )

        return unlink_nostr_identity_body
