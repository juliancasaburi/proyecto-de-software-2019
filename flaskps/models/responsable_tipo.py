class Responsable_tipo(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM responsable_tipo
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()
