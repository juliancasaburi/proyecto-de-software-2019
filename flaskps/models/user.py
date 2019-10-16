class User(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT u.id, email, username, password, activo, created_at, updated_at, first_name, last_name, rol.nombre as rol_nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id
        """
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = """
            INSERT INTO usuarios (email, username, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, list(data.values()))
        cls.db.commit()

        return True

    @classmethod
    def find_by_user_and_pass(cls, username, password):
        sql = """
            SELECT * FROM usuarios AS u
            WHERE u.username = %s AND u.password = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (username, password))

        return cursor.fetchone()

    @classmethod
    def find_by_user(cls, username):
        sql = """
            SELECT * FROM usuarios AS u
            WHERE u.username = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, username)

        return cursor.fetchone()

    @classmethod
    def permissions(cls, username):
        sql = """
            SELECT p.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id INNER JOIN rol_tiene_permiso as u_rol_perm ON rol.id = u_rol_perm.rol_id INNER JOIN permiso AS p ON p.id = u_rol_perm.permiso_id
            WHERE u.username = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, username)

        return cursor.fetchall()

    @classmethod
    def has_permission(cls, username, permission_name):
        sql = """
            SELECT p.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id INNER JOIN rol_tiene_permiso as u_rol_perm ON rol.id = u_rol_perm.rol_id INNER JOIN permiso AS p ON p.id = u_rol_perm.permiso_id
            WHERE u.username = %s AND p.nombre = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (username, permission_name))

        return cursor.fetchone()

    @classmethod
    def role(cls, username):
        sql = """
            SELECT rol.nombre
            FROM usuarios AS u INNER JOIN usuario_tiene_rol as u_rol ON u.id = u_rol.usuario_id INNER JOIN rol ON rol.id = u_rol.rol_id
            WHERE u.username = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, username)

        return cursor.fetchone()
