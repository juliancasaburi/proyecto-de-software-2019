from flaskps.db import get_db


class Nivel(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM nivel
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()
