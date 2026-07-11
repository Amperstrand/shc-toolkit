from enum import Enum


class ListPaymentMethodsResponse200ItemsItemType(str, Enum):
    ACH = "ach"
    CC = "cc"

    def __str__(self) -> str:
        return str(self.value)
