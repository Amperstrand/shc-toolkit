from enum import Enum


class ListAccountManagersResponse200ItemsItemStatusType3Type1(str, Enum):
    ACTIVE = "active"
    INVALID = "invalid"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
