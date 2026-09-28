from enum import StrEnum


class ListPaymentMethodsResponse200ItemsItemStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNVERIFIED = "unverified"

    def __str__(self) -> str:
        return str(self.value)
