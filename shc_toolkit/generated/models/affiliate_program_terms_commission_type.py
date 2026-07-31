from typing import Literal

AffiliateProgramTermsCommissionType = Literal["fixed", "percentage"]

AFFILIATE_PROGRAM_TERMS_COMMISSION_TYPE_VALUES: set[
    AffiliateProgramTermsCommissionType
] = {
    "fixed",
    "percentage",
}


def check_affiliate_program_terms_commission_type(
    value: str,
) -> AffiliateProgramTermsCommissionType:
    if value in AFFILIATE_PROGRAM_TERMS_COMMISSION_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AFFILIATE_PROGRAM_TERMS_COMMISSION_TYPE_VALUES!r}"
    )
