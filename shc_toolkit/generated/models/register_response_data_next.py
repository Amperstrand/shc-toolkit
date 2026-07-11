from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterResponseDataNext")


@_attrs_define
class RegisterResponseDataNext:
    """Pointers to the next steps (catalog browse, docs).

    Attributes:
        catalog (str | Unset):  Example: /user-api/v2/ordering/catalog.
        docs (str | Unset):  Example: /user-api/docs/.
        note (str | Unset):  Example: Account is inert until a first order is placed and its invoice is paid.
            Authenticate with the api_key Bearer token, or HTTP Basic (email + password)..
    """

    catalog: str | Unset = UNSET
    docs: str | Unset = UNSET
    note: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        catalog = self.catalog

        docs = self.docs

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if docs is not UNSET:
            field_dict["docs"] = docs
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        catalog = d.pop("catalog", UNSET)

        docs = d.pop("docs", UNSET)

        note = d.pop("note", UNSET)

        register_response_data_next = cls(
            catalog=catalog,
            docs=docs,
            note=note,
        )

        register_response_data_next.additional_properties = d
        return register_response_data_next

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
