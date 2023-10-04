from functools import wraps

from iam.user.model.user_role import UserRole
from flask import g


def is_authorized(role: UserRole):
    def is_auth_decorator(f):
        @wraps(f)
        def auth_wrapper(*args, **kwargs):
            if (g.user and g.user.role < role):
                return ("uhuhuh you didnt say the magic word", 401)
            return f(*args, **kwargs)

        return auth_wrapper

    return is_auth_decorator
