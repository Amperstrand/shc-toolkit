from typing import Literal

CloudInitApplyResultFormat = Literal["vfat"]

CLOUD_INIT_APPLY_RESULT_FORMAT_VALUES: set[CloudInitApplyResultFormat] = {
    "vfat",
}


def check_cloud_init_apply_result_format(value: str) -> CloudInitApplyResultFormat:
    if value in CLOUD_INIT_APPLY_RESULT_FORMAT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLOUD_INIT_APPLY_RESULT_FORMAT_VALUES!r}"
    )
