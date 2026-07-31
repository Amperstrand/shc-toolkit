from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="ManagedAccountSwitchResponseAudit")


@_attrs_define
class ManagedAccountSwitchResponseAudit:
    """Indicates that dual-identity audit fields were recorded for this switch."""

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        dual_identity = d.pop("dual_identity")

        managed_account_switch_response_audit = cls(
            dual_identity=dual_identity,
        )

        return managed_account_switch_response_audit
