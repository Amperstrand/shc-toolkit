from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cancel_vm_request_additional_property_type_4 import (
        CancelVmRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="CancelVmRequest")


@_attrs_define
class CancelVmRequest:
    """
    Example:
        {'reason': 'Service no longer needed after migration.', 'immediate': False}

    Attributes:
        reason (str | Unset): Optional customer-supplied cancellation note. The API trims and sanitizes this value
            before passing it to Blesta. Example: Service no longer needed after migration..
        immediate (bool | Unset): Set to `true` to cancel the service immediately. Leave unset or `false` to cancel at
            the end of the current term. Default: False.
    """

    reason: str | Unset = UNSET
    immediate: bool | Unset = False
    additional_properties: dict[
        str,
        bool
        | CancelVmRequestAdditionalPropertyType4
        | float
        | int
        | list[str]
        | None
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cancel_vm_request_additional_property_type_4 import (
            CancelVmRequestAdditionalPropertyType4,
        )

        reason = self.reason

        immediate = self.immediate

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, CancelVmRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason
        if immediate is not UNSET:
            field_dict["immediate"] = immediate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cancel_vm_request_additional_property_type_4 import (
            CancelVmRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        reason = d.pop("reason", UNSET)

        immediate = d.pop("immediate", UNSET)

        cancel_vm_request = cls(
            reason=reason,
            immediate=immediate,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                bool
                | CancelVmRequestAdditionalPropertyType4
                | float
                | int
                | list[str]
                | None
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        CancelVmRequestAdditionalPropertyType4.from_dict(data)
                    )

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_5 = cast(list[str], data)

                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(
                    bool
                    | CancelVmRequestAdditionalPropertyType4
                    | float
                    | int
                    | list[str]
                    | None
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        cancel_vm_request.additional_properties = additional_properties
        return cancel_vm_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        bool
        | CancelVmRequestAdditionalPropertyType4
        | float
        | int
        | list[str]
        | None
        | str
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: bool
        | CancelVmRequestAdditionalPropertyType4
        | float
        | int
        | list[str]
        | None
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
