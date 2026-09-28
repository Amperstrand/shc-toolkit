from enum import StrEnum


class ListManagedAccountsResponse200ItemsItemStatus(StrEnum):
    ACTIVE = "active"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
