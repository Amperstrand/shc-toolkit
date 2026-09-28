from enum import StrEnum


class SupportTicketReplyResponseReplyAuthorType(StrEnum):
    CLIENT = "client"

    def __str__(self) -> str:
        return str(self.value)
