from iam.user.model.user import User
from iam.user.model.user_role import UserRole


class Monster(User):
    role = UserRole.MONSTER
