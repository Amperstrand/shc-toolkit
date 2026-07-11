from enum import Enum


class GetSupportTicketResponse200DataRepliesItemAuthorType(str, Enum):
    CLIENT = "client"
    STAFF = "staff"

    def __str__(self) -> str:
        return str(self.value)
