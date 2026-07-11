from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.transaction_detail import TransactionDetail


T = TypeVar("T", bound="GetTransactionResponse200")


@_attrs_define
class GetTransactionResponse200:
    """
    Attributes:
        data (TransactionDetail):
    """

    data: TransactionDetail

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
        from ..models.transaction_detail import TransactionDetail

        d = dict(src_dict)
        data = TransactionDetail.from_dict(d.pop("data"))

        get_transaction_response_200 = cls(
            data=data,
        )

        return get_transaction_response_200
