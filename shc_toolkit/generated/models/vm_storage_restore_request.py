from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_storage_restore_request_additional_property_type_4 import (
        VmStorageRestoreRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmStorageRestoreRequest")


@_attrs_define
class VmStorageRestoreRequest:
    """v2.4.0: exactly one of backup_id | snapshot_id | id | volid is required (aliases, first present wins).

    Example:
        {'backup_id': 'bk_6ERwSd_PLY66FW72VFM'}

    Attributes:
        backup_id (str | Unset): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the
            real storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        encryption_key (str | Unset): Reserved — client-side backup encryption is not yet available; a non-empty value
            returns 501.
        snapshot_id (str | Unset): v2.4.0 alias of backup_id (accepted on input).
        id (str | Unset): v2.4.0 alias of backup_id (accepted on input).
    """

    backup_id: str | Unset = UNSET
    encryption_key: str | Unset = UNSET
    snapshot_id: str | Unset = UNSET
    id: str | Unset = UNSET
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmStorageRestoreRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_storage_restore_request_additional_property_type_4 import (
            VmStorageRestoreRequestAdditionalPropertyType4,
        )

        backup_id = self.backup_id

        encryption_key = self.encryption_key

        snapshot_id = self.snapshot_id

        id = self.id

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmStorageRestoreRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})
        if backup_id is not UNSET:
            field_dict["backup_id"] = backup_id
        if encryption_key is not UNSET:
            field_dict["encryption_key"] = encryption_key
        if snapshot_id is not UNSET:
            field_dict["snapshot_id"] = snapshot_id
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_storage_restore_request_additional_property_type_4 import (
            VmStorageRestoreRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        backup_id = d.pop("backup_id", UNSET)

        encryption_key = d.pop("encryption_key", UNSET)

        snapshot_id = d.pop("snapshot_id", UNSET)

        id = d.pop("id", UNSET)

        vm_storage_restore_request = cls(
            backup_id=backup_id,
            encryption_key=encryption_key,
            snapshot_id=snapshot_id,
            id=id,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                bool
                | float
                | int
                | list[str]
                | None
                | str
                | VmStorageRestoreRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmStorageRestoreRequestAdditionalPropertyType4.from_dict(data)
                    )

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_5 = cast(list[str], data)

                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(
                    bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str
                    | VmStorageRestoreRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_storage_restore_request.additional_properties = additional_properties
        return vm_storage_restore_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmStorageRestoreRequestAdditionalPropertyType4
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmStorageRestoreRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
