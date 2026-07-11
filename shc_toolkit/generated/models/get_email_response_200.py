from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.email_detail import EmailDetail


T = TypeVar("T", bound="GetEmailResponse200")


@_attrs_define
class GetEmailResponse200:
    """
    Attributes:
        data (EmailDetail): Customer-safe email / notice detail with full body.
    """

    data: EmailDetail

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
        from ..models.email_detail import EmailDetail

        d = dict(src_dict)
        data = EmailDetail.from_dict(d.pop("data"))

        get_email_response_200 = cls(
            data=data,
        )

        return get_email_response_200
