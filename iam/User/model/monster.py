from iam.User.model.User import User
from iam.User.model.UserRole import UserRole


class Monster(User):
    role = UserRole.MONSTER
