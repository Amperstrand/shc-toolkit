from typing import Literal

CreateApiKeyBodyAreasItem = Literal[
    "_credits",
    "_managed",
    "client_accounts",
    "client_contacts",
    "client_emails",
    "client_invoices",
    "client_quotations",
    "client_services",
    "client_transactions",
    "support",
]

CREATE_API_KEY_BODY_AREAS_ITEM_VALUES: set[CreateApiKeyBodyAreasItem] = {
    "_credits",
    "_managed",
    "client_accounts",
    "client_contacts",
    "client_emails",
    "client_invoices",
    "client_quotations",
    "client_services",
    "client_transactions",
    "support",
}


def check_create_api_key_body_areas_item(value: str) -> CreateApiKeyBodyAreasItem:
    if value in CREATE_API_KEY_BODY_AREAS_ITEM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_API_KEY_BODY_AREAS_ITEM_VALUES!r}"
    )
