from enum import Enum


class ListManagedAccountsResponse200ItemsItemStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
