from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.cancel_pending_order_response_200_data_status import (
    CancelPendingOrderResponse200DataStatus,
    check_cancel_pending_order_response_200_data_status,
)

T = TypeVar("T", bound="CancelPendingOrderResponse200Data")


@_attrs_define
class CancelPendingOrderResponse200Data:
    order_id: int
    order_number: str
    status: CancelPendingOrderResponse200DataStatus
    """ Verified final order status. """
    invoice_id: int
    invoice_status: None | str
    """ Invoice status read back after cancellation, or null if unavailable. """
    deleted_service_ids: list[int]
    """ Pending or in-review services deleted by the cancellation. """

    def to_dict(self) -> dict[str, Any]:
        order_id = self.order_id

        order_number = self.order_number

        status: str = self.status

        invoice_id = self.invoice_id

        invoice_status: None | str
        invoice_status = self.invoice_status

        deleted_service_ids = self.deleted_service_ids

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "order_id": order_id,
                "order_number": order_number,
                "status": status,
                "invoice_id": invoice_id,
                "invoice_status": invoice_status,
                "deleted_service_ids": deleted_service_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        order_id = d.pop("order_id")

        order_number = d.pop("order_number")

        status = check_cancel_pending_order_response_200_data_status(d.pop("status"))

        invoice_id = d.pop("invoice_id")

        def _parse_invoice_status(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        invoice_status = _parse_invoice_status(d.pop("invoice_status"))

        deleted_service_ids = cast(list[int], d.pop("deleted_service_ids"))

        cancel_pending_order_response_200_data = cls(
            order_id=order_id,
            order_number=order_number,
            status=status,
            invoice_id=invoice_id,
            invoice_status=invoice_status,
            deleted_service_ids=deleted_service_ids,
        )

        return cancel_pending_order_response_200_data
