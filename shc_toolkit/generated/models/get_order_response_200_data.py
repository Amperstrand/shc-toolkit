from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_order_response_200_data_status import GetOrderResponse200DataStatus

if TYPE_CHECKING:
    from ..models.get_order_response_200_data_invoice import (
        GetOrderResponse200DataInvoice,
    )
    from ..models.get_order_response_200_data_next import GetOrderResponse200DataNext
    from ..models.get_order_response_200_data_services_item import (
        GetOrderResponse200DataServicesItem,
    )


T = TypeVar("T", bound="GetOrderResponse200Data")


@_attrs_define
class GetOrderResponse200Data:
    """
    Attributes:
        order_id (int):
        order_number (str):
        status (GetOrderResponse200DataStatus):
        date_added (None | str): Raw Blesta order timestamp.
        order_form_id (int | None):
        order_form_label (str):
        invoice (GetOrderResponse200DataInvoice):
        services (list[GetOrderResponse200DataServicesItem]):
        cancelable (bool):
        next_ (GetOrderResponse200DataNext):
    """

    order_id: int
    order_number: str
    status: GetOrderResponse200DataStatus
    date_added: None | str
    order_form_id: int | None
    order_form_label: str
    invoice: GetOrderResponse200DataInvoice
    services: list[GetOrderResponse200DataServicesItem]
    cancelable: bool
    next_: GetOrderResponse200DataNext

    def to_dict(self) -> dict[str, Any]:
        order_id = self.order_id

        order_number = self.order_number

        status = self.status.value

        date_added: None | str
        date_added = self.date_added

        order_form_id: int | None
        order_form_id = self.order_form_id

        order_form_label = self.order_form_label

        invoice = self.invoice.to_dict()

        services = []
        for services_item_data in self.services:
            services_item = services_item_data.to_dict()
            services.append(services_item)

        cancelable = self.cancelable

        next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "order_id": order_id,
                "order_number": order_number,
                "status": status,
                "date_added": date_added,
                "order_form_id": order_form_id,
                "order_form_label": order_form_label,
                "invoice": invoice,
                "services": services,
                "cancelable": cancelable,
                "next": next_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_order_response_200_data_invoice import (
            GetOrderResponse200DataInvoice,
        )
        from ..models.get_order_response_200_data_next import (
            GetOrderResponse200DataNext,
        )
        from ..models.get_order_response_200_data_services_item import (
            GetOrderResponse200DataServicesItem,
        )

        d = dict(src_dict)
        order_id = d.pop("order_id")

        order_number = d.pop("order_number")

        status = GetOrderResponse200DataStatus(d.pop("status"))

        def _parse_date_added(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        date_added = _parse_date_added(d.pop("date_added"))

        def _parse_order_form_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        order_form_id = _parse_order_form_id(d.pop("order_form_id"))

        order_form_label = d.pop("order_form_label")

        invoice = GetOrderResponse200DataInvoice.from_dict(d.pop("invoice"))

        services = []
        _services = d.pop("services")
        for services_item_data in _services:
            services_item = GetOrderResponse200DataServicesItem.from_dict(
                services_item_data
            )

            services.append(services_item)

        cancelable = d.pop("cancelable")

        next_ = GetOrderResponse200DataNext.from_dict(d.pop("next"))

        get_order_response_200_data = cls(
            order_id=order_id,
            order_number=order_number,
            status=status,
            date_added=date_added,
            order_form_id=order_form_id,
            order_form_label=order_form_label,
            invoice=invoice,
            services=services,
            cancelable=cancelable,
            next_=next_,
        )

        return get_order_response_200_data
