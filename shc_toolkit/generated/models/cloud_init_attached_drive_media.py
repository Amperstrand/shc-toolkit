from typing import Literal

CloudInitAttachedDriveMedia = Literal["cdrom"]

CLOUD_INIT_ATTACHED_DRIVE_MEDIA_VALUES: set[CloudInitAttachedDriveMedia] = {
    "cdrom",
}


def check_cloud_init_attached_drive_media(value: str) -> CloudInitAttachedDriveMedia:
    if value in CLOUD_INIT_ATTACHED_DRIVE_MEDIA_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLOUD_INIT_ATTACHED_DRIVE_MEDIA_VALUES!r}"
    )
