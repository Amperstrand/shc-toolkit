from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.lint_finding import LintFinding


T = TypeVar("T", bound="LintReport")


@_attrs_define
class LintReport:
    """
    Attributes:
        accepted (bool):
        findings (list[LintFinding]):
        normalized_size (int):  Example: 82.
    """

    accepted: bool
    findings: list[LintFinding]
    normalized_size: int

    def to_dict(self) -> dict[str, Any]:
        accepted = self.accepted

        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)

        normalized_size = self.normalized_size

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "accepted": accepted,
                "findings": findings,
                "normalizedSize": normalized_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lint_finding import LintFinding

        d = dict(src_dict)
        accepted = d.pop("accepted")

        findings = []
        _findings = d.pop("findings")
        for findings_item_data in _findings:
            findings_item = LintFinding.from_dict(findings_item_data)

            findings.append(findings_item)

        normalized_size = d.pop("normalizedSize")

        lint_report = cls(
            accepted=accepted,
            findings=findings,
            normalized_size=normalized_size,
        )

        return lint_report
