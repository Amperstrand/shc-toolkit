from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CancelVmRequest")


@_attrs_define
class CancelVmRequest:
    """
    Example:
        {'reason': 'Service no longer needed after migration.', 'immediate': False}

    Attributes:
        reason (str | Unset): Optional customer-supplied cancellation note. The API trims and sanitizes this value
            before passing it to Blesta. Example: Service no longer needed after migration..
        immediate (bool | Unset): Set to `true` to cancel the service immediately. Leave unset or `false` to cancel at
            the end of the current term. Default: False.
    """

    reason: str | Unset = UNSET
    immediate: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        immediate = self.immediate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason
        if immediate is not UNSET:
            field_dict["immediate"] = immediate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason", UNSET)

        immediate = d.pop("immediate", UNSET)

        cancel_vm_request = cls(
            reason=reason,
            immediate=immediate,
        )

        cancel_vm_request.additional_properties = d
        return cancel_vm_request

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
