from typing import Literal

SupportTicketReplyResponseReplyAuthorType = Literal["client"]

SUPPORT_TICKET_REPLY_RESPONSE_REPLY_AUTHOR_TYPE_VALUES: set[
    SupportTicketReplyResponseReplyAuthorType
] = {
    "client",
}


def check_support_ticket_reply_response_reply_author_type(
    value: str,
) -> SupportTicketReplyResponseReplyAuthorType:
    if value in SUPPORT_TICKET_REPLY_RESPONSE_REPLY_AUTHOR_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SUPPORT_TICKET_REPLY_RESPONSE_REPLY_AUTHOR_TYPE_VALUES!r}"
    )
