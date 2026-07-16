from enum import Enum


class ProblemFieldErrorType(str, Enum):
    FIELD = "field"

    def __str__(self) -> str:
        return str(self.value)
