from enum import Enum


class ListSupportDepartmentsResponse200ItemsItemFieldsItemType(str, Enum):
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
