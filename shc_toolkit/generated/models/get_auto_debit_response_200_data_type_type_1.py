from typing import Literal

GetAutoDebitResponse200DataTypeType1 = Literal["ach", "cc"]

GET_AUTO_DEBIT_RESPONSE_200_DATA_TYPE_TYPE_1_VALUES: set[
    GetAutoDebitResponse200DataTypeType1
] = {
    "ach",
    "cc",
}


def check_get_auto_debit_response_200_data_type_type_1(
    value: str,
) -> GetAutoDebitResponse200DataTypeType1:
    if value in GET_AUTO_DEBIT_RESPONSE_200_DATA_TYPE_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_AUTO_DEBIT_RESPONSE_200_DATA_TYPE_TYPE_1_VALUES!r}"
    )
