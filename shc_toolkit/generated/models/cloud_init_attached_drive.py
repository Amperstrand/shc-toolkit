from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.cloud_init_attached_drive_media import (
    CloudInitAttachedDriveMedia,
    check_cloud_init_attached_drive_media,
)

T = TypeVar("T", bound="CloudInitAttachedDrive")


@_attrs_define
class CloudInitAttachedDrive:
    drive: str
    volid: str
    media: CloudInitAttachedDriveMedia

    def to_dict(self) -> dict[str, Any]:
        drive = self.drive

        volid = self.volid

        media: str = self.media

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "drive": drive,
                "volid": volid,
                "media": media,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        drive = d.pop("drive")

        volid = d.pop("volid")

        media = check_cloud_init_attached_drive_media(d.pop("media"))

        cloud_init_attached_drive = cls(
            drive=drive,
            volid=volid,
            media=media,
        )

        return cloud_init_attached_drive
