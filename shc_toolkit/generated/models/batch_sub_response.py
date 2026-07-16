from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_sub_response_body_type_0 import BatchSubResponseBodyType0
    from ..models.batch_sub_response_body_type_1_item import (
        BatchSubResponseBodyType1Item,
    )
    from ..models.batch_sub_response_headers import BatchSubResponseHeaders
    from ..models.problem import Problem


T = TypeVar("T", bound="BatchSubResponse")


@_attrs_define
class BatchSubResponse:
    """One batch sub-response, returned in the same array position as its sub-request.

    Attributes:
        id (None | str):  Example: vm-read.
        status (int):  Example: 200.
        headers (BatchSubResponseHeaders): Selected public response headers for this sub-response. Example: {'X-Request-
            Id': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}.
        body (BatchSubResponseBodyType0 | list[BatchSubResponseBodyType1Item] | None | Unset): Success body for this
            sub-response when the target operation succeeds.
        error (Problem | Unset): RFC 9457 problem detail envelope. Error responses use application/problem+json only.
    """

    id: None | str
    status: int
    headers: BatchSubResponseHeaders
    body: (
        BatchSubResponseBodyType0 | list[BatchSubResponseBodyType1Item] | None | Unset
    ) = UNSET
    error: Problem | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_sub_response_body_type_0 import BatchSubResponseBodyType0

        id: None | str
        id = self.id

        status = self.status

        headers = self.headers.to_dict()

        body: dict[str, Any] | list[dict[str, Any]] | None | Unset
        if isinstance(self.body, Unset):
            body = UNSET
        elif isinstance(self.body, BatchSubResponseBodyType0):
            body = self.body.to_dict()
        elif isinstance(self.body, list):
            body = []
            for body_type_1_item_data in self.body:
                body_type_1_item = body_type_1_item_data.to_dict()
                body.append(body_type_1_item)

        else:
            body = self.body

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "status": status,
                "headers": headers,
            }
        )
        if body is not UNSET:
            field_dict["body"] = body
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_sub_response_body_type_0 import BatchSubResponseBodyType0
        from ..models.batch_sub_response_body_type_1_item import (
            BatchSubResponseBodyType1Item,
        )
        from ..models.batch_sub_response_headers import BatchSubResponseHeaders
        from ..models.problem import Problem

        d = dict(src_dict)

        def _parse_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        id = _parse_id(d.pop("id"))

        status = d.pop("status")

        headers = BatchSubResponseHeaders.from_dict(d.pop("headers"))

        def _parse_body(
            data: object,
        ) -> (
            BatchSubResponseBodyType0
            | list[BatchSubResponseBodyType1Item]
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                body_type_0 = BatchSubResponseBodyType0.from_dict(data)

                return body_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                body_type_1 = []
                _body_type_1 = data
                for body_type_1_item_data in _body_type_1:
                    body_type_1_item = BatchSubResponseBodyType1Item.from_dict(
                        body_type_1_item_data
                    )

                    body_type_1.append(body_type_1_item)

                return body_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BatchSubResponseBodyType0
                | list[BatchSubResponseBodyType1Item]
                | None
                | Unset,
                data,
            )

        body = _parse_body(d.pop("body", UNSET))

        _error = d.pop("error", UNSET)
        error: Problem | Unset
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = Problem.from_dict(_error)

        batch_sub_response = cls(
            id=id,
            status=status,
            headers=headers,
            body=body,
            error=error,
        )

        return batch_sub_response
