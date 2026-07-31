from typing import Literal

LintFindingSeverity = Literal["error", "info", "warning"]

LINT_FINDING_SEVERITY_VALUES: set[LintFindingSeverity] = {
    "error",
    "info",
    "warning",
}


def check_lint_finding_severity(value: str) -> LintFindingSeverity:
    if value in LINT_FINDING_SEVERITY_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LINT_FINDING_SEVERITY_VALUES!r}"
    )
