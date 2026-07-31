from typing import Literal

CloudEventSpecversion = Literal["1.0"]

CLOUD_EVENT_SPECVERSION_VALUES: set[CloudEventSpecversion] = {
    "1.0",
}


def check_cloud_event_specversion(value: str) -> CloudEventSpecversion:
    if value in CLOUD_EVENT_SPECVERSION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLOUD_EVENT_SPECVERSION_VALUES!r}"
    )
