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

    @classmethod
    def destroy(cls, id_ciclo):
        sql_eliminar = """
                    DELETE 
                    FROM ciclo_lectivo 
                    WHERE (id = %s) AND (ciclo_lectivo.id NOT IN (
                        SELECT ciclo_lectivo_taller.ciclo_lectivo_id
                        FROM ciclo_lectivo_taller 
                        WHERE ciclo_lectivo_id = %s))
                """

        sql_comprobar_eliminacion = """
                                    SELECT id FROM ciclo_lectivo
                                    WHERE id = %s    
                                    """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql_eliminar, (id_ciclo, id_ciclo),
                )
                cls.db.commit()
                cursor.execute(
                    sql_comprobar_eliminacion, (id_ciclo),
                )
        finally:
            cls.db.cursor().close()
        row = cursor.fetchone()
        if row is None:
            return True
        return False

    @classmethod
    def talleres(cls, c_id):
        sql = """
                SELECT  t.id, t.nombre, t.nombre_corto
                FROM    ciclo_lectivo_taller c INNER JOIN taller t on c.taller_id = t.id
                WHERE   ciclo_lectivo_id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, c_id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchall()
