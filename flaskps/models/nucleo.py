from pymysql.err import IntegrityError

from flaskps.db import get_db


class Nucleo(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    nucleo
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def activos(cls):
        sql = """
                SELECT  *
                FROM    nucleo
                WHERE activo = 1
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
            INSERT INTO nucleo 
                        (nombre, 
                         direccion, 
                         telefono, 
                         lat, 
                         lng) 
            VALUES      (%s, 
                         %s, 
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
                        data.get("direccion"),
                        data.get("telefono"),
                        data.get("lat"),
                        data.get("lng"),
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
    def update(cls, data):

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:

                query = """
                        UPDATE nucleo
                        SET    nombre = %s, 
                               direccion = %s, 
                               telefono = %s, 
                               lat = %s, 
                               lng = %s
                        WHERE  id = %s 
                    """

                cursor.execute(
                    query,
                    (
                        data.get("nombre"),
                        data.get("direccion"),
                        data.get("telefono"),
                        data.get("lat"),
                        data.get("lng"),
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

    @classmethod
    def delete(cls, nid):
        sql = """
                UPDATE  nucleo 
                SET     activo = NOT activo
                WHERE  id = %s 
            """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, nid)
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
                FROM    nucleo
                WHERE   id = %s
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()
