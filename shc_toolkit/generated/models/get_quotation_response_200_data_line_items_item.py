from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetQuotationResponse200DataLineItemsItem")


@_attrs_define
class GetQuotationResponse200DataLineItemsItem:
    """
    Attributes:
        description (None | str | Unset):
        qty (float | None | Unset):  Example: 1.
        amount (None | str | Unset):  Example: 50.00.
        subtotal (None | str | Unset):  Example: 50.00.
    """

    description: None | str | Unset = UNSET
    qty: float | None | Unset = UNSET
    amount: None | str | Unset = UNSET
    subtotal: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        qty: float | None | Unset
        if isinstance(self.qty, Unset):
            qty = UNSET
        else:
            qty = self.qty

        amount: None | str | Unset
        if isinstance(self.amount, Unset):
            amount = UNSET
        else:
            amount = self.amount

        subtotal: None | str | Unset
        if isinstance(self.subtotal, Unset):
            subtotal = UNSET
        else:
            subtotal = self.subtotal

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if qty is not UNSET:
            field_dict["qty"] = qty
        if amount is not UNSET:
            field_dict["amount"] = amount
        if subtotal is not UNSET:
            field_dict["subtotal"] = subtotal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_qty(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        qty = _parse_qty(d.pop("qty", UNSET))

        def _parse_amount(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        amount = _parse_amount(d.pop("amount", UNSET))

        def _parse_subtotal(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subtotal = _parse_subtotal(d.pop("subtotal", UNSET))

        get_quotation_response_200_data_line_items_item = cls(
            description=description,
            qty=qty,
            amount=amount,
            subtotal=subtotal,
        )

        return get_quotation_response_200_data_line_items_item
