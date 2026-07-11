from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.billing_balance import BillingBalance


T = TypeVar("T", bound="GetBillingBalanceResponse200")


@_attrs_define
class GetBillingBalanceResponse200:
    """
    Attributes:
        data (BillingBalance):
    """

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_balance import BillingBalance

        d = dict(src_dict)
        data = BillingBalance.from_dict(d.pop("data"))

        get_billing_balance_response_200 = cls(
            data=data,
        )

        return get_billing_balance_response_200
