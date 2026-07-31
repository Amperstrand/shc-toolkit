from typing import Literal

CreditTopupResponseType = Literal["account_credit"]

CREDIT_TOPUP_RESPONSE_TYPE_VALUES: set[CreditTopupResponseType] = {
    "account_credit",
}


def check_credit_topup_response_type(value: str) -> CreditTopupResponseType:
    if value in CREDIT_TOPUP_RESPONSE_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREDIT_TOPUP_RESPONSE_TYPE_VALUES!r}"
    )
