from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.vm_standby_quote_side import VmStandbyQuoteSide


T = TypeVar("T", bound="VmStandbyPreviewResponse")


@_attrs_define
class VmStandbyPreviewResponse:
    service_id: int
    keep: VmStandbyQuoteSide
    release: VmStandbyQuoteSide
    keep_ip_delta: str
    currency: str
    period: str

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        keep = self.keep.to_dict()

        release = self.release.to_dict()

        keep_ip_delta = self.keep_ip_delta

        currency = self.currency

        period = self.period

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "keep": keep,
                "release": release,
                "keep_ip_delta": keep_ip_delta,
                "currency": currency,
                "period": period,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.vm_standby_quote_side import VmStandbyQuoteSide

        d = dict(src_dict)
        service_id = d.pop("service_id")

        keep = VmStandbyQuoteSide.from_dict(d.pop("keep"))

        release = VmStandbyQuoteSide.from_dict(d.pop("release"))

        keep_ip_delta = d.pop("keep_ip_delta")

        currency = d.pop("currency")

        period = d.pop("period")

        vm_standby_preview_response = cls(
            service_id=service_id,
            keep=keep,
            release=release,
            keep_ip_delta=keep_ip_delta,
            currency=currency,
            period=period,
        )

        return vm_standby_preview_response
