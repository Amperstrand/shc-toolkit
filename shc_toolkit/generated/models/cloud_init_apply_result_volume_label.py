from typing import Literal

CloudInitApplyResultVolumeLabel = Literal["CIDATA"]

CLOUD_INIT_APPLY_RESULT_VOLUME_LABEL_VALUES: set[CloudInitApplyResultVolumeLabel] = {
    "CIDATA",
}


def check_cloud_init_apply_result_volume_label(
    value: str,
) -> CloudInitApplyResultVolumeLabel:
    if value in CLOUD_INIT_APPLY_RESULT_VOLUME_LABEL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLOUD_INIT_APPLY_RESULT_VOLUME_LABEL_VALUES!r}"
    )
