from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_upgrade_request_config_options import VmUpgradeRequestConfigOptions


T = TypeVar("T", bound="VmUpgradeRequest")


@_attrs_define
class VmUpgradeRequest:
    """Target pricing_ref + optional config_options + the REQUIRED idempotency_key. v2.4.0: one of pricing_ref | pricing_id
    is required (aliases; pricing_ref wins if both sent).

        Example:
            {'pricing_ref': '58', 'config_options': {'142': '64'}, 'idempotency_key':
                '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}

        Attributes:
            idempotency_key (str): REQUIRED. Service-scoped idempotency key (a missing key returns 400). Reuse the same
                value with the same body to replay the original 202 for this service. Example:
                5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
            pricing_ref (int | str | Unset): Raw package_pricing.id (same-group, client-allowable, same billing term).
                Example: 58.
            config_options (VmUpgradeRequestConfigOptions | Unset): Map of package option id (string) -> selected value
                (validated identically to ordering). Example: {'142': '64'}.
            pricing_id (int | Unset): v2.4.0 alias (additive): synonym of pricing_ref (the RAW package_pricing.id, the same
                id the ordering catalog calls pricing_id). pricing_ref wins if both are sent.
    """

    idempotency_key: str
    pricing_ref: int | str | Unset = UNSET
    config_options: VmUpgradeRequestConfigOptions | Unset = UNSET
    pricing_id: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        idempotency_key = self.idempotency_key

        pricing_ref: int | str | Unset
        if isinstance(self.pricing_ref, Unset):
            pricing_ref = UNSET
        else:
            pricing_ref = self.pricing_ref

        config_options: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_options, Unset):
            config_options = self.config_options.to_dict()

        pricing_id = self.pricing_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "idempotency_key": idempotency_key,
            }
        )
        if pricing_ref is not UNSET:
            field_dict["pricing_ref"] = pricing_ref
        if config_options is not UNSET:
            field_dict["config_options"] = config_options
        if pricing_id is not UNSET:
            field_dict["pricing_id"] = pricing_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgrade_request_config_options import (
            VmUpgradeRequestConfigOptions,
        )

        d = dict(src_dict)
        idempotency_key = d.pop("idempotency_key")

        def _parse_pricing_ref(data: object) -> int | str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(int | str | Unset, data)

        pricing_ref = _parse_pricing_ref(d.pop("pricing_ref", UNSET))

        _config_options = d.pop("config_options", UNSET)
        config_options: VmUpgradeRequestConfigOptions | Unset
        if isinstance(_config_options, Unset):
            config_options = UNSET
        else:
            config_options = VmUpgradeRequestConfigOptions.from_dict(_config_options)

        pricing_id = d.pop("pricing_id", UNSET)

        vm_upgrade_request = cls(
            idempotency_key=idempotency_key,
            pricing_ref=pricing_ref,
            config_options=config_options,
            pricing_id=pricing_id,
        )

        vm_upgrade_request.additional_properties = d
        return vm_upgrade_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
