class Escuela(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM escuela
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()