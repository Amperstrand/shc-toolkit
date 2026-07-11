from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteSshKeyResponse")


@_attrs_define
class DeleteSshKeyResponse:
    """
    Example:
        {'deleted': True, 'fingerprint': 'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}

    Attributes:
        deleted (bool):  Example: True.
        fingerprint (str | Unset): Present when a matching key was removed. Example:
            SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU.
        message (str | Unset): Present for idempotent no-op deletes when the fingerprint is not stored. Example: key not
            present.
    """

    deleted: bool
    fingerprint: str | Unset = UNSET
    message: str | Unset = UNSET

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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
