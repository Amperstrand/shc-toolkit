from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.order_list_item_status import OrderListItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderListItem")


@_attrs_define
class OrderListItem:
    """
    Attributes:
        order_id (int):
        order_number (str):
        status (OrderListItemStatus):
        date_added (None | str): Blesta UTC timestamp as emitted by the v2 handler. Example: 2026-07-12 02:50:55.
        invoice_id (int):
        currency (str):
        total (str):
        paid (str):
        balance_due (str):
        order_form_id (int | None | Unset):
        order_form_label (str | Unset):
        invoice_id_code (str | Unset):
        date_closed (None | str | Unset): Blesta UTC timestamp as emitted by the v2 handler. Example: 2026-07-12
            02:50:55.
    """

    order_id: int
    order_number: str
    status: OrderListItemStatus
    date_added: None | str
    invoice_id: int
    currency: str
    total: str
    paid: str
    balance_due: str
    order_form_id: int | None | Unset = UNSET
    order_form_label: str | Unset = UNSET
    invoice_id_code: str | Unset = UNSET
    date_closed: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        order_id = self.order_id

        order_number = self.order_number

        status = self.status.value

        date_added: None | str
        date_added = self.date_added

        invoice_id = self.invoice_id

        currency = self.currency

        total = self.total

        paid = self.paid

        balance_due = self.balance_due

        order_form_id: int | None | Unset
        if isinstance(self.order_form_id, Unset):
            order_form_id = UNSET
        else:
            order_form_id = self.order_form_id

        order_form_label = self.order_form_label

        invoice_id_code = self.invoice_id_code

        date_closed: None | str | Unset
        if isinstance(self.date_closed, Unset):
            date_closed = UNSET
        else:
            date_closed = self.date_closed

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "order_id": order_id,
                "order_number": order_number,
                "status": status,
                "date_added": date_added,
                "invoice_id": invoice_id,
                "currency": currency,
                "total": total,
                "paid": paid,
                "balance_due": balance_due,
            }
        )
        if order_form_id is not UNSET:
            field_dict["order_form_id"] = order_form_id
        if order_form_label is not UNSET:
            field_dict["order_form_label"] = order_form_label
        if invoice_id_code is not UNSET:
            field_dict["invoice_id_code"] = invoice_id_code
        if date_closed is not UNSET:
            field_dict["date_closed"] = date_closed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        order_id = d.pop("order_id")

        order_number = d.pop("order_number")

        status = OrderListItemStatus(d.pop("status"))

        def _parse_date_added(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        date_added = _parse_date_added(d.pop("date_added"))

        invoice_id = d.pop("invoice_id")

        currency = d.pop("currency")

        total = d.pop("total")

        paid = d.pop("paid")

        balance_due = d.pop("balance_due")

        def _parse_order_form_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        order_form_id = _parse_order_form_id(d.pop("order_form_id", UNSET))

        order_form_label = d.pop("order_form_label", UNSET)

        invoice_id_code = d.pop("invoice_id_code", UNSET)

        def _parse_date_closed(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date_closed = _parse_date_closed(d.pop("date_closed", UNSET))

        order_list_item = cls(
            order_id=order_id,
            order_number=order_number,
            status=status,
            date_added=date_added,
            invoice_id=invoice_id,
            currency=currency,
            total=total,
            paid=paid,
            balance_due=balance_due,
            order_form_id=order_form_id,
            order_form_label=order_form_label,
            invoice_id_code=invoice_id_code,
            date_closed=date_closed,
        )

        return order_list_item
