from enum import Enum


class ListAffiliatePayoutsStatus(str, Enum):
    APPROVED = "approved"
    DECLINED = "declined"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
