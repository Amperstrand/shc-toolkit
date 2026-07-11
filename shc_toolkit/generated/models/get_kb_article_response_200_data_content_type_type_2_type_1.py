from enum import Enum


class GetKbArticleResponse200DataContentTypeType2Type1(str, Enum):
    HTML = "html"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
