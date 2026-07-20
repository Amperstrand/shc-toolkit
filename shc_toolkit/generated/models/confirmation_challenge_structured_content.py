from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.confirmation_challenge_structured_content_how_to_proceed import (
        ConfirmationChallengeStructuredContentHowToProceed,
    )


T = TypeVar("T", bound="ConfirmationChallengeStructuredContent")


@_attrs_define
class ConfirmationChallengeStructuredContent:
    """LEGACY nested copy, kept verbatim for existing clients. May be absent.

    Attributes:
        status (str | Unset):  Example: confirmation_required.
        tool (str | Unset): The operationId requiring confirmation.
        spends_money (bool | Unset):
        destructive (bool | Unset):
        money_credential_write (bool | Unset):
        scope (None | str | Unset): Method scope required for the operation.
        confirmation_id (str | Unset):
        idempotency_key (None | str | Unset): The idempotency key bound to this pending action; re-send it unchanged.
        how_to_proceed (ConfirmationChallengeStructuredContentHowToProceed | Unset):
    """

    status: str | Unset = UNSET
    tool: str | Unset = UNSET
    spends_money: bool | Unset = UNSET
    destructive: bool | Unset = UNSET
    money_credential_write: bool | Unset = UNSET
    scope: None | str | Unset = UNSET
    confirmation_id: str | Unset = UNSET
    idempotency_key: None | str | Unset = UNSET
    how_to_proceed: ConfirmationChallengeStructuredContentHowToProceed | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        tool = self.tool

        spends_money = self.spends_money

        destructive = self.destructive

        money_credential_write = self.money_credential_write

        scope: None | str | Unset
        if isinstance(self.scope, Unset):
            scope = UNSET
        else:
            scope = self.scope

        confirmation_id = self.confirmation_id

        idempotency_key: None | str | Unset
        if isinstance(self.idempotency_key, Unset):
            idempotency_key = UNSET
        else:
            idempotency_key = self.idempotency_key

        how_to_proceed: dict[str, Any] | Unset = UNSET
        if not isinstance(self.how_to_proceed, Unset):
            how_to_proceed = self.how_to_proceed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if tool is not UNSET:
            field_dict["tool"] = tool
        if spends_money is not UNSET:
            field_dict["spends_money"] = spends_money
        if destructive is not UNSET:
            field_dict["destructive"] = destructive
        if money_credential_write is not UNSET:
            field_dict["money_credential_write"] = money_credential_write
        if scope is not UNSET:
            field_dict["scope"] = scope
        if confirmation_id is not UNSET:
            field_dict["confirmation_id"] = confirmation_id
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if how_to_proceed is not UNSET:
            field_dict["how_to_proceed"] = how_to_proceed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.confirmation_challenge_structured_content_how_to_proceed import (
            ConfirmationChallengeStructuredContentHowToProceed,
        )

        d = dict(src_dict)
        status = d.pop("status", UNSET)

        tool = d.pop("tool", UNSET)

        spends_money = d.pop("spends_money", UNSET)

        destructive = d.pop("destructive", UNSET)

        money_credential_write = d.pop("money_credential_write", UNSET)

        def _parse_scope(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scope = _parse_scope(d.pop("scope", UNSET))

        confirmation_id = d.pop("confirmation_id", UNSET)

        def _parse_idempotency_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        idempotency_key = _parse_idempotency_key(d.pop("idempotency_key", UNSET))

        _how_to_proceed = d.pop("how_to_proceed", UNSET)
        how_to_proceed: ConfirmationChallengeStructuredContentHowToProceed | Unset
        if isinstance(_how_to_proceed, Unset):
            how_to_proceed = UNSET
        else:
            how_to_proceed = (
                ConfirmationChallengeStructuredContentHowToProceed.from_dict(
                    _how_to_proceed
                )
            )

        confirmation_challenge_structured_content = cls(
            status=status,
            tool=tool,
            spends_money=spends_money,
            destructive=destructive,
            money_credential_write=money_credential_write,
            scope=scope,
            confirmation_id=confirmation_id,
            idempotency_key=idempotency_key,
            how_to_proceed=how_to_proceed,
        )

        confirmation_challenge_structured_content.additional_properties = d
        return confirmation_challenge_structured_content

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
