from enum import StrEnum


class ListPaymentMethodsResponse200ItemsItemType(StrEnum):
    ACH = "ach"
    CC = "cc"

    def __str__(self) -> str:
        return str(self.value)
