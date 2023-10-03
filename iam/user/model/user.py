from pydantic import BaseModel

from iam.user.model.user_role import UserRole


class User(BaseModel):
    role: UserRole
    name: str
