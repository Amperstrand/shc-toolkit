from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.preview_service_addon_body_config_options import (
        PreviewServiceAddonBodyConfigOptions,
    )
    from ..models.preview_service_addon_body_fields import PreviewServiceAddonBodyFields


T = TypeVar("T", bound="PreviewServiceAddonBody")


@_attrs_define
class PreviewServiceAddonBody:
    """
    Attributes:
        package_group_id (int): The addon package group (from /addons/options).
        pricing_id (int): The addon package pricing id (selects package + term).
        qty (int | Unset):  Default: 1.
        config_options (PreviewServiceAddonBodyConfigOptions | Unset): Map of package option id -> selected value.
        fields (PreviewServiceAddonBodyFields | Unset): Module service fields for the addon, when the addon module
            requires any.
    """

    package_group_id: int
    pricing_id: int
    qty: int | Unset = 1
    config_options: PreviewServiceAddonBodyConfigOptions | Unset = UNSET
    fields: PreviewServiceAddonBodyFields | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        package_group_id = self.package_group_id

        pricing_id = self.pricing_id

        qty = self.qty

        config_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_options, Unset):
            config_options = self.config_options.to_dict()

        fields: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "package_group_id": package_group_id,
                "pricing_id": pricing_id,
            }
        )
        if qty is not UNSET:
            field_dict["qty"] = qty
        if config_options is not UNSET:
            field_dict["config_options"] = config_options
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.preview_service_addon_body_config_options import (
            PreviewServiceAddonBodyConfigOptions,
        )
        from ..models.preview_service_addon_body_fields import (
            PreviewServiceAddonBodyFields,
        )

        d = dict(src_dict)
        package_group_id = d.pop("package_group_id")

        pricing_id = d.pop("pricing_id")

        qty = d.pop("qty", UNSET)

        _config_options = d.pop("config_options", UNSET)
        config_options: PreviewServiceAddonBodyConfigOptions | Unset
        if isinstance(_config_options, Unset):
            config_options = UNSET
        else:
            config_options = PreviewServiceAddonBodyConfigOptions.from_dict(
                _config_options
            )

        _fields = d.pop("fields", UNSET)
        fields: PreviewServiceAddonBodyFields | Unset
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = PreviewServiceAddonBodyFields.from_dict(_fields)

        preview_service_addon_body = cls(
            package_group_id=package_group_id,
            pricing_id=pricing_id,
            qty=qty,
            config_options=config_options,
            fields=fields,
        )

        return preview_service_addon_body
