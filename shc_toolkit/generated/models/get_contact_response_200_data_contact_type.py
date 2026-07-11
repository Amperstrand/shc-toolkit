from enum import Enum


class GetContactResponse200DataContactType(str, Enum):
    BILLING = "billing"
    OTHER = "other"
    PRIMARY = "primary"

    def __str__(self) -> str:
        return str(self.value)
