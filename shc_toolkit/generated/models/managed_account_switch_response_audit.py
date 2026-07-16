from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ManagedAccountSwitchResponseAudit")


@_attrs_define
class ManagedAccountSwitchResponseAudit:
    """Indicates that dual-identity audit fields were recorded for this switch.

    Attributes:
        dual_identity (bool):
    """

    dual_identity: bool

    def to_dict(self) -> dict[str, Any]:
        dual_identity = self.dual_identity

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dual_identity": dual_identity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dual_identity = d.pop("dual_identity")

        managed_account_switch_response_audit = cls(
            dual_identity=dual_identity,
        )

        return managed_account_switch_response_audit
