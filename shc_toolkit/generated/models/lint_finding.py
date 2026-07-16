from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.lint_finding_severity import LintFindingSeverity

T = TypeVar("T", bound="LintFinding")


@_attrs_define
class LintFinding:
    """
    Attributes:
        severity (LintFindingSeverity):  Example: error.
        rule_id (str):  Example: cloud-init.runcmd.remote-shell.
        message (str):  Example: runcmd must not pipe remote content into a shell..
        location (None | str): Structural locator only: JSON Pointer or YAML path to the offending node. The value must
            not contain source text. Example: /runcmd/0.
    """

    severity: LintFindingSeverity
    rule_id: str
    message: str
    location: None | str

    def to_dict(self) -> dict[str, Any]:
        severity = self.severity.value

        rule_id = self.rule_id

        message = self.message

        location: None | str
        location = self.location

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "severity": severity,
                "ruleId": rule_id,
                "message": message,
                "location": location,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        severity = LintFindingSeverity(d.pop("severity"))

        rule_id = d.pop("ruleId")

        message = d.pop("message")

        def _parse_location(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        location = _parse_location(d.pop("location"))

        lint_finding = cls(
            severity=severity,
            rule_id=rule_id,
            message=message,
            location=location,
        )

        return lint_finding
