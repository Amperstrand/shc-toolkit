from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_init_derived_seed import CloudInitDerivedSeed
    from ..models.lint_report import LintReport


T = TypeVar("T", bound="CloudInitValidateResult")


@_attrs_define
class CloudInitValidateResult:
    """
    Attributes:
        service_id (int):
        accepted (bool):
        lint_report (LintReport):
        derived (CloudInitDerivedSeed):
    """

    service_id: int
    accepted: bool
    lint_report: LintReport
    derived: CloudInitDerivedSeed

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        accepted = self.accepted

        lint_report = self.lint_report.to_dict()

        derived = self.derived.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "accepted": accepted,
                "lintReport": lint_report,
                "derived": derived,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_init_derived_seed import CloudInitDerivedSeed
        from ..models.lint_report import LintReport

        d = dict(src_dict)
        service_id = d.pop("service_id")

        accepted = d.pop("accepted")

        lint_report = LintReport.from_dict(d.pop("lintReport"))

        derived = CloudInitDerivedSeed.from_dict(d.pop("derived"))

        cloud_init_validate_result = cls(
            service_id=service_id,
            accepted=accepted,
            lint_report=lint_report,
            derived=derived,
        )

        return cloud_init_validate_result
