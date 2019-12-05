from pymysql.err import IntegrityError


class Nucleo(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    nucleo
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()

    @classmethod
    def activos(cls):
        sql = """
                SELECT  *
                FROM    nucleo
                WHERE activo = 1
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
            INSERT INTO nucleo 
                        (nombre, 
                         direccion, 
                         telefono, 
                         lat, 
                         lng) 
            VALUES      (%s, 
                         %s, 
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
                        data.get("direccion"),
                        data.get("telefono"),
                        data.get("lat"),
                        data.get("lng"),
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
    def update(cls, data):

        try:
            with cls.db.cursor() as cursor:

                query = """
                        UPDATE nucleo
                        SET    nombre = %s, 
                               direccion = %s, 
                               telefono = %s, 
                               lat = %s, 
                               lng = %s
                        WHERE  id = %s 
                    """

                cursor.execute(
                    query,
                    (
                        data.get("nombre"),
                        data.get("direccion"),
                        data.get("telefono"),
                        data.get("lat"),
                        data.get("lng"),
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

    @classmethod
    def delete(cls, nid):
        sql = """
                UPDATE  nucleo 
                SET     activo = NOT activo
                WHERE  id = %s 
            """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, nid)
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
                FROM    nucleo
                WHERE   id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()
