from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitVirtualMachineRenewalBody")


@_attrs_define
class SubmitVirtualMachineRenewalBody:
    """
    Attributes:
        idempotency_key (str): Client-chosen idempotency key; replays return the original result.
        pricing_id (int | Unset): Optional target term (package_pricing id) to renew into; requires the account to allow
            term changes. Omit to renew the current term.
    """

    idempotency_key: str
    pricing_id: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        idempotency_key = self.idempotency_key

        pricing_id = self.pricing_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "idempotency_key": idempotency_key,
            }
        )
        if pricing_id is not UNSET:
            field_dict["pricing_id"] = pricing_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        idempotency_key = d.pop("idempotency_key")

        pricing_id = d.pop("pricing_id", UNSET)

        submit_virtual_machine_renewal_body = cls(
            idempotency_key=idempotency_key,
            pricing_id=pricing_id,
        )

        return submit_virtual_machine_renewal_body
