from enum import StrEnum


class ListClientDocumentsSort(StrEnum):
    DATE_ADDED = "date_added"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
