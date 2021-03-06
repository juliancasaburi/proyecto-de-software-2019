from pymysql.err import IntegrityError

from flaskps.db import get_db


class Taller(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    taller
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, id):
        sql = """
                SELECT  *
                FROM    taller
                WHERE   id = %s
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()

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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (data.get("nombre"), data.get("nombre_corto")))
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql_delete_relation, data.get("taller_id"))
                dbconn.commit()

                ciclos = data.get("ciclos")
                for ciclo in ciclos:
                    cursor.execute(sql_insert_relation, (data.get("taller_id"), ciclo))
                    dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def ciclos(cls, t_id):
        sql = """
                SELECT  clt.ciclo_lectivo_id, cl.fecha_ini, cl.fecha_fin, cl.semestre
                FROM    ciclo_lectivo_taller clt INNER JOIN ciclo_lectivo cl on clt.ciclo_lectivo_id = cl.id
                WHERE   taller_id = %s
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, t_id)
        finally:
            dbconn.cursor().close()

        return cursor.fetchall()

    @classmethod
    def docentes_ciclo(cls, t_id, c_id):
        sql = """
                SELECT  d.id, d.nombre, d.apellido
                FROM    docente_responsable_taller c INNER JOIN docente d on c.docente_id = d.id
                WHERE   taller_id = %s AND ciclo_lectivo_id = %s
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (t_id, c_id))
        finally:
            dbconn.cursor().close()

        return cursor.fetchall()

    @classmethod
    def estudiantes_ciclo(cls, t_id, c_id):
        sql = """
                    SELECT  e.id, e.nombre, e.apellido
                    FROM    estudiante_taller et INNER JOIN estudiante e on et.estudiante_id = e.id
                    WHERE   taller_id = %s AND ciclo_lectivo_id = %s
                """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (t_id, c_id))
        finally:
            dbconn.cursor().close()

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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql_delete_relation,
                    (data.get("taller_id"), data.get("ciclo_lectivo_id")),
                )
                dbconn.commit()

                docentes = data.get("docentes")
                for docente in docentes:
                    cursor.execute(
                        sql_insert_relation,
                        (docente, data.get("ciclo_lectivo_id"), data.get("taller_id")),
                    )
                    dbconn.commit()

        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def set_estudiantes(cls, data):
        sql_delete_relation = """
                    DELETE FROM estudiante_taller
                    WHERE  taller_id = %s AND ciclo_lectivo_id = %s
                """

        sql_insert_relation = """
                INSERT INTO estudiante_taller
                            (estudiante_id,
                             ciclo_lectivo_id,
                             taller_id 
                             ) 
                VALUES      (%s, 
                             %s,
                             %s
                             )
                        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql_delete_relation,
                    (data.get("taller_id"), data.get("ciclo_lectivo_id")),
                )
                dbconn.commit()

                estudiantes = data.get("estudiantes")
                for estudiante in estudiantes:
                    cursor.execute(
                        sql_insert_relation,
                        (
                            estudiante,
                            data.get("ciclo_lectivo_id"),
                            data.get("taller_id"),
                        ),
                    )
                    dbconn.commit()

        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def update(cls, data):

        sql = """
                        UPDATE taller 
                        SET nombre = %s, 
                            nombre_corto = %s 
                        WHERE id = %s
                """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (data.get("nombre"), data.get("nombre_corto"), data.get("id"),),
                )
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True
