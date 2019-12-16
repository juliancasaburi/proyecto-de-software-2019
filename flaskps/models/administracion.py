from pymysql import IntegrityError

from flaskps.db import get_db


class Administracion(object):
    @classmethod
    def talleres_docente(cls, did):
        sql = """
            SELECT DISTINCT t.id, t.nombre, t.nombre_corto
            FROM    taller t INNER JOIN docente_responsable_taller r ON t.id = r.taller_id 
            WHERE   r.docente_id = %s
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, did)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def ciclos_taller_docente(cls, did, tid):
        sql = """
                    SELECT  c.id, c.fecha_ini, c.fecha_fin
                    FROM    ciclo_lectivo c INNER JOIN docente_responsable_taller r ON c.id = r.ciclo_lectivo_id
                    WHERE   r.docente_id = %s and r.taller_id = %s
                """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (did, tid))
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def dias_nucleo_ciclo_taller_docente(cls, did, tid, cid, nid):
        sql = """
                        SELECT  ds.id, ds.nombre
                        FROM    taller t INNER JOIN docente_responsable_taller r ON t.id = r.taller_id 
                                         INNER JOIN docente d ON d.id = r.docente_id
                                         INNER JOIN ciclo_lectivo_taller ct ON ct.taller_id = t.id
                                         INNER JOIN ciclo_lectivo c ON c.id = ct.ciclo_lectivo_id
                                         INNER JOIN docente_horario dh ON r.id = dh.docente_responsable_taller_id
                                         INNER JOIN nucleo n ON n.id = dh.nucleo_id
                                         INNER JOIN dia_semana ds ON ds.id = dh.dia_id
                        WHERE   d.id = %s and t.id = %s and c.id = %s and n.id = %s
                    """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (did, tid, cid, nid))
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def docente_responsable_taller_id(cls, did, cid, tid):
        sql = """
                SELECT  id
                FROM    docente_responsable_taller
                WHERE   docente_id = %s and ciclo_lectivo_id = %s and taller_id = %s 
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, (did, cid, tid))
        finally:
            dbconn.cursor().close()
        return cursor.fetchone()

    @classmethod
    def docente_set_horario(cls, rid, nid, dias):
        # borra todos los días de ese núcleo y docente_responsable_taller
        sql_delete_relation = """
                        DELETE FROM docente_horario
                        WHERE docente_responsable_taller_id = %s AND nucleo_id = %s
                    """

        # agrego los días seleccionados
        sql_insert_relation = """
                    INSERT INTO docente_horario 
                                (docente_responsable_taller_id,
                                 nucleo_id,
                                 dia_id 
                                 ) 
                    VALUES      (%s, 
                                 %s,
                                 %s
                                 )
                            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql_delete_relation, (rid, nid))
                dbconn.commit()

                for dia in dias:

                    cursor.execute(sql_insert_relation, (rid, nid, dia))
                    dbconn.commit()

        except IntegrityError:
            return False

        finally:
            dbconn.cursor().close()
        return True
