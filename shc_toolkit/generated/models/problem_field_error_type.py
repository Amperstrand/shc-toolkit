from typing import Literal

ProblemFieldErrorType = Literal["field"]

PROBLEM_FIELD_ERROR_TYPE_VALUES: set[ProblemFieldErrorType] = {
    "field",
}


def check_problem_field_error_type(value: str) -> ProblemFieldErrorType:
    if value in PROBLEM_FIELD_ERROR_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROBLEM_FIELD_ERROR_TYPE_VALUES!r}"
    )
