from enum import Enum


class PaymentCheckoutRequestGateway(str, Enum):
    BTCPAY_SERVER = "btcpay_server"

    def __str__(self) -> str:
        return str(self.value)
