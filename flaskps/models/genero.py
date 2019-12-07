from flaskps.db import get_db


class Genero(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM genero
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, gid):
        sql = """
                SELECT  nombre
                FROM    genero
                WHERE   id = %s
            """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, gid)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()
