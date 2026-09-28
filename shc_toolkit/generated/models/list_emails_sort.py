from enum import StrEnum


class ListEmailsSort(StrEnum):
    DATE_SENT = "date_sent"
    SUBJECT = "subject"

    def __str__(self) -> str:
        return str(self.value)
