from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="GetOrderResponse200DataServicesItem")


@_attrs_define
class GetOrderResponse200DataServicesItem:
    """
    Attributes:
        service_id (int):
        status (None | str): Current service status, or null when the service row has been deleted.
    """

    service_id: int
    status: None | str

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        status: None | str
        status = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        def _parse_status(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        status = _parse_status(d.pop("status"))

        get_order_response_200_data_services_item = cls(
            service_id=service_id,
            status=status,
        )

        return get_order_response_200_data_services_item
