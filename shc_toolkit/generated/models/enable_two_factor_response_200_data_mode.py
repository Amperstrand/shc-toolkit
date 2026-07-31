from typing import Literal

EnableTwoFactorResponse200DataMode = Literal["none", "totp"]

ENABLE_TWO_FACTOR_RESPONSE_200_DATA_MODE_VALUES: set[
    EnableTwoFactorResponse200DataMode
] = {
    "none",
    "totp",
}


def check_enable_two_factor_response_200_data_mode(
    value: str,
) -> EnableTwoFactorResponse200DataMode:
    if value in ENABLE_TWO_FACTOR_RESPONSE_200_DATA_MODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ENABLE_TWO_FACTOR_RESPONSE_200_DATA_MODE_VALUES!r}"
    )
