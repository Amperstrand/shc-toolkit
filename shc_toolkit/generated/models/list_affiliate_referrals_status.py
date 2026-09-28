from enum import StrEnum


class ListAffiliateReferralsStatus(StrEnum):
    CANCELED = "canceled"
    MATURE = "mature"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
