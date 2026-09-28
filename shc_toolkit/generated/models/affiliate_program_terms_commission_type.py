from enum import StrEnum


class AffiliateProgramTermsCommissionType(StrEnum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"

    def __str__(self) -> str:
        return str(self.value)
