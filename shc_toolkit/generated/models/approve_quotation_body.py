from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.approve_quotation_body_additional_property_type_4 import (
        ApproveQuotationBodyAdditionalPropertyType4,
    )


T = TypeVar("T", bound="ApproveQuotationBody")


@_attrs_define
class ApproveQuotationBody:
    """
    Attributes:
        idempotency_key (str): Replay key required by the live route body idempotency gate.
    """

    idempotency_key: str
    additional_properties: dict[
        str,
        ApproveQuotationBodyAdditionalPropertyType4
        | bool
        | float
        | int
        | list[str]
        | None
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.approve_quotation_body_additional_property_type_4 import (
            ApproveQuotationBodyAdditionalPropertyType4,
        )

        idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ApproveQuotationBodyAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "idempotency_key": idempotency_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.approve_quotation_body_additional_property_type_4 import (
            ApproveQuotationBodyAdditionalPropertyType4,
        )

        d = dict(src_dict)
        idempotency_key = d.pop("idempotency_key")

        approve_quotation_body = cls(
            idempotency_key=idempotency_key,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                ApproveQuotationBodyAdditionalPropertyType4
                | bool
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
                        ApproveQuotationBodyAdditionalPropertyType4.from_dict(data)
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
                    ApproveQuotationBodyAdditionalPropertyType4
                    | bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        approve_quotation_body.additional_properties = additional_properties
        return approve_quotation_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        ApproveQuotationBodyAdditionalPropertyType4
        | bool
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
        value: ApproveQuotationBodyAdditionalPropertyType4
        | bool
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
