from enum import StrEnum


class ListAccountManagersResponse200ItemsItemStatusType3Type1(StrEnum):
    ACTIVE = "active"
    INVALID = "invalid"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
