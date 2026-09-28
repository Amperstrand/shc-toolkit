from enum import StrEnum


class ListQuotationsStatus(StrEnum):
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
