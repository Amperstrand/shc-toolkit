from enum import StrEnum


class ErrorErrorLinksItemRel(StrEnum):
    ABOUT = "about"
    DOCS = "docs"
    HELP = "help"
    RETRY = "retry"
    STATUS = "status"

    def __str__(self) -> str:
        return str(self.value)
