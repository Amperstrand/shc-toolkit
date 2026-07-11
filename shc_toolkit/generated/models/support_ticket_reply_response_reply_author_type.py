from enum import Enum


class SupportTicketReplyResponseReplyAuthorType(str, Enum):
    CLIENT = "client"

    def __str__(self) -> str:
        return str(self.value)
