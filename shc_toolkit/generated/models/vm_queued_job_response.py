from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.next_poll import NextPoll


T = TypeVar("T", bound="VmQueuedJobResponse")


@_attrs_define
class VmQueuedJobResponse:
    """Queued backup, snapshot, or restore job response.

    Example:
        {'service_id': 353, 'job_id': 912, 'type': 'backup', 'source': None, 'backup_id': None, 'name': 'nightly-demo',
            'mode': 'suspend', 'description': None, 'message': 'Backup queued successfully.'}

    Attributes:
        service_id (int):  Example: 353.
        job_id (int):  Example: 912.
        type_ (str):  Example: backup.
        message (str):  Example: Backup queued successfully..
        source (None | str | Unset):
        backup_id (str | Unset): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the
            real storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        name (None | str | Unset):  Example: nightly-demo.
        mode (None | str | Unset):  Example: suspend.
        description (None | str | Unset):
        next_ (NextPoll | Unset): Poll pointer for an async (queued-job) producer.
    """

    service_id: int
    job_id: int
    type_: str
    message: str
    source: None | str | Unset = UNSET
    backup_id: str | Unset = UNSET
    name: None | str | Unset = UNSET
    mode: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    next_: NextPoll | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        job_id = self.job_id

        type_ = self.type_

        message = self.message

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        backup_id = self.backup_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        mode: None | str | Unset
        if isinstance(self.mode, Unset):
            mode = UNSET
        else:
            mode = self.mode

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "job_id": job_id,
                "type": type_,
                "message": message,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if backup_id is not UNSET:
            field_dict["backup_id"] = backup_id
        if name is not UNSET:
            field_dict["name"] = name
        if mode is not UNSET:
            field_dict["mode"] = mode
        if description is not UNSET:
            field_dict["description"] = description
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.next_poll import NextPoll

        d = dict(src_dict)
        service_id = d.pop("service_id")

        job_id = d.pop("job_id")

        type_ = d.pop("type")

        message = d.pop("message")

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        backup_id = d.pop("backup_id", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_mode(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        mode = _parse_mode(d.pop("mode", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _next_ = d.pop("next", UNSET)
        next_: NextPoll | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = NextPoll.from_dict(_next_)

        vm_queued_job_response = cls(
            service_id=service_id,
            job_id=job_id,
            type_=type_,
            message=message,
            source=source,
            backup_id=backup_id,
            name=name,
            mode=mode,
            description=description,
            next_=next_,
        )

        vm_queued_job_response.additional_properties = d
        return vm_queued_job_response

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
