from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.payment_checkout_request_gateway import PaymentCheckoutRequestGateway
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_checkout_request_additional_property_type_4 import (
        PaymentCheckoutRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="PaymentCheckoutRequest")


@_attrs_define
class PaymentCheckoutRequest:
    """
    Example:
        {'gateway': 'btcpay_server', 'idempotency_key': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7', 'return_url':
            'https://app.example.com/billing/return', 'cancel_url': 'https://app.example.com/billing/cancel'}

    Attributes:
        idempotency_key (str): Invoice-scoped idempotency key. Reuse the same value with the same body to replay the
            original response for this invoice. Example: 5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
        gateway (PaymentCheckoutRequestGateway | Unset): Gateway class selector. Only the enabled BTCPay nonmerchant
            gateway is currently accepted; other values return 400. Default: PaymentCheckoutRequestGateway.BTCPAY_SERVER.
            Example: btcpay_server.
        return_url (None | str | Unset): Optional HTTPS URL to which BTCPay should redirect the browser after checkout.
            Non-https URLs are rejected with 400. Example: https://app.example.com/billing/return.
        cancel_url (None | str | Unset): Optional HTTPS URL accepted for client compatibility. BTCPay's native Blesta
            flow uses a single redirect URL, so this value is advisory unless the gateway gains first-class support for it.
            Non-https URLs are rejected with 400. Example: https://app.example.com/billing/cancel.
    """

    idempotency_key: str
    gateway: PaymentCheckoutRequestGateway | Unset = (
        PaymentCheckoutRequestGateway.BTCPAY_SERVER
    )
    return_url: None | str | Unset = UNSET
    cancel_url: None | str | Unset = UNSET
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | PaymentCheckoutRequestAdditionalPropertyType4
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.payment_checkout_request_additional_property_type_4 import (
            PaymentCheckoutRequestAdditionalPropertyType4,
        )

        idempotency_key = self.idempotency_key

        gateway: str | Unset = UNSET
        if not isinstance(self.gateway, Unset):
            gateway = self.gateway.value

        return_url: None | str | Unset
        if isinstance(self.return_url, Unset):
            return_url = UNSET
        else:
            return_url = self.return_url

        cancel_url: None | str | Unset
        if isinstance(self.cancel_url, Unset):
            cancel_url = UNSET
        else:
            cancel_url = self.cancel_url

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, PaymentCheckoutRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "idempotency_key": idempotency_key,
            }
        )
        if gateway is not UNSET:
            field_dict["gateway"] = gateway
        if return_url is not UNSET:
            field_dict["return_url"] = return_url
        if cancel_url is not UNSET:
            field_dict["cancel_url"] = cancel_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_checkout_request_additional_property_type_4 import (
            PaymentCheckoutRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        idempotency_key = d.pop("idempotency_key")

        _gateway = d.pop("gateway", UNSET)
        gateway: PaymentCheckoutRequestGateway | Unset
        if isinstance(_gateway, Unset):
            gateway = UNSET
        else:
            gateway = PaymentCheckoutRequestGateway(_gateway)

        def _parse_return_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        return_url = _parse_return_url(d.pop("return_url", UNSET))

        def _parse_cancel_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cancel_url = _parse_cancel_url(d.pop("cancel_url", UNSET))

        payment_checkout_request = cls(
            idempotency_key=idempotency_key,
            gateway=gateway,
            return_url=return_url,
            cancel_url=cancel_url,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                bool
                | float
                | int
                | list[str]
                | None
                | PaymentCheckoutRequestAdditionalPropertyType4
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        PaymentCheckoutRequestAdditionalPropertyType4.from_dict(data)
                    )

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_5 = cast(list[str], data)

                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(
                    bool
                    | float
                    | int
                    | list[str]
                    | None
                    | PaymentCheckoutRequestAdditionalPropertyType4
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        payment_checkout_request.additional_properties = additional_properties
        return payment_checkout_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        bool
        | float
        | int
        | list[str]
        | None
        | PaymentCheckoutRequestAdditionalPropertyType4
        | str
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: bool
        | float
        | int
        | list[str]
        | None
        | PaymentCheckoutRequestAdditionalPropertyType4
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
