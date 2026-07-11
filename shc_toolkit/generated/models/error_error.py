from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_detail import ErrorDetail
    from ..models.error_error_links_item import ErrorErrorLinksItem


T = TypeVar("T", bound="ErrorError")


@_attrs_define
class ErrorError:
    """
    Attributes:
        code (str):  Example: validation_failed.
        message (str):  Example: Request body must be a non-empty JSON object..
        request_id (UUID):  Example: 5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
        details (list[ErrorDetail]): ALWAYS present. An array of field-level validation issues; it is an empty array []
            when there are no field-level issues (e.g. on 401/403/404/409/429/500). Detail-bearing errors (typically
            400/422) carry one ErrorDetail per offending field. A consumer can therefore read error.details unconditionally
            without an existence check.
        retry_after_seconds (int | Unset): Seconds to wait before retrying. Mirrors the `Retry-After` response header so
            an agent that reads only the body still gets the backoff. Present on 429 responses. v2.4.0: also emitted with
            registry defaults for transient error_code values (vm_locked=15, upstream_failure=30). Example: 30.
        links (list[ErrorErrorLinksItem] | Unset): Optional stable recovery relations. Lets an agent self-route after an
            error (e.g. rel=status -> the summary/poll endpoint to re-read authoritative state).
        error_code (str | Unset): v2.4.0 (additive): stable machine code from the documented registry (mirrors
            error.code, refined where the transport code is generic — e.g. a rejected key is unauthorized +
            error_code=invalid_token). Prefer matching on this over message text.
    """

    code: str
    message: str
    request_id: UUID
    details: list[ErrorDetail]
    retry_after_seconds: int | Unset = UNSET
    links: list[ErrorErrorLinksItem] | Unset = UNSET
    error_code: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        request_id = str(self.request_id)

        details = []
        for details_item_data in self.details:
            details_item = details_item_data.to_dict()
            details.append(details_item)

        retry_after_seconds = self.retry_after_seconds

        links: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()
                links.append(links_item)

        error_code = self.error_code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
                "request_id": request_id,
                "details": details,
            }
        )
        if retry_after_seconds is not UNSET:
            field_dict["retry_after_seconds"] = retry_after_seconds
        if links is not UNSET:
            field_dict["links"] = links
        if error_code is not UNSET:
            field_dict["error_code"] = error_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_detail import ErrorDetail
        from ..models.error_error_links_item import ErrorErrorLinksItem

        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        request_id = UUID(d.pop("request_id"))

        details = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = ErrorDetail.from_dict(details_item_data)

            details.append(details_item)

        retry_after_seconds = d.pop("retry_after_seconds", UNSET)

        _links = d.pop("links", UNSET)
        links: list[ErrorErrorLinksItem] | Unset = UNSET
        if _links is not UNSET:
            links = []
            for links_item_data in _links:
                links_item = ErrorErrorLinksItem.from_dict(links_item_data)

                links.append(links_item)

        error_code = d.pop("error_code", UNSET)

        error_error = cls(
            code=code,
            message=message,
            request_id=request_id,
            details=details,
            retry_after_seconds=retry_after_seconds,
            links=links,
            error_code=error_code,
        )

        return error_error
