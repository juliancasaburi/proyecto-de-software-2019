from flaskps.db import get_db


class TipoInstrumento(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    tipo_instrumento
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, id):
        sql = """
                SELECT  *
                FROM    tipo_instrumento
                WHERE   id = %s
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()
