from pymysql.err import IntegrityError


class Taller(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    taller
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
            INSERT INTO taller
                        (nombre, 
                         nombre_corto
                         ) 
            VALUES      (%s, 
                         %s
                         )
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (data.get("nombre"), data.get("nombre_corto")))
                cls.db.commit()

        except IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def set_ciclo(cls, data):
        sql_delete_relation = """
                DELETE FROM ciclo_lectivo_taller 
                WHERE  taller_id = %s 
            """

        sql_insert_relation = """
            INSERT INTO ciclo_lectivo_taller 
                        (taller_id, 
                         ciclo_lectivo_id
                         ) 
            VALUES      (%s, 
                         %s
                         )
                    """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql_delete_relation, data.get("taller_id"))
                cls.db.commit()
                cursor.execute(sql_insert_relation, (data.get("taller_id"), data.get("ciclo_id")))
                cls.db.commit()

        except IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True
