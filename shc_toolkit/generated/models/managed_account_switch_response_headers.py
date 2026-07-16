from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ManagedAccountSwitchResponseHeaders")


@_attrs_define
class ManagedAccountSwitchResponseHeaders:
    """
    Attributes:
        x_managed_client_id (str): Send this header on subsequent calls to act as the managed client within the approved
            areas.
    """

    x_managed_client_id: str

    def to_dict(self) -> dict[str, Any]:
        x_managed_client_id = self.x_managed_client_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "X-Managed-Client-Id": x_managed_client_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        x_managed_client_id = d.pop("X-Managed-Client-Id")

        managed_account_switch_response_headers = cls(
            x_managed_client_id=x_managed_client_id,
        )

        return managed_account_switch_response_headers
