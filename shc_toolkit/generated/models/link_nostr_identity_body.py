from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_nostr_identity_body_event_type_0 import (
        LinkNostrIdentityBodyEventType0,
    )
    from ..models.link_nostr_identity_body_target_event_type_0 import (
        LinkNostrIdentityBodyTargetEventType0,
    )


T = TypeVar("T", bound="LinkNostrIdentityBody")


@_attrs_define
class LinkNostrIdentityBody:
    """
    Attributes:
        event (LinkNostrIdentityBodyEventType0 | str): Signed NIP-98 event accepted as a JSON object or JSON string.
        target_event (LinkNostrIdentityBodyTargetEventType0 | str | Unset): Signed NIP-98 event accepted as a JSON
            object or JSON string.
    """

    event: LinkNostrIdentityBodyEventType0 | str
    target_event: LinkNostrIdentityBodyTargetEventType0 | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.link_nostr_identity_body_event_type_0 import (
            LinkNostrIdentityBodyEventType0,
        )
        from ..models.link_nostr_identity_body_target_event_type_0 import (
            LinkNostrIdentityBodyTargetEventType0,
        )

        event: dict[str, Any] | str
        if isinstance(self.event, LinkNostrIdentityBodyEventType0):
            event = self.event.to_dict()
        else:
            event = self.event

        target_event: dict[str, Any] | str | Unset
        if isinstance(self.target_event, Unset):
            target_event = UNSET
        elif isinstance(self.target_event, LinkNostrIdentityBodyTargetEventType0):
            target_event = self.target_event.to_dict()
        else:
            target_event = self.target_event

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "event": event,
            }
        )
        if target_event is not UNSET:
            field_dict["target_event"] = target_event

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.link_nostr_identity_body_event_type_0 import (
            LinkNostrIdentityBodyEventType0,
        )
        from ..models.link_nostr_identity_body_target_event_type_0 import (
            LinkNostrIdentityBodyTargetEventType0,
        )

        d = dict(src_dict)

        def _parse_event(data: object) -> LinkNostrIdentityBodyEventType0 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_0 = LinkNostrIdentityBodyEventType0.from_dict(data)

                return event_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LinkNostrIdentityBodyEventType0 | str, data)

        event = _parse_event(d.pop("event"))

        def _parse_target_event(
            data: object,
        ) -> LinkNostrIdentityBodyTargetEventType0 | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                target_event_type_0 = LinkNostrIdentityBodyTargetEventType0.from_dict(
                    data
                )

                return target_event_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LinkNostrIdentityBodyTargetEventType0 | str | Unset, data)

        target_event = _parse_target_event(d.pop("target_event", UNSET))

        link_nostr_identity_body = cls(
            event=event,
            target_event=target_event,
        )

        return link_nostr_identity_body
