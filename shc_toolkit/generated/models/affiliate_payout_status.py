from typing import Literal

AffiliatePayoutStatus = Literal["approved", "declined", "pending"]

AFFILIATE_PAYOUT_STATUS_VALUES: set[AffiliatePayoutStatus] = {
    "approved",
    "declined",
    "pending",
}


def check_affiliate_payout_status(value: str) -> AffiliatePayoutStatus:
    if value in AFFILIATE_PAYOUT_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AFFILIATE_PAYOUT_STATUS_VALUES!r}"
    )
