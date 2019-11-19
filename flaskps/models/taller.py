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
    def set_ciclos(cls, data):
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

                ciclos = data.get("ciclos")
                for ciclo in ciclos:
                    cursor.execute(sql_insert_relation, (data.get("taller_id"), ciclo))
                    cls.db.commit()

        except IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def ciclos(cls, t_id):
        sql = """
                SELECT  ciclo_lectivo_id
                FROM    ciclo_lectivo_taller
                WHERE   taller_id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, t_id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchall()

    @classmethod
    def docentes_ciclo(cls, t_id, c_id):
        sql = """
                SELECT  d.id, d.nombre, d.apellido
                FROM    docente_responsable_taller c INNER JOIN docente d on c.docente_id = d.id
                WHERE   taller_id = %s AND ciclo_lectivo_id = %s
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, (t_id, c_id))
        finally:
            cls.db.cursor().close()

        return cursor.fetchall()

    @classmethod
    def set_docentes(cls, data):
        sql_delete_relation = """
                DELETE FROM docente_responsable_taller
                WHERE  taller_id = %s AND ciclo_lectivo_id = %s
            """

        sql_insert_relation = """
            INSERT INTO docente_responsable_taller 
                        (docente_id,
                         ciclo_lectivo_id,
                         taller_id 
                         ) 
            VALUES      (%s, 
                         %s,
                         %s
                         )
                    """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql_delete_relation,
                    (data.get("taller_id"), data.get("ciclo_lectivo_id")),
                )
                cls.db.commit()

                docentes = data.get("docentes")
                for docente in docentes:
                    cursor.execute(
                        sql_insert_relation,
                        (docente, data.get("ciclo_lectivo_id"), data.get("taller_id")),
                    )
                    cls.db.commit()

        finally:
            cls.db.cursor().close()
        return True
