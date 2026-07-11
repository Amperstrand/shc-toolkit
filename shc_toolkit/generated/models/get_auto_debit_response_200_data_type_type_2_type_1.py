from enum import Enum


class GetAutoDebitResponse200DataTypeType2Type1(str, Enum):
    ACH = "ach"
    CC = "cc"

    def __str__(self) -> str:
        return str(self.value)
