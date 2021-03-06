from pymysql.err import IntegrityError

from flaskps.db import get_db


class User(object):
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
            FROM    usuario AS u 
                    INNER JOIN usuario_tiene_rol AS u_rol 
                            ON u.id = u_rol.usuario_id 
                    INNER JOIN rol 
                            ON rol.id = u_rol.rol_id 
            GROUP  BY u.id
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = """
            INSERT INTO usuario 
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
            FROM    usuario as u
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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
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
                dbconn.commit()
                cursor.execute(sql_user_id, data["username"])
                user_id = cursor.fetchone()
                for rol in roles:
                    cursor.execute(sql_user_rol, (user_id["id"], rol))
                    dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def delete(cls, uid):
        sql = """
            UPDATE  usuario 
            SET     activo = NOT activo
            WHERE  id = %s 
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, uid)
                dbconn.commit()
        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
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
            dbconn = get_db()
            with dbconn.cursor() as cursor:

                query = """
                    UPDATE usuario 
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
                dbconn.commit()

                cursor.execute(sql_delete_user_roles, data.get("id"))
                dbconn.commit()

                roles = data.get("roles")

                for rol in roles:
                    cursor.execute(sql_user_rol, (data.get("id"), rol))
                    dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def find_by_user_and_pass(cls, username, password):
        sql = """
            SELECT * 
            FROM   usuario
            WHERE  username = %s 
                   AND password = %s
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (username, password))
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

    @classmethod
    def find_by_user(cls, username):
        sql = """
            SELECT * 
            FROM   usuario 
            WHERE  username = %s
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT  *
            FROM    usuario
            WHERE   id = %s
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

    @classmethod
    def permissions(cls, username):
        sql = """
            SELECT p.nombre 
            FROM   usuario AS u 
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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            dbconn.cursor().close()

        return cursor.fetchall()

    @classmethod
    def has_permission(cls, username, permission_name):
        sql = """
            SELECT p.nombre 
            FROM   usuario AS u 
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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (username, permission_name))
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

    @classmethod
    def role(cls, username):
        sql = """
            SELECT rol.nombre 
            FROM   usuario AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
            WHERE  u.username = %s
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

    @classmethod
    def has_role(cls, username, role_name):
        sql = """
            SELECT rol.nombre 
            FROM   usuario AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
            WHERE  u.username = %s 
                   AND rol.nombre = %s
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (username, role_name))
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

    @classmethod
    def update_email(cls, email, username):
        sql = """
            UPDATE usuario
            SET    email = %s 
            WHERE  username = %s
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (email, username))
                dbconn.commit()
                return True
        finally:
            dbconn.cursor().close()

    @classmethod
    def update_password(cls, password, username):
        sql = """
            UPDATE usuario 
            SET    password = %s 
            WHERE  username = %s
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (password, username))
                dbconn.commit()
                return True
        finally:
            dbconn.cursor().close()

    @classmethod
    def user_roles(cls, username):
        sql = """
            SELECT rol.id     AS id, 
                   rol.nombre AS nombre 
            FROM   usuario AS u 
                   inner join usuario_tiene_rol AS u_rol 
                           ON u.id = u_rol.usuario_id 
                   inner join rol 
                           ON rol.id = u_rol.rol_id 
            WHERE  u.username = %s
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, username)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def all_table(cls):
        users = cls.all()

        for dict_item in users:
            del dict_item["password"]
            dict_item["created_at"] = dict_item["created_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )
            dict_item["updated_at"] = dict_item["updated_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        return users
