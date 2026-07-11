from enum import Enum


class TransactionSummaryStatus(str, Enum):
    APPROVED = "approved"
    DECLINED = "declined"
    ERROR = "error"
    PENDING = "pending"
    REFUNDED = "refunded"
    RETURNED = "returned"
    VOID = "void"

    def __str__(self) -> str:
        return str(self.value)
