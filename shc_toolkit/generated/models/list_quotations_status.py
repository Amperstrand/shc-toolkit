from enum import Enum


class ListQuotationsStatus(str, Enum):
    ALL = "all"
    APPROVED = "approved"
    DEAD = "dead"
    DRAFT = "draft"
    EXPIRED = "expired"
    INVOICED = "invoiced"
    LOST = "lost"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
