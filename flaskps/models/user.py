import pymysql


class User(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  u.id, 
                    email, 
                    username, 
                    password, 
                    activo, 
                    created_at, 
                    updated_at, 
                    first_name, 
                    last_name, 
                    Group_concat(rol.nombre ORDER BY rol.nombre SEPARATOR ', ') AS rol_nombre 
            FROM    usuarios AS u 
                    INNER JOIN usuario_tiene_rol AS u_rol 
                            ON u.id = u_rol.usuario_id 
                    INNER JOIN rol 
                            ON rol.id = u_rol.rol_id 
            GROUP  BY u.id
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
            INSERT INTO usuarios 
                        (first_name, 
                         last_name, 
                         email, 
                         username, 
                         PASSWORD) 
            VALUES      (%s, 
                         %s, 
                         %s, 
                         %s, 
                         %s)
        """

        sql_user_id = """
            SELECT  u.id
            FROM    usuarios as u
            WHERE   username = %s
        """

        sql_user_rol = """
            INSERT INTO usuario_tiene_rol 
                        (usuario_id,
                        rol_id)
            VALUES      (%s,
                        %s)
        """

        roles = data.get("roles")

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("first_name"),
                        data.get("last_name"),
                        data.get("email"),
                        data.get("username"),
                        data.get("password"),
                    ),
                )
                cls.db.commit()
                cursor.execute(sql_user_id, data["username"])
                user_id = cursor.fetchone()
                for rol in roles:
                    cursor.execute(sql_user_rol, (user_id["id"], rol))
                    cls.db.commit()

        except pymysql.err.IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def delete(cls, uid):
        sql = """
            DELETE FROM usuarios
            WHERE   usuarios.id = %s
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, uid)
                cls.db.commit()
        except pymysql.err.IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def update(cls, data):

        sql_delete_user_roles = """
            DELETE from usuario_tiene_rol
            WHERE   usuario_id = %s
        """

        sql_user_rol = """
            INSERT INTO usuario_tiene_rol 
                        (usuario_id, 
                        rol_id) 
            VALUES      (%s, 
                        %s) 
        """

        try:
            with cls.db.cursor() as cursor:

                query = """
                    UPDATE usuarios 
                    SET    activo = %s, 
                           first_name = %s, 
                           last_name = %s, 
                           email = %s, 
                           username = %s 
                    WHERE  id = %s 
                """

                cursor.execute(
                    query,
                    (
                        data.get("activo"),
                        data.get("first_name"),
                        data.get("last_name"),
                        data.get("email"),
                        data.get("username"),
                        data.get("id"),
                    ),
                )
                cls.db.commit()

                cursor.execute(sql_delete_user_roles, data.get("id"))
                cls.db.commit()

                roles = data.get("roles")

                for rol in roles:
                    cursor.execute(sql_user_rol, (data.get("id"), rol))
                    cls.db.commit()

        except pymysql.err.IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def find_by_user_and_pass(cls, username, password):
        sql = """
            SELECT * 
            FROM   usuarios
            WHERE  username = %s 
                   AND password = %s
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
            SELECT * 
            FROM   usuarios 
            WHERE  username = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT  *
            FROM    usuarios
            WHERE   id = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def permissions(cls, username):
        sql = """
            SELECT p.nombre 
            FROM   usuarios AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
                   inner join rol_tiene_permiso AS u_rol_perm 
                           ON rol.id = u_rol_perm.rol_id 
                   inner join permiso AS p 
                           ON p.id = u_rol_perm.permiso_id 
            WHERE  u.username = %s
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
            FROM   usuarios AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
                   inner join rol_tiene_permiso AS u_rol_perm 
                           ON rol.id = u_rol_perm.rol_id 
                   inner join permiso AS p 
                           ON p.id = u_rol_perm.permiso_id 
            WHERE  u.username = %s 
                   AND p.nombre = %s
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
            FROM   usuarios AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
            WHERE  u.username = %s
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
            FROM   usuarios AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
            WHERE  u.username = %s 
                   AND rol.nombre = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (username, role_name))
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def update_email(cls, email, username):
        sql = """
            UPDATE usuarios
            SET    email = %s 
            WHERE  username = %s
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (email, username))
                cls.db.commit()
        finally:
            cls.db.cursor().close()

    @classmethod
    def update_password(cls, password, username):
        sql = """
            UPDATE usuarios 
            SET    password = %s 
            WHERE  username = %s
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (password, username))
                cls.db.commit()
        finally:
            cls.db.cursor().close()

    @classmethod
    def user_roles(cls, username):
        sql = """
            SELECT rol.id     AS id, 
                   rol.nombre AS nombre 
            FROM   usuarios AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
            WHERE  u.username = %s
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()
