from enum import StrEnum


class ListAffiliatePayoutsStatus(StrEnum):
    APPROVED = "approved"
    DECLINED = "declined"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
