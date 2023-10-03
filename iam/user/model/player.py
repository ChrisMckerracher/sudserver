from iam.user.model.user import User
from iam.user.model.user_role import UserRole


class Player(User):
    role = UserRole.PLAYER
