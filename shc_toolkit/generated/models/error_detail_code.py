from enum import Enum


class ErrorDetailCode(str, Enum):
    ALREADY_IN_USE = "already_in_use"
    INVALID = "invalid"
    OUT_OF_RANGE = "out_of_range"
    REQUIRED = "required"
    UNKNOWN_FIELD = "unknown_field"
    UNSUPPORTED_VALUE = "unsupported_value"

    def __str__(self) -> str:
        return str(self.value)
