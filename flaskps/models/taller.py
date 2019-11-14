from pymysql.err import IntegrityError


class Taller(object):

    db = None

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
