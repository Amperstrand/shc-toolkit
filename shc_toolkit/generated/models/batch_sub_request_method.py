from typing import Literal

BatchSubRequestMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]

BATCH_SUB_REQUEST_METHOD_VALUES: set[BatchSubRequestMethod] = {
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
}


def check_batch_sub_request_method(value: str) -> BatchSubRequestMethod:
    if value in BATCH_SUB_REQUEST_METHOD_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BATCH_SUB_REQUEST_METHOD_VALUES!r}"
    )
