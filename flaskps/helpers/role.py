from flaskps.models.user import User


def has_role(role_name, session):
    username = session.get("user")
    role = User.has_role(username, role_name)

    return role


def roles(session):
    username = session.get("user")
    uroles = User.role(username)
    return uroles
