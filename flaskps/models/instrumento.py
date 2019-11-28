from pymysql.err import IntegrityError


class Instrumento(object):
    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    instrumento
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = """
                INSERT INTO instrumento 
                            (nombre, 
                             tipo_id, 
                             num_inventario,
                             image_path) 
                VALUES      (%s, 
                             %s,
                             %s, 
                             %s)
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("nombre"),
                        data.get("tipo_id"),
                        data.get("num_inventario"),
                        data.get("image_path"),
                    ),
                )
                cls.db.commit()

        except IntegrityError:
            cls.db.cursor().close()
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def tipos_instrumento(cls):
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
