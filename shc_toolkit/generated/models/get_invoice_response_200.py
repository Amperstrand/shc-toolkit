from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.account_invoice_detail import AccountInvoiceDetail


T = TypeVar("T", bound="GetInvoiceResponse200")


@_attrs_define
class GetInvoiceResponse200:
    """
    Attributes:
        data (AccountInvoiceDetail): Customer-safe single invoice with line items and optional applied payments.
    """

    data: AccountInvoiceDetail

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
        from ..models.account_invoice_detail import AccountInvoiceDetail

        d = dict(src_dict)
        data = AccountInvoiceDetail.from_dict(d.pop("data"))

        get_invoice_response_200 = cls(
            data=data,
        )

        return get_invoice_response_200
