from enum import StrEnum


class GetAutoDebitResponse200DataTypeType2Type1(StrEnum):
    ACH = "ach"
    CC = "cc"

    def __str__(self) -> str:
        return str(self.value)
