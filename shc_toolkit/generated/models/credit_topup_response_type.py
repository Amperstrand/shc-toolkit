from enum import StrEnum


class CreditTopupResponseType(StrEnum):
    ACCOUNT_CREDIT = "account_credit"

    def __str__(self) -> str:
        return str(self.value)
