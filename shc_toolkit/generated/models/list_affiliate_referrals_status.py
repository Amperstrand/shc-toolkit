from enum import Enum


class ListAffiliateReferralsStatus(str, Enum):
    CANCELED = "canceled"
    MATURE = "mature"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
