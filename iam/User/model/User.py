from pydantic import BaseModel

from iam.User.model.UserRole import UserRole


class User(BaseModel):
    role: UserRole
    name: str
