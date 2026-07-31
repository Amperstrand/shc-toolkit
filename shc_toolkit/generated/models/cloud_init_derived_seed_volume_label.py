from typing import Literal

CloudInitDerivedSeedVolumeLabel = Literal["CIDATA"]

CLOUD_INIT_DERIVED_SEED_VOLUME_LABEL_VALUES: set[CloudInitDerivedSeedVolumeLabel] = {
    "CIDATA",
}


def check_cloud_init_derived_seed_volume_label(
    value: str,
) -> CloudInitDerivedSeedVolumeLabel:
    if value in CLOUD_INIT_DERIVED_SEED_VOLUME_LABEL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLOUD_INIT_DERIVED_SEED_VOLUME_LABEL_VALUES!r}"
    )
