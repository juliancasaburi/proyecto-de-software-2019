from flaskps.db import get_db
from flaskps.models.user import User


def has_role(role_name, session):
    User.db = get_db()
    username = session.get("user")
    role = User.has_role(username, role_name)

    return role


def roles(session):
    User.db = get_db()
    username = session.get("user")
    uroles = User.role(username)
    return uroles
