class User(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT u.id, email, username, password, activo, created_at, updated_at, first_name, last_name, rol.nombre as rol_nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = """
            INSERT INTO usuarios (email, username, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, list(data.values()))
                cls.db.commit()
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def find_by_user_and_pass(cls, username, password):
        sql = """
            SELECT * FROM usuarios AS u
            WHERE u.username = %s AND u.password = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (username, password))
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def find_by_user(cls, username):
        sql = """
            SELECT * FROM usuarios AS u
            WHERE u.username = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def permissions(cls, username):
        sql = """
            SELECT p.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id INNER JOIN rol_tiene_permiso as u_rol_perm ON rol.id = u_rol_perm.rol_id INNER JOIN permiso AS p ON p.id = u_rol_perm.permiso_id
            WHERE u.username = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            cls.db.cursor().close()

        return cursor.fetchall()

    @classmethod
    def has_permission(cls, username, permission_name):
        sql = """
            SELECT p.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id INNER JOIN rol_tiene_permiso as u_rol_perm ON rol.id = u_rol_perm.rol_id INNER JOIN permiso AS p ON p.id = u_rol_perm.permiso_id
            WHERE u.username = %s AND p.nombre = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (username, permission_name))
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def role(cls, username):
        sql = """
            SELECT rol.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id
            WHERE u.username = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def has_role(cls, username, role_name):
        sql = """
            SELECT rol.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id
            WHERE u.username = %s AND rol.nombre = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (username, role_name))
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()
