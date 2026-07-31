from typing import Literal

GetTwoFactorStatusResponse200DataMode = Literal["motp", "none", "totp"]

GET_TWO_FACTOR_STATUS_RESPONSE_200_DATA_MODE_VALUES: set[
    GetTwoFactorStatusResponse200DataMode
] = {
    "motp",
    "none",
    "totp",
}


def check_get_two_factor_status_response_200_data_mode(
    value: str,
) -> GetTwoFactorStatusResponse200DataMode:
    if value in GET_TWO_FACTOR_STATUS_RESPONSE_200_DATA_MODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_TWO_FACTOR_STATUS_RESPONSE_200_DATA_MODE_VALUES!r}"
    )
