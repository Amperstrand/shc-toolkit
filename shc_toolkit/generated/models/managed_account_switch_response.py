from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.managed_account_switch_response_audit import (
        ManagedAccountSwitchResponseAudit,
    )
    from ..models.managed_account_switch_response_headers import (
        ManagedAccountSwitchResponseHeaders,
    )


T = TypeVar("T", bound="ManagedAccountSwitchResponse")


@_attrs_define
class ManagedAccountSwitchResponse:
    """
    Attributes:
        switched (bool): True when the act-as context is available.
        acting_client_id (int): Authenticated manager client id.
        effective_client_id (int): Managed client id to send in X-Managed-Client-Id on later requests.
        managed_client_id (int): Alias of effective_client_id for callers that model this as the path id.
        areas (list[str]): Effective areas approved for this switch. This is never a superset of the request or the
            Blesta grant.
        same_company (bool): True after same-company enforcement succeeds.
        headers (ManagedAccountSwitchResponseHeaders):
        audit (ManagedAccountSwitchResponseAudit): Indicates that dual-identity audit fields were recorded for this
            switch.
    """

    switched: bool
    acting_client_id: int
    effective_client_id: int
    managed_client_id: int
    areas: list[str]
    same_company: bool
    headers: ManagedAccountSwitchResponseHeaders
    audit: ManagedAccountSwitchResponseAudit

    def to_dict(self) -> dict[str, Any]:
        switched = self.switched

        acting_client_id = self.acting_client_id

        effective_client_id = self.effective_client_id

        managed_client_id = self.managed_client_id

        areas = self.areas

        same_company = self.same_company

        headers = self.headers.to_dict()

        audit = self.audit.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "switched": switched,
                "acting_client_id": acting_client_id,
                "effective_client_id": effective_client_id,
                "managed_client_id": managed_client_id,
                "areas": areas,
                "same_company": same_company,
                "headers": headers,
                "audit": audit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_account_switch_response_audit import (
            ManagedAccountSwitchResponseAudit,
        )
        from ..models.managed_account_switch_response_headers import (
            ManagedAccountSwitchResponseHeaders,
        )

        d = dict(src_dict)
        switched = d.pop("switched")

        acting_client_id = d.pop("acting_client_id")

        effective_client_id = d.pop("effective_client_id")

        managed_client_id = d.pop("managed_client_id")

        areas = cast(list[str], d.pop("areas"))

        same_company = d.pop("same_company")

        headers = ManagedAccountSwitchResponseHeaders.from_dict(d.pop("headers"))

        audit = ManagedAccountSwitchResponseAudit.from_dict(d.pop("audit"))

        managed_account_switch_response = cls(
            switched=switched,
            acting_client_id=acting_client_id,
            effective_client_id=effective_client_id,
            managed_client_id=managed_client_id,
            areas=areas,
            same_company=same_company,
            headers=headers,
            audit=audit,
        )

        return managed_account_switch_response
