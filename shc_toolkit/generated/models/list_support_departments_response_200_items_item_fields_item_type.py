from enum import StrEnum


class ListSupportDepartmentsResponse200ItemsItemFieldsItemType(StrEnum):
    CHECKBOX = "checkbox"
    EMERGENCY = "emergency"
    PASSWORD = "password"
    QUANTITY = "quantity"
    RADIO = "radio"
    SELECT = "select"
    TEXT = "text"
    TEXTAREA = "textarea"

    def __str__(self) -> str:
        return str(self.value)
