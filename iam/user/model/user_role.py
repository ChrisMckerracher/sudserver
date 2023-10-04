from enum import Enum
from typing import ForwardRef


class UserRole(Enum):
    MONSTER = 1
    PLAYER = 2
    ADMIN = 3

    def __lt__(self, other: ForwardRef("UserRole")):
        return self.value < other.value