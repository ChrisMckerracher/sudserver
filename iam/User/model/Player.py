from iam.User.model.User import User
from iam.User.model.UserRole import UserRole


class Player(User):
    role = UserRole.PLAYER
