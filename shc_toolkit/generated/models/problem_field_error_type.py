from enum import StrEnum


class ProblemFieldErrorType(StrEnum):
    FIELD = "field"

    def __str__(self) -> str:
        return str(self.value)
