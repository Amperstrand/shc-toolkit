from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.permission_options_envelope import PermissionOptionsEnvelope


T = TypeVar("T", bound="GetManagerPermissionOptionsResponse200")


@_attrs_define
class GetManagerPermissionOptionsResponse200:
    """
    Attributes:
        data (PermissionOptionsEnvelope): Vocabulary of permission areas that may be granted to a contact or account
            manager, as key/label pairs. Returned by GET /contacts/permission-options and GET /managers/permission-options
            (the manager vocabulary is the contact vocabulary minus the _managed area).
    """

    data: PermissionOptionsEnvelope

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission_options_envelope import PermissionOptionsEnvelope

        d = dict(src_dict)
        data = PermissionOptionsEnvelope.from_dict(d.pop("data"))

        get_manager_permission_options_response_200 = cls(
            data=data,
        )

        return get_manager_permission_options_response_200
