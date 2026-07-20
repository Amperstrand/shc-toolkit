from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.confirmation_challenge_structured_content_how_to_proceed_arguments import (
        ConfirmationChallengeStructuredContentHowToProceedArguments,
    )


T = TypeVar("T", bound="ConfirmationChallengeStructuredContentHowToProceed")


@_attrs_define
class ConfirmationChallengeStructuredContentHowToProceed:
    """
    Attributes:
        name (str | Unset):
        transport (str | Unset):  Example: header.
        header (str | Unset):  Example: X-User-Api-Confirm.
        confirmation_id (str | Unset):
        arguments (ConfirmationChallengeStructuredContentHowToProceedArguments | Unset):
    """

    name: str | Unset = UNSET
    transport: str | Unset = UNSET
    header: str | Unset = UNSET
    confirmation_id: str | Unset = UNSET
    arguments: ConfirmationChallengeStructuredContentHowToProceedArguments | Unset = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        transport = self.transport

        header = self.header

        confirmation_id = self.confirmation_id

        arguments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if transport is not UNSET:
            field_dict["transport"] = transport
        if header is not UNSET:
            field_dict["header"] = header
        if confirmation_id is not UNSET:
            field_dict["confirmation_id"] = confirmation_id
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.confirmation_challenge_structured_content_how_to_proceed_arguments import (
            ConfirmationChallengeStructuredContentHowToProceedArguments,
        )

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        transport = d.pop("transport", UNSET)

        header = d.pop("header", UNSET)

        confirmation_id = d.pop("confirmation_id", UNSET)

        _arguments = d.pop("arguments", UNSET)
        arguments: ConfirmationChallengeStructuredContentHowToProceedArguments | Unset
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = (
                ConfirmationChallengeStructuredContentHowToProceedArguments.from_dict(
                    _arguments
                )
            )

        confirmation_challenge_structured_content_how_to_proceed = cls(
            name=name,
            transport=transport,
            header=header,
            confirmation_id=confirmation_id,
            arguments=arguments,
        )

        confirmation_challenge_structured_content_how_to_proceed.additional_properties = d
        return confirmation_challenge_structured_content_how_to_proceed

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
