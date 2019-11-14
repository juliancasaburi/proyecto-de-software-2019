class Genero(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM genero
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, gid):
        sql = """
                SELECT  nombre
                FROM    genero
                WHERE   id = %s
            """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, gid)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()
