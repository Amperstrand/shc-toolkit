from typing import Literal

AffiliateReferralStatus = Literal["canceled", "mature", "pending"]

AFFILIATE_REFERRAL_STATUS_VALUES: set[AffiliateReferralStatus] = {
    "canceled",
    "mature",
    "pending",
}


def check_affiliate_referral_status(value: str) -> AffiliateReferralStatus:
    if value in AFFILIATE_REFERRAL_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AFFILIATE_REFERRAL_STATUS_VALUES!r}"
    )
