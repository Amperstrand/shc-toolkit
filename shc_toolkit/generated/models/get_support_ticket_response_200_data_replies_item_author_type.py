from typing import Literal

GetSupportTicketResponse200DataRepliesItemAuthorType = Literal["client", "staff"]

GET_SUPPORT_TICKET_RESPONSE_200_DATA_REPLIES_ITEM_AUTHOR_TYPE_VALUES: set[
    GetSupportTicketResponse200DataRepliesItemAuthorType
] = {
    "client",
    "staff",
}


def check_get_support_ticket_response_200_data_replies_item_author_type(
    value: str,
) -> GetSupportTicketResponse200DataRepliesItemAuthorType:
    if value in GET_SUPPORT_TICKET_RESPONSE_200_DATA_REPLIES_ITEM_AUTHOR_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_SUPPORT_TICKET_RESPONSE_200_DATA_REPLIES_ITEM_AUTHOR_TYPE_VALUES!r}"
    )
