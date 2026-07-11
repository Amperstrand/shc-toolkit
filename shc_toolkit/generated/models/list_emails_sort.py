from enum import Enum


class ListEmailsSort(str, Enum):
    DATE_SENT = "date_sent"
    SUBJECT = "subject"

    def __str__(self) -> str:
        return str(self.value)
