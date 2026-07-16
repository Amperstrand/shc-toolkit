from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_ssh_key_apply_live_request_additional_property_type_4 import (
        VmSshKeyApplyLiveRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmSshKeyApplyLiveRequest")


@_attrs_define
class VmSshKeyApplyLiveRequest:
    """Live-inject a single-line SSH public key into the running VM via the guest agent. The key is also persisted so a
    later reinstall keeps it.

        Example:
            {'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}

        Attributes:
            ssh_key (str): Single-line ssh-rsa, ssh-ed25519, or ecdsa-sha2-nistp256/384/521 public key. Example: ssh-ed25519
                AAAAC3NzaC1lZDI1NTE5AAAA... user@host.
    """

    ssh_key: str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmSshKeyApplyLiveRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_ssh_key_apply_live_request_additional_property_type_4 import (
            VmSshKeyApplyLiveRequestAdditionalPropertyType4,
        )

        ssh_key = self.ssh_key

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmSshKeyApplyLiveRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "ssh_key": ssh_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_ssh_key_apply_live_request_additional_property_type_4 import (
            VmSshKeyApplyLiveRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        ssh_key = d.pop("ssh_key")

        vm_ssh_key_apply_live_request = cls(
            ssh_key=ssh_key,
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
                | VmSshKeyApplyLiveRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmSshKeyApplyLiveRequestAdditionalPropertyType4.from_dict(data)
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
                    | VmSshKeyApplyLiveRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_ssh_key_apply_live_request.additional_properties = additional_properties
        return vm_ssh_key_apply_live_request

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
        | VmSshKeyApplyLiveRequestAdditionalPropertyType4
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
        | VmSshKeyApplyLiveRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
