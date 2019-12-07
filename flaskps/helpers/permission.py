from flaskps.db import get_db
from flaskps.models.user import User


def has_permission(permission_name, session):
    username = session.get("user")
    perm = User.has_permission(username, permission_name)

    return perm
