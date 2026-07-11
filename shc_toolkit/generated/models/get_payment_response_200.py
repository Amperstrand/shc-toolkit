from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.invoice_detail import InvoiceDetail


T = TypeVar("T", bound="GetPaymentResponse200")


@_attrs_define
class GetPaymentResponse200:
    """
    Attributes:
        data (InvoiceDetail):  Example: {'id': 123, 'invoice_status': 'open', 'subtotal': '11.99', 'total': '11.99',
            'paid': '0.00', 'currency': 'USD', 'date_billed': '2026-02-01T07:57:55+00:00', 'date_due':
            '2026-02-08T07:57:55+00:00', 'date_closed': None, 'note': None, 'line_items': {'items': [{'description': 'NVMe
            VPS - Standard', 'qty': 1, 'amount': '11.99'}], 'pagination': {'total': 1, 'limit': 100, 'offset': 0,
            'has_more': False}}}.
    """

    data: InvoiceDetail
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invoice_detail import InvoiceDetail

        d = dict(src_dict)
        data = InvoiceDetail.from_dict(d.pop("data"))

        get_payment_response_200 = cls(
            data=data,
        )

        get_payment_response_200.additional_properties = d
        return get_payment_response_200

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
