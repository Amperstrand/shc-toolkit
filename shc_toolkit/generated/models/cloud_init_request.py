from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CloudInitRequest")


@_attrs_define
class CloudInitRequest:
    r"""
    Example:
        {'cloudInit': '#cloud-config\npackage_update: true\n'}

    Attributes:
        cloud_init (str): Customer-supplied #cloud-config content only. Filenames, paths, storage names, node paths, ISO
            names, and shell fragments are never accepted from the request. Example: #cloud-config
            package_update: true
            .
    """

    cloud_init: str

    def to_dict(self) -> dict[str, Any]:
        cloud_init = self.cloud_init

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cloudInit": cloud_init,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cloud_init = d.pop("cloudInit")

        cloud_init_request = cls(
            cloud_init=cloud_init,
        )

        return cloud_init_request
