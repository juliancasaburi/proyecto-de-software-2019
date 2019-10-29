from flaskps.db import get_db
from flaskps.models.user import User


def has_role(role_name, session):
    User.db = get_db()
    username = session.get('user')
    perm = User.has_role(username, role_name)
    if perm:
        return True
    else:
        return False


def roles(session):
    User.db = get_db()
    username = session.get('user')
    uroles = User.role(username)
    return uroles

