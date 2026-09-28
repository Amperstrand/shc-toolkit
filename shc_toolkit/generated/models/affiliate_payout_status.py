from enum import StrEnum


class AffiliatePayoutStatus(StrEnum):
    APPROVED = "approved"
    DECLINED = "declined"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
