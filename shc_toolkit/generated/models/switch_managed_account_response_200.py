from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.managed_account_switch_response import ManagedAccountSwitchResponse


T = TypeVar("T", bound="SwitchManagedAccountResponse200")


@_attrs_define
class SwitchManagedAccountResponse200:
    """
    Attributes:
        data (ManagedAccountSwitchResponse):
    """

    data: ManagedAccountSwitchResponse

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_account_switch_response import (
            ManagedAccountSwitchResponse,
        )

        d = dict(src_dict)
        data = ManagedAccountSwitchResponse.from_dict(d.pop("data"))

        switch_managed_account_response_200 = cls(
            data=data,
        )

        return switch_managed_account_response_200
