from enum import StrEnum


class GetSupportTicketResponse200DataRepliesItemAuthorType(StrEnum):
    CLIENT = "client"
    STAFF = "staff"

    def __str__(self) -> str:
        return str(self.value)
