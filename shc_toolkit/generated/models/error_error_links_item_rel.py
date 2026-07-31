from typing import Literal

ErrorErrorLinksItemRel = Literal["about", "docs", "help", "retry", "status"]

ERROR_ERROR_LINKS_ITEM_REL_VALUES: set[ErrorErrorLinksItemRel] = {
    "about",
    "docs",
    "help",
    "retry",
    "status",
}


def check_error_error_links_item_rel(value: str) -> ErrorErrorLinksItemRel:
    if value in ERROR_ERROR_LINKS_ITEM_REL_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ERROR_ERROR_LINKS_ITEM_REL_VALUES!r}"
    )
