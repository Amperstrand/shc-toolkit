from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.link_target_method import LinkTargetMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkTarget")


@_attrs_define
class LinkTarget:
    """Typed hypermedia target. Relation names are carried by the containing Links object and use IANA-registered rels.

    Attributes:
        href (str):  Example: /user-api/v3/virtual-machines/353/jobs/912.
        method (LinkTargetMethod | Unset):  Example: GET.
        path (str | Unset):  Example: /virtual-machines/353/jobs/912.
        operation_id (str | Unset):  Example: getVirtualMachineJob.
        description (str | Unset):  Example: Poll job status..
    """

    href: str
    method: LinkTargetMethod | Unset = UNSET
    path: str | Unset = UNSET
    operation_id: str | Unset = UNSET
    description: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        path = self.path

        operation_id = self.operation_id

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "href": href,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if path is not UNSET:
            field_dict["path"] = path
        if operation_id is not UNSET:
            field_dict["operationId"] = operation_id
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        href = d.pop("href")

        _method = d.pop("method", UNSET)
        method: LinkTargetMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = LinkTargetMethod(_method)

        path = d.pop("path", UNSET)

        operation_id = d.pop("operationId", UNSET)

        description = d.pop("description", UNSET)

        link_target = cls(
            href=href,
            method=method,
            path=path,
            operation_id=operation_id,
            description=description,
        )

        return link_target
