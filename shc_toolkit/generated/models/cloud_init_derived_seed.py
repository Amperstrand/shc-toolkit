from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.cloud_init_derived_seed_volume_label import (
    CloudInitDerivedSeedVolumeLabel,
)

T = TypeVar("T", bound="CloudInitDerivedSeed")


@_attrs_define
class CloudInitDerivedSeed:
    """
    Attributes:
        iso_name (str):  Example: cloud-init-seed.iso.
        volume_label (CloudInitDerivedSeedVolumeLabel):
    """

    iso_name: str
    volume_label: CloudInitDerivedSeedVolumeLabel

    def to_dict(self) -> dict[str, Any]:
        iso_name = self.iso_name

        volume_label = self.volume_label.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "isoName": iso_name,
                "volumeLabel": volume_label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        iso_name = d.pop("isoName")

        volume_label = CloudInitDerivedSeedVolumeLabel(d.pop("volumeLabel"))

        cloud_init_derived_seed = cls(
            iso_name=iso_name,
            volume_label=volume_label,
        )

        return cloud_init_derived_seed
