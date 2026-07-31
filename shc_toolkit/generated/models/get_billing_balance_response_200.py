from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.billing_balance import BillingBalance


T = TypeVar("T", bound="GetBillingBalanceResponse200")


@_attrs_define
class GetBillingBalanceResponse200:
    data: BillingBalance

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.billing_balance import BillingBalance

        d = dict(src_dict)
        data = BillingBalance.from_dict(d.pop("data"))

        get_billing_balance_response_200 = cls(
            data=data,
        )

        return get_billing_balance_response_200
