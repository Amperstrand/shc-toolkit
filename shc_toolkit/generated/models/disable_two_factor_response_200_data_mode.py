from typing import Literal

DisableTwoFactorResponse200DataMode = Literal["none", "totp"]

DISABLE_TWO_FACTOR_RESPONSE_200_DATA_MODE_VALUES: set[
    DisableTwoFactorResponse200DataMode
] = {
    "none",
    "totp",
}


def check_disable_two_factor_response_200_data_mode(
    value: str,
) -> DisableTwoFactorResponse200DataMode:
    if value in DISABLE_TWO_FACTOR_RESPONSE_200_DATA_MODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DISABLE_TWO_FACTOR_RESPONSE_200_DATA_MODE_VALUES!r}"
    )
