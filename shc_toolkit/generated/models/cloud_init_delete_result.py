from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CloudInitDeleteResult")


@_attrs_define
class CloudInitDeleteResult:
    """
    Attributes:
        service_id (int):
        iso_name (str):  Example: cloud-init-seed.iso.
        storage (str):  Example: local.
        detached (bool):
        deleted (bool):
        restored_generated_cloud_init (bool):
    """

    service_id: int
    iso_name: str
    storage: str
    detached: bool
    deleted: bool
    restored_generated_cloud_init: bool

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        iso_name = self.iso_name

        storage = self.storage

        detached = self.detached

        deleted = self.deleted

        restored_generated_cloud_init = self.restored_generated_cloud_init

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "isoName": iso_name,
                "storage": storage,
                "detached": detached,
                "deleted": deleted,
                "restoredGeneratedCloudInit": restored_generated_cloud_init,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        iso_name = d.pop("isoName")

        storage = d.pop("storage")

        detached = d.pop("detached")

        deleted = d.pop("deleted")

        restored_generated_cloud_init = d.pop("restoredGeneratedCloudInit")

        cloud_init_delete_result = cls(
            service_id=service_id,
            iso_name=iso_name,
            storage=storage,
            detached=detached,
            deleted=deleted,
            restored_generated_cloud_init=restored_generated_cloud_init,
        )

        return cloud_init_delete_result
