from enum import Enum


class ListClientDocumentsSort(str, Enum):
    DATE_ADDED = "date_added"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
