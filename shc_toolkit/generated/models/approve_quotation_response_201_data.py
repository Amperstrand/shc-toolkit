from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.approve_quotation_response_201_data_status import (
    ApproveQuotationResponse201DataStatus,
    check_approve_quotation_response_201_data_status,
)

T = TypeVar("T", bound="ApproveQuotationResponse201Data")


@_attrs_define
class ApproveQuotationResponse201Data:
    quotation_id: int
    """ Approved quotation id. """
    status: ApproveQuotationResponse201DataStatus
    """ Final quotation status. """

    def to_dict(self) -> dict[str, Any]:
        quotation_id = self.quotation_id

        status: str = self.status

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "quotation_id": quotation_id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        quotation_id = d.pop("quotation_id")

        status = check_approve_quotation_response_201_data_status(d.pop("status"))

        approve_quotation_response_201_data = cls(
            quotation_id=quotation_id,
            status=status,
        )

        return approve_quotation_response_201_data
