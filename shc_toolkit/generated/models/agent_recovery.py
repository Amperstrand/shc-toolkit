from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.agent_recovery_action import AgentRecoveryAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_target import LinkTarget


T = TypeVar("T", bound="AgentRecovery")


@_attrs_define
class AgentRecovery:
    """Machine-readable next action for agents after an error.

    Attributes:
        action (AgentRecoveryAction):  Example: fixRequest.
        message (str):  Example: Correct the fields named in fieldErrors and retry..
        fields (list[str] | Unset):  Example: ['body.hostname'].
        retry_after_seconds (int | Unset):  Example: 30.
        next_ (LinkTarget | Unset): Typed hypermedia target. Relation names are carried by the containing Links object
            and use IANA-registered rels.
    """

    action: AgentRecoveryAction
    message: str
    fields: list[str] | Unset = UNSET
    retry_after_seconds: int | Unset = UNSET
    next_: LinkTarget | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        message = self.message

        fields: list[str] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields

        retry_after_seconds = self.retry_after_seconds

        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "action": action,
                "message": message,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields
        if retry_after_seconds is not UNSET:
            field_dict["retryAfterSeconds"] = retry_after_seconds
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.link_target import LinkTarget

        d = dict(src_dict)
        action = AgentRecoveryAction(d.pop("action"))

        message = d.pop("message")

        fields = cast(list[str], d.pop("fields", UNSET))

        retry_after_seconds = d.pop("retryAfterSeconds", UNSET)

        _next_ = d.pop("next", UNSET)
        next_: LinkTarget | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = LinkTarget.from_dict(_next_)

        agent_recovery = cls(
            action=action,
            message=message,
            fields=fields,
            retry_after_seconds=retry_after_seconds,
            next_=next_,
        )

        return agent_recovery
