from flaskps.db import get_db
from flaskps.models.user import User


def has_permission(permission_name, session):
    User.db = get_db()
    username = session.get("user")
    perm = User.has_permission(username, permission_name)
    if perm:
        return True
    else:
        return False
