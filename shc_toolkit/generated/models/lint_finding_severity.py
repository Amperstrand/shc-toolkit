from enum import StrEnum


class LintFindingSeverity(StrEnum):
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
