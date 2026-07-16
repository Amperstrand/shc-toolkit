from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.batch_sub_request_method import BatchSubRequestMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_sub_request_body_type_0 import BatchSubRequestBodyType0
    from ..models.batch_sub_request_body_type_1_item import BatchSubRequestBodyType1Item


T = TypeVar("T", bound="BatchSubRequest")


@_attrs_define
class BatchSubRequest:
    """One staged batch sub-request. Each sub-request is authorized, confirmed, and idempotency-checked as if called
    directly.

        Example:
            {'id': 'vm-read', 'method': 'GET', 'path': '/vm/353'}

        Attributes:
            method (BatchSubRequestMethod):  Example: GET.
            path (str): Live /user-api/v2-relative path using the current v2 route convention (for example /vm, /events,
                /event-subscriptions, /account). Absolute URLs, scheme URLs, double-slash paths, and nested /batch requests are
                rejected by the native batch dispatcher. Example: /vm/353.
            id (str | Unset): Optional caller correlation id echoed in the matching sub-response. Example: step-1.
            body (BatchSubRequestBodyType0 | list[BatchSubRequestBodyType1Item] | None | Unset): Optional JSON request body
                for this sub-request. Unknown fields are validated against the target operation schema before dispatch.
            idempotency_key (str | Unset): Optional per-sub-request Idempotency-Key value. Required when the target
                operation requires idempotency. Example: 5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
            confirm (str | Unset): Optional per-sub-request X-User-Api-Confirm value for a confirmed retry. Example:
                cnf_01J2Z7QCGJ7FQ86A6W6A9A0M5X.
    """

    method: BatchSubRequestMethod
    path: str
    id: str | Unset = UNSET
    body: (
        BatchSubRequestBodyType0 | list[BatchSubRequestBodyType1Item] | None | Unset
    ) = UNSET
    idempotency_key: str | Unset = UNSET
    confirm: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_sub_request_body_type_0 import BatchSubRequestBodyType0

        method = self.method.value

        path = self.path

        id = self.id

        body: dict[str, Any] | list[dict[str, Any]] | None | Unset
        if isinstance(self.body, Unset):
            body = UNSET
        elif isinstance(self.body, BatchSubRequestBodyType0):
            body = self.body.to_dict()
        elif isinstance(self.body, list):
            body = []
            for body_type_1_item_data in self.body:
                body_type_1_item = body_type_1_item_data.to_dict()
                body.append(body_type_1_item)

        else:
            body = self.body

        idempotency_key = self.idempotency_key

        confirm = self.confirm

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "method": method,
                "path": path,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if body is not UNSET:
            field_dict["body"] = body
        if idempotency_key is not UNSET:
            field_dict["idempotencyKey"] = idempotency_key
        if confirm is not UNSET:
            field_dict["confirm"] = confirm

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_sub_request_body_type_0 import BatchSubRequestBodyType0
        from ..models.batch_sub_request_body_type_1_item import (
            BatchSubRequestBodyType1Item,
        )

        d = dict(src_dict)
        method = BatchSubRequestMethod(d.pop("method"))

        path = d.pop("path")

        id = d.pop("id", UNSET)

        def _parse_body(
            data: object,
        ) -> (
            BatchSubRequestBodyType0 | list[BatchSubRequestBodyType1Item] | None | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                body_type_0 = BatchSubRequestBodyType0.from_dict(data)

                return body_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                body_type_1 = []
                _body_type_1 = data
                for body_type_1_item_data in _body_type_1:
                    body_type_1_item = BatchSubRequestBodyType1Item.from_dict(
                        body_type_1_item_data
                    )

                    body_type_1.append(body_type_1_item)

                return body_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                BatchSubRequestBodyType0
                | list[BatchSubRequestBodyType1Item]
                | None
                | Unset,
                data,
            )

        body = _parse_body(d.pop("body", UNSET))

        idempotency_key = d.pop("idempotencyKey", UNSET)

        confirm = d.pop("confirm", UNSET)

        batch_sub_request = cls(
            method=method,
            path=path,
            id=id,
            body=body,
            idempotency_key=idempotency_key,
            confirm=confirm,
        )

        return batch_sub_request
