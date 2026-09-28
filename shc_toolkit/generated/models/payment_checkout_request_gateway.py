from enum import StrEnum


class PaymentCheckoutRequestGateway(StrEnum):
    BTCPAY_SERVER = "btcpay_server"

    def __str__(self) -> str:
        return str(self.value)
