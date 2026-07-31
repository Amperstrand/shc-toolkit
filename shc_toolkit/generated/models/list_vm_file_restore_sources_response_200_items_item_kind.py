from typing import Literal

ListVmFileRestoreSourcesResponse200ItemsItemKind = Literal["backup", "snapshot"]

LIST_VM_FILE_RESTORE_SOURCES_RESPONSE_200_ITEMS_ITEM_KIND_VALUES: set[
    ListVmFileRestoreSourcesResponse200ItemsItemKind
] = {
    "backup",
    "snapshot",
}


def check_list_vm_file_restore_sources_response_200_items_item_kind(
    value: str,
) -> ListVmFileRestoreSourcesResponse200ItemsItemKind:
    if value in LIST_VM_FILE_RESTORE_SOURCES_RESPONSE_200_ITEMS_ITEM_KIND_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_VM_FILE_RESTORE_SOURCES_RESPONSE_200_ITEMS_ITEM_KIND_VALUES!r}"
    )
