from enum import Enum


class ListPaymentMethodsResponse200ItemsItemStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNVERIFIED = "unverified"

    def __str__(self) -> str:
        return str(self.value)
