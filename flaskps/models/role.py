from flaskps.db import get_db


class Role(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM rol
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()
