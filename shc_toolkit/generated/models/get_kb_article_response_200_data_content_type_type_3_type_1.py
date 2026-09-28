from enum import StrEnum


class GetKbArticleResponse200DataContentTypeType3Type1(StrEnum):
    HTML = "html"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
