from pymysql.err import IntegrityError

from flaskps.db import get_db


class Instrumento(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    instrumento
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
                INSERT INTO instrumento 
                            (nombre, 
                             tipo_id, 
                             num_inventario,
                             image_path) 
                VALUES      (%s, 
                             %s,
                             %s, 
                             %s)
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("nombre"),
                        data.get("tipo_id"),
                        data.get("num_inventario"),
                        data.get("image_path"),
                    ),
                )
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def find_by_id(cls, id):
        sql = """
                SELECT  *
                FROM    instrumento
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
    def image_path(cls, id):
        sql = """
                SELECT  image_path
                FROM    instrumento
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
    def update(cls, data):

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:

                query = """
                            UPDATE instrumento
                            SET    nombre = %s, 
                                   tipo_id = %s, 
                                   num_inventario = %s 
                            WHERE  id = %s 
                        """

                cursor.execute(
                    query,
                    (
                        data.get("nombre"),
                        data.get("tipo_id"),
                        data.get("num_inventario"),
                        data.get("id"),
                    ),
                )
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True
