from enum import StrEnum


class ActivityItemType(StrEnum):
    CONTACT_CHANGE = "contact_change"
    LOGIN = "login"
    LOGIN_FAILED = "login_failed"
    SETTING_CHANGE = "setting_change"
    TRANSACTION = "transaction"

    def __str__(self) -> str:
        return str(self.value)
