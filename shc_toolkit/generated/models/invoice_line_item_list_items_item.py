from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="InvoiceLineItemListItemsItem")


@_attrs_define
class InvoiceLineItemListItemsItem:
    """
    Attributes:
        description (None | str):
        qty (float):  Example: 1.
        amount (str):  Example: 11.99.
    """

    description: None | str
    qty: float
    amount: str

    def to_dict(self) -> dict[str, Any]:
        description: None | str
        description = self.description

        qty = self.qty

        amount = self.amount

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "description": description,
                "qty": qty,
                "amount": amount,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        qty = d.pop("qty")

        amount = d.pop("amount")

        invoice_line_item_list_items_item = cls(
            description=description,
            qty=qty,
            amount=amount,
        )

        return invoice_line_item_list_items_item
