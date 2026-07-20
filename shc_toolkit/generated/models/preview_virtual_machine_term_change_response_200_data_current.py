from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="PreviewVirtualMachineTermChangeResponse200DataCurrent")


@_attrs_define
class PreviewVirtualMachineTermChangeResponse200DataCurrent:
    """
    Attributes:
        pricing_id (int):
        term (int):
        period (str):
        price (str): Current renewal amount as a fixed two-decimal money string.
    """

    pricing_id: int
    term: int
    period: str
    price: str

    def to_dict(self) -> dict[str, Any]:
        pricing_id = self.pricing_id

        term = self.term

        period = self.period

        price = self.price

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "pricing_id": pricing_id,
                "term": term,
                "period": period,
                "price": price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pricing_id = d.pop("pricing_id")

        term = d.pop("term")

        period = d.pop("period")

        price = d.pop("price")

        preview_virtual_machine_term_change_response_200_data_current = cls(
            pricing_id=pricing_id,
            term=term,
            period=period,
            price=price,
        )

        return preview_virtual_machine_term_change_response_200_data_current
