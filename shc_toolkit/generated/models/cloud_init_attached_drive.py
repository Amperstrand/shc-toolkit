from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.cloud_init_attached_drive_media import CloudInitAttachedDriveMedia

T = TypeVar("T", bound="CloudInitAttachedDrive")


@_attrs_define
class CloudInitAttachedDrive:
    """
    Attributes:
        drive (str):  Example: ide2.
        volid (str):  Example: local:iso/cloud-init-seed.iso.
        media (CloudInitAttachedDriveMedia):
    """

    drive: str
    volid: str
    media: CloudInitAttachedDriveMedia

    def to_dict(self) -> dict[str, Any]:
        drive = self.drive

        volid = self.volid

        media = self.media.value

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        drive = d.pop("drive")

        volid = d.pop("volid")

        media = CloudInitAttachedDriveMedia(d.pop("media"))

        cloud_init_attached_drive = cls(
            drive=drive,
            volid=volid,
            media=media,
        )

        return cloud_init_attached_drive
