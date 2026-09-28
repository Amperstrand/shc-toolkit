from enum import StrEnum


class AffiliateReferralStatus(StrEnum):
    CANCELED = "canceled"
    MATURE = "mature"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
