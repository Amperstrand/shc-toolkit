from enum import StrEnum


class ApproveQuotationResponse201DataStatus(StrEnum):
    APPROVED = "approved"

    def __str__(self) -> str:
        return str(self.value)
