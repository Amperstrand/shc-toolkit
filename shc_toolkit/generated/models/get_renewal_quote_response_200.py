from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.renew_quote import RenewQuote


T = TypeVar("T", bound="GetRenewalQuoteResponse200")


@_attrs_define
class GetRenewalQuoteResponse200:
    """
    Attributes:
        data (RenewQuote): Renewal quote for one existing service. Example: {'service_id': 353, 'service_status':
            'active', 'date_renews': '2027-02-01T07:57:55+00:00', 'term': 1, 'period': 'month', 'amount': '11.99',
            'currency': 'USD'}.
    """

    data: RenewQuote
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.renew_quote import RenewQuote

        d = dict(src_dict)
        data = RenewQuote.from_dict(d.pop("data"))

        get_renewal_quote_response_200 = cls(
            data=data,
        )

        get_renewal_quote_response_200.additional_properties = d
        return get_renewal_quote_response_200

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
