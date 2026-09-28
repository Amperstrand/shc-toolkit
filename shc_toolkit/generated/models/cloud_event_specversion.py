from enum import StrEnum


class CloudEventSpecversion(StrEnum):
    VALUE_0 = "1.0"

    def __str__(self) -> str:
        return str(self.value)
