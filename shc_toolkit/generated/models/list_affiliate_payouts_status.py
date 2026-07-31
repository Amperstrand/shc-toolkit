from typing import Literal

ListAffiliatePayoutsStatus = Literal["approved", "declined", "pending"]

LIST_AFFILIATE_PAYOUTS_STATUS_VALUES: set[ListAffiliatePayoutsStatus] = {
    "approved",
    "declined",
    "pending",
}


def check_list_affiliate_payouts_status(value: str) -> ListAffiliatePayoutsStatus:
    if value in LIST_AFFILIATE_PAYOUTS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_AFFILIATE_PAYOUTS_STATUS_VALUES!r}"
    )
