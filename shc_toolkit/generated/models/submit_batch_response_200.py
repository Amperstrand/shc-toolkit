from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.batch_sub_response import BatchSubResponse


T = TypeVar("T", bound="SubmitBatchResponse200")


@_attrs_define
class SubmitBatchResponse200:
    """
    Attributes:
        data (list[BatchSubResponse]): Ordered array of batch sub-responses. Partial failures are represented by per-
            item status/error values; successful siblings are not rolled back.
    """

    data: list[BatchSubResponse]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for componentsschemas_batch_response_item_data in self.data:
            componentsschemas_batch_response_item = (
                componentsschemas_batch_response_item_data.to_dict()
            )
            data.append(componentsschemas_batch_response_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_sub_response import BatchSubResponse

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for componentsschemas_batch_response_item_data in _data:
            componentsschemas_batch_response_item = BatchSubResponse.from_dict(
                componentsschemas_batch_response_item_data
            )

            data.append(componentsschemas_batch_response_item)

        submit_batch_response_200 = cls(
            data=data,
        )

        return submit_batch_response_200
