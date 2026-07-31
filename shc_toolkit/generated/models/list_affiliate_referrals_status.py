from typing import Literal

ListAffiliateReferralsStatus = Literal["canceled", "mature", "pending"]

LIST_AFFILIATE_REFERRALS_STATUS_VALUES: set[ListAffiliateReferralsStatus] = {
    "canceled",
    "mature",
    "pending",
}


def check_list_affiliate_referrals_status(value: str) -> ListAffiliateReferralsStatus:
    if value in LIST_AFFILIATE_REFERRALS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_AFFILIATE_REFERRALS_STATUS_VALUES!r}"
    )
