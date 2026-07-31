from typing import Literal

GetKbArticleResponse200DataContentTypeType3Type1 = Literal["html", "text"]

GET_KB_ARTICLE_RESPONSE_200_DATA_CONTENT_TYPE_TYPE_3_TYPE_1_VALUES: set[
    GetKbArticleResponse200DataContentTypeType3Type1
] = {
    "html",
    "text",
}


def check_get_kb_article_response_200_data_content_type_type_3_type_1(
    value: str,
) -> GetKbArticleResponse200DataContentTypeType3Type1:
    if value in GET_KB_ARTICLE_RESPONSE_200_DATA_CONTENT_TYPE_TYPE_3_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_KB_ARTICLE_RESPONSE_200_DATA_CONTENT_TYPE_TYPE_3_TYPE_1_VALUES!r}"
    )
