from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteSshKeyResponse")


@_attrs_define
class DeleteSshKeyResponse:
    """
    Example:
        {'deleted': True, 'fingerprint': 'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}

    """

    deleted: bool
    fingerprint: str | Unset = UNSET
    """ Present when a matching key was removed. """
    message: str | Unset = UNSET
    """ Present for idempotent no-op deletes when the fingerprint is not stored. """

    def to_dict(self) -> dict[str, Any]:
        deleted = self.deleted

        fingerprint = self.fingerprint

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "deleted": deleted,
            }
        )
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        deleted = d.pop("deleted")

        fingerprint = d.pop("fingerprint", UNSET)

        message = d.pop("message", UNSET)

        delete_ssh_key_response = cls(
            deleted=deleted,
            fingerprint=fingerprint,
            message=message,
        )

        return delete_ssh_key_response
