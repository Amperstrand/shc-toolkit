from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApproveQuotationBody")


@_attrs_define
class ApproveQuotationBody:
    """
    Attributes:
        return_url (str | Unset):
        cancel_url (str | Unset):
    """

    return_url: str | Unset = UNSET
    cancel_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        return_url = self.return_url

        cancel_url = self.cancel_url

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if return_url is not UNSET:
            field_dict["returnUrl"] = return_url
        if cancel_url is not UNSET:
            field_dict["cancelUrl"] = cancel_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        return_url = d.pop("returnUrl", UNSET)

        cancel_url = d.pop("cancelUrl", UNSET)

        approve_quotation_body = cls(
            return_url=return_url,
            cancel_url=cancel_url,
        )

        return approve_quotation_body
