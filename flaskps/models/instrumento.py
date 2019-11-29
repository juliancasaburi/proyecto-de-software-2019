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
    def find_by_id(cls, id):
        sql = """
                SELECT  *
                FROM    instrumento
                WHERE   id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def image_path(cls, id):
        sql = """
                SELECT  image_path
                FROM    instrumento
                WHERE   id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

    @classmethod
    def update(cls, data):

        try:
            with cls.db.cursor() as cursor:

                query = """
                            UPDATE instrumento
                            SET    nombre = %s, 
                                   tipo_id = %s, 
                                   num_inventario = %s 
                            WHERE  id = %s 
                        """

                cursor.execute(
                    query,
                    (
                        data.get("nombre"),
                        data.get("tipo_id"),
                        data.get("num_inventario"),
                        data.get("id"),
                    ),
                )
                cls.db.commit()

        except IntegrityError:
            cls.db.cursor().close()
            return False
        finally:
            cls.db.cursor().close()
        return True
