from enum import Enum


class ApproveQuotationResponse201DataStatus(str, Enum):
    APPROVED = "approved"

    def __str__(self) -> str:
        return str(self.value)
