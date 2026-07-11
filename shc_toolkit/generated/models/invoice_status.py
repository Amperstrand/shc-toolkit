from enum import Enum


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    PAST_DUE = "past_due"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    VOIDED = "voided"

    def __str__(self) -> str:
        return str(self.value)
