from typing import Literal

StorageItemKind = Literal["backup", "snapshot"]

STORAGE_ITEM_KIND_VALUES: set[StorageItemKind] = {
    "backup",
    "snapshot",
}


def check_storage_item_kind(value: str) -> StorageItemKind:
    if value in STORAGE_ITEM_KIND_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STORAGE_ITEM_KIND_VALUES!r}"
    )
