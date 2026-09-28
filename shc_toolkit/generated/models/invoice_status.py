from enum import StrEnum


class InvoiceStatus(StrEnum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    PAST_DUE = "past_due"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    VOIDED = "voided"

    def __str__(self) -> str:
        return str(self.value)
