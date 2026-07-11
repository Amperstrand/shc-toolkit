from enum import Enum


class RegisterRequestScope(str, Enum):
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
