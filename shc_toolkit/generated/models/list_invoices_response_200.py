from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.account_invoice_summary import AccountInvoiceSummary
    from ..models.pagination import Pagination


T = TypeVar("T", bound="ListInvoicesResponse200")


@_attrs_define
class ListInvoicesResponse200:
    """
    Attributes:
        items (list[AccountInvoiceSummary]):
        pagination (Pagination):  Example: {'total': 42, 'limit': 100, 'offset': 0, 'has_more': False}.
    """

    items: list[AccountInvoiceSummary]
    pagination: Pagination

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        pagination = self.pagination.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "items": items,
                "pagination": pagination,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_invoice_summary import AccountInvoiceSummary
        from ..models.pagination import Pagination

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = AccountInvoiceSummary.from_dict(items_item_data)

            items.append(items_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        list_invoices_response_200 = cls(
            items=items,
            pagination=pagination,
        )

        return list_invoices_response_200
