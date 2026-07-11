from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.service_status import ServiceStatus

T = TypeVar("T", bound="RenewQuote")


@_attrs_define
class RenewQuote:
    """Renewal quote for one existing service.

    Example:
        {'service_id': 353, 'service_status': 'active', 'date_renews': '2027-02-01T07:57:55+00:00', 'term': 1, 'period':
            'month', 'amount': '11.99', 'currency': 'USD'}

    Attributes:
        service_id (int):  Example: 353.
        service_status (ServiceStatus): Blesta service lifecycle state. Example: active.
        date_renews (datetime.datetime | None):  Example: 2027-02-01T07:57:55+00:00.
        term (int):  Example: 1.
        period (str):  Example: month.
        amount (str):  Example: 11.99.
        currency (str):  Example: USD.
    """

    service_id: int
    service_status: ServiceStatus
    date_renews: datetime.datetime | None
    term: int
    period: str
    amount: str
    currency: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        service_status = self.service_status.value

        date_renews: None | str
        if isinstance(self.date_renews, datetime.datetime):
            date_renews = self.date_renews.isoformat()
        else:
            date_renews = self.date_renews

        term = self.term

        period = self.period

        amount = self.amount

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "service_status": service_status,
                "date_renews": date_renews,
                "term": term,
                "period": period,
                "amount": amount,
                "currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        service_status = ServiceStatus(d.pop("service_status"))

        def _parse_date_renews(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_renews_type_0 = datetime.datetime.fromisoformat(data)

                return date_renews_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_renews = _parse_date_renews(d.pop("date_renews"))

        term = d.pop("term")

        period = d.pop("period")

        amount = d.pop("amount")

        currency = d.pop("currency")

        renew_quote = cls(
            service_id=service_id,
            service_status=service_status,
            date_renews=date_renews,
            term=term,
            period=period,
            amount=amount,
            currency=currency,
        )

        renew_quote.additional_properties = d
        return renew_quote

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
