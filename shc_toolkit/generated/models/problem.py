from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

from ..models.problem_x_error_code import ProblemXErrorCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_recovery import AgentRecovery
    from ..models.links import Links
    from ..models.lint_report import LintReport
    from ..models.problem_field_error import ProblemFieldError


T = TypeVar("T", bound="Problem")


@_attrs_define
class Problem:
    """RFC 9457 problem detail envelope. Error responses use application/problem+json only.

    Attributes:
        type_ (str):  Example: https://api.sovereignhybridcompute.com/problems/v3/validation-failed.
        title (str):  Example: Validation Failed.
        status (int):  Example: 422.
        detail (str):  Example: One or more typed field errors were found..
        instance (str):  Example: /user-api/v3/problems/5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
        x_error_code (ProblemXErrorCode):  Example: validation_failed.
        request_id (UUID | Unset):  Example: 5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
        field_errors (list[ProblemFieldError] | Unset):
        retry_after_seconds (int | Unset):  Example: 30.
        retryable (bool | Unset):  Example: True.
        links (Links | Unset): Hypermedia links keyed by IANA-registered link relation names.
        lint_report (LintReport | Unset):
        x_shc_agent_recovery (AgentRecovery | Unset): Machine-readable next action for agents after an error.
    """

    type_: str
    title: str
    status: int
    detail: str
    instance: str
    x_error_code: ProblemXErrorCode
    request_id: UUID | Unset = UNSET
    field_errors: list[ProblemFieldError] | Unset = UNSET
    retry_after_seconds: int | Unset = UNSET
    retryable: bool | Unset = UNSET
    links: Links | Unset = UNSET
    lint_report: LintReport | Unset = UNSET
    x_shc_agent_recovery: AgentRecovery | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        status = self.status

        detail = self.detail

        instance = self.instance

        x_error_code = self.x_error_code.value

        request_id: str | Unset = UNSET
        if not isinstance(self.request_id, Unset):
            request_id = str(self.request_id)

        field_errors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.field_errors, Unset):
            field_errors = []
            for field_errors_item_data in self.field_errors:
                field_errors_item = field_errors_item_data.to_dict()
                field_errors.append(field_errors_item)

        retry_after_seconds = self.retry_after_seconds

        retryable = self.retryable

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        lint_report: dict[str, Any] | Unset = UNSET
        if not isinstance(self.lint_report, Unset):
            lint_report = self.lint_report.to_dict()

        x_shc_agent_recovery: dict[str, Any] | Unset = UNSET
        if not isinstance(self.x_shc_agent_recovery, Unset):
            x_shc_agent_recovery = self.x_shc_agent_recovery.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "title": title,
                "status": status,
                "detail": detail,
                "instance": instance,
                "x-error-code": x_error_code,
            }
        )
        if request_id is not UNSET:
            field_dict["requestId"] = request_id
        if field_errors is not UNSET:
            field_dict["fieldErrors"] = field_errors
        if retry_after_seconds is not UNSET:
            field_dict["retryAfterSeconds"] = retry_after_seconds
        if retryable is not UNSET:
            field_dict["retryable"] = retryable
        if links is not UNSET:
            field_dict["links"] = links
        if lint_report is not UNSET:
            field_dict["lintReport"] = lint_report
        if x_shc_agent_recovery is not UNSET:
            field_dict["x-shc-agent-recovery"] = x_shc_agent_recovery

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_recovery import AgentRecovery
        from ..models.links import Links
        from ..models.lint_report import LintReport
        from ..models.problem_field_error import ProblemFieldError

        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        status = d.pop("status")

        detail = d.pop("detail")

        instance = d.pop("instance")

        x_error_code = ProblemXErrorCode(d.pop("x-error-code"))

        _request_id = d.pop("requestId", UNSET)
        request_id: UUID | Unset
        if isinstance(_request_id, Unset):
            request_id = UNSET
        else:
            request_id = UUID(_request_id)

        _field_errors = d.pop("fieldErrors", UNSET)
        field_errors: list[ProblemFieldError] | Unset = UNSET
        if _field_errors is not UNSET:
            field_errors = []
            for field_errors_item_data in _field_errors:
                field_errors_item = ProblemFieldError.from_dict(field_errors_item_data)

                field_errors.append(field_errors_item)

        retry_after_seconds = d.pop("retryAfterSeconds", UNSET)

        retryable = d.pop("retryable", UNSET)

        _links = d.pop("links", UNSET)
        links: Links | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = Links.from_dict(_links)

        _lint_report = d.pop("lintReport", UNSET)
        lint_report: LintReport | Unset
        if isinstance(_lint_report, Unset):
            lint_report = UNSET
        else:
            lint_report = LintReport.from_dict(_lint_report)

        _x_shc_agent_recovery = d.pop("x-shc-agent-recovery", UNSET)
        x_shc_agent_recovery: AgentRecovery | Unset
        if isinstance(_x_shc_agent_recovery, Unset):
            x_shc_agent_recovery = UNSET
        else:
            x_shc_agent_recovery = AgentRecovery.from_dict(_x_shc_agent_recovery)

        problem = cls(
            type_=type_,
            title=title,
            status=status,
            detail=detail,
            instance=instance,
            x_error_code=x_error_code,
            request_id=request_id,
            field_errors=field_errors,
            retry_after_seconds=retry_after_seconds,
            retryable=retryable,
            links=links,
            lint_report=lint_report,
            x_shc_agent_recovery=x_shc_agent_recovery,
        )

        return problem
