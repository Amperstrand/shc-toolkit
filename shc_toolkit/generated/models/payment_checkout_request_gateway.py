from typing import Literal

PaymentCheckoutRequestGateway = Literal["btcpay_server"]

PAYMENT_CHECKOUT_REQUEST_GATEWAY_VALUES: set[PaymentCheckoutRequestGateway] = {
    "btcpay_server",
}


def check_payment_checkout_request_gateway(value: str) -> PaymentCheckoutRequestGateway:
    if value in PAYMENT_CHECKOUT_REQUEST_GATEWAY_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PAYMENT_CHECKOUT_REQUEST_GATEWAY_VALUES!r}"
    )
