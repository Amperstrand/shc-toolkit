from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_ssh_key_apply_live_response_live_inject import (
    VmSshKeyApplyLiveResponseLiveInject,
)

T = TypeVar("T", bound="VmSshKeyApplyLiveResponse")


@_attrs_define
class VmSshKeyApplyLiveResponse:
    """Result of a live SSH-key inject. The live guest-exec result is best-effort and not authoritatively confirmable, so
    `live_inject` is always `attempted` (never `success`).

        Attributes:
            service_id (int):  Example: 353.
            live_inject (VmSshKeyApplyLiveResponseLiveInject):  Example: attempted.
            key_fingerprint (None | str): Server-computed SHA-256 fingerprint of the injected key (pass to DELETE
                /vm/{serviceId}/ssh-keys/live to live-remove it). Example: SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU.
    """

    service_id: int
    live_inject: VmSshKeyApplyLiveResponseLiveInject
    key_fingerprint: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        live_inject = self.live_inject.value

        key_fingerprint: None | str
        key_fingerprint = self.key_fingerprint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "live_inject": live_inject,
                "key_fingerprint": key_fingerprint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        live_inject = VmSshKeyApplyLiveResponseLiveInject(d.pop("live_inject"))

        def _parse_key_fingerprint(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        key_fingerprint = _parse_key_fingerprint(d.pop("key_fingerprint"))

        vm_ssh_key_apply_live_response = cls(
            service_id=service_id,
            live_inject=live_inject,
            key_fingerprint=key_fingerprint,
        )

        vm_ssh_key_apply_live_response.additional_properties = d
        return vm_ssh_key_apply_live_response

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
