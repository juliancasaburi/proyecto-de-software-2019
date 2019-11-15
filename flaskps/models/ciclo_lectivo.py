from pymysql.err import IntegrityError


class CicloLectivo(object):
    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    ciclo_lectivo
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
                INSERT INTO ciclo_lectivo 
                            (fecha_ini, 
                             fecha_fin, 
                             semestre) 
                VALUES      (%s, 
                             %s, 
                             %s)
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("fecha_inicio"),
                        data.get("fecha_fin"),
                        data.get("semestre"),
                    ),
                )
                cls.db.commit()

        except IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True
