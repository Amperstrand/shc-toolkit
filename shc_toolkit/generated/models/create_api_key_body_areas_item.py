from enum import Enum


class CreateApiKeyBodyAreasItem(str, Enum):
    CLIENT_ACCOUNTS = "client_accounts"
    CLIENT_CONTACTS = "client_contacts"
    CLIENT_EMAILS = "client_emails"
    CLIENT_INVOICES = "client_invoices"
    CLIENT_QUOTATIONS = "client_quotations"
    CLIENT_SERVICES = "client_services"
    CLIENT_TRANSACTIONS = "client_transactions"
    SUPPORT = "support"
    VALUE_7 = "_credits"
    VALUE_8 = "_managed"

    def __str__(self) -> str:
        return str(self.value)
