class TipoInstrumento(object):
    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    tipo_instrumento
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, id):
        sql = """
                SELECT  *
                FROM    tipo_instrumento
                WHERE   id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()
