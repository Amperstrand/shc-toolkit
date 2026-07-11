from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountPasswordChangeRequest")


@_attrs_define
class AccountPasswordChangeRequest:
    """
    Example:
        {'current_password': '<current-password>', 'new_password': '<new-password>', 'idempotency_key':
            '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}

    Attributes:
        current_password (str): The authenticated customer's current Blesta login password.
        new_password (str): The replacement password. Must satisfy the company's configured Blesta password rules.
        idempotency_key (str | Unset): Optional opaque caller-supplied key for retry-safe client bookkeeping.
    """

    current_password: str
    new_password: str
    idempotency_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_password = self.current_password

        new_password = self.new_password

        idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_password": current_password,
                "new_password": new_password,
            }
        )
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        current_password = d.pop("current_password")

        new_password = d.pop("new_password")

        idempotency_key = d.pop("idempotency_key", UNSET)

        account_password_change_request = cls(
            current_password=current_password,
            new_password=new_password,
            idempotency_key=idempotency_key,
        )

        account_password_change_request.additional_properties = d
        return account_password_change_request

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
