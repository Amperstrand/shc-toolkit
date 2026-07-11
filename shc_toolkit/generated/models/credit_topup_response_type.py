from enum import Enum


class CreditTopupResponseType(str, Enum):
    ACCOUNT_CREDIT = "account_credit"

    def __str__(self) -> str:
        return str(self.value)
