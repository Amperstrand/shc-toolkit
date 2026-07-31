from typing import Literal

ApproveQuotationResponse201DataStatus = Literal["approved"]

APPROVE_QUOTATION_RESPONSE_201_DATA_STATUS_VALUES: set[
    ApproveQuotationResponse201DataStatus
] = {
    "approved",
}


def check_approve_quotation_response_201_data_status(
    value: str,
) -> ApproveQuotationResponse201DataStatus:
    if value in APPROVE_QUOTATION_RESPONSE_201_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {APPROVE_QUOTATION_RESPONSE_201_DATA_STATUS_VALUES!r}"
    )
