from flaskps.db import get_db


class Responsable_tipo(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM responsable_tipo
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()
