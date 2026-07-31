from typing import Literal

UpdateNip05Response200DataStatus = Literal["updated"]

UPDATE_NIP_05_RESPONSE_200_DATA_STATUS_VALUES: set[UpdateNip05Response200DataStatus] = {
    "updated",
}


def check_update_nip_05_response_200_data_status(
    value: str,
) -> UpdateNip05Response200DataStatus:
    if value in UPDATE_NIP_05_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPDATE_NIP_05_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
