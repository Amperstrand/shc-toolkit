from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_session_audit_record_data_additional_property_type_4 import (
        AgentSessionAuditRecordDataAdditionalPropertyType4,
    )


T = TypeVar("T", bound="AgentSessionAuditRecordData")


@_attrs_define
class AgentSessionAuditRecordData:
    """Includes tamperEvidence when the audit row carries prevEventHash and eventHash."""

    additional_properties: dict[
        str,
        AgentSessionAuditRecordDataAdditionalPropertyType4
        | bool
        | float
        | int
        | list[str]
        | None
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_session_audit_record_data_additional_property_type_4 import (
            AgentSessionAuditRecordDataAdditionalPropertyType4,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, AgentSessionAuditRecordDataAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_session_audit_record_data_additional_property_type_4 import (
            AgentSessionAuditRecordDataAdditionalPropertyType4,
        )

        d = dict(src_dict)
        agent_session_audit_record_data = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                AgentSessionAuditRecordDataAdditionalPropertyType4
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
                        AgentSessionAuditRecordDataAdditionalPropertyType4.from_dict(
                            data
                        )
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
                    AgentSessionAuditRecordDataAdditionalPropertyType4
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

        agent_session_audit_record_data.additional_properties = additional_properties
        return agent_session_audit_record_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        AgentSessionAuditRecordDataAdditionalPropertyType4
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
        value: AgentSessionAuditRecordDataAdditionalPropertyType4
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
