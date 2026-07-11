from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.pagination import Pagination
    from ..models.transaction_applied_invoice_list_items_item import (
        TransactionAppliedInvoiceListItemsItem,
    )


T = TypeVar("T", bound="TransactionAppliedInvoiceList")


@_attrs_define
class TransactionAppliedInvoiceList:
    """
    Attributes:
        items (list[TransactionAppliedInvoiceListItemsItem]):
        pagination (Pagination):  Example: {'total': 42, 'limit': 100, 'offset': 0, 'has_more': False}.
    """

    items: list[TransactionAppliedInvoiceListItemsItem]
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
        from ..models.pagination import Pagination
        from ..models.transaction_applied_invoice_list_items_item import (
            TransactionAppliedInvoiceListItemsItem,
        )

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = TransactionAppliedInvoiceListItemsItem.from_dict(
                items_item_data
            )

            items.append(items_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        transaction_applied_invoice_list = cls(
            items=items,
            pagination=pagination,
        )

        return transaction_applied_invoice_list
