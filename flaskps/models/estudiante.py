from pymysql.err import IntegrityError

from flaskps.db import get_db


class Estudiante(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT  e.*,
                    n.nombre,  
                    g.nombre,
                    es.nombre,
                    b.nombre,
                    r.nombre
            FROM    estudiante AS e
                    INNER JOIN nivel AS n
                            ON n.id = e.nivel_id
                    INNER JOIN genero AS g
                            ON g.id = e.genero_id
                    INNER JOIN escuela AS es
                            ON es.id = e.escuela_id
                    INNER JOIN barrio AS b
                            ON b.id = e.barrio_id
                    INNER JOIN responsable_tipo as r
                            ON r.id = e.responsable_tipo_id
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = """
            INSERT INTO estudiante 
                        (apellido, 
                         nombre, 
                         fecha_nac, 
                         localidad_id, 
                         nivel_id,
                         domicilio,
                         genero_id,
                         escuela_id,
                         tipo_doc_id,
                         numero,
                         tel,
                         barrio_id,
                         responsable_tipo_id) 
            VALUES      (%s, 
                         %s, 
                         %s, 
                         %s, 
                         %s,
                         %s,
                         %s,
                         %s,
                         %s,
                         %s,
                         %s,
                         %s,
                         %s)
        """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("last_name"),
                        data.get("first_name"),
                        data.get("fecha_nacimiento"),
                        data.get("select_localidad"),
                        data.get("select_nivel"),
                        data.get("domicilio"),
                        data.get("select_genero"),
                        data.get("select_escuela"),
                        data.get("select_tipo"),
                        data.get("documento_numero"),
                        data.get("telefono_numero"),
                        data.get("select_barrio"),
                        data.get("select_responsable_tipo"),
                    ),
                )
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def update(cls, data):

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:

                query = """
                        UPDATE estudiante
                        SET    apellido = %s, 
                               nombre = %s, 
                               fecha_nac = %s, 
                               localidad_id = %s, 
                               nivel_id = %s,
                               domicilio = %s,
                               genero_id = %s,
                               escuela_id = %s,
                               tipo_doc_id = %s,
                               numero = %s,
                               tel = %s,
                               barrio_id = %s,
                               responsable_tipo_id = %s
                        WHERE  id = %s 
                    """

                cursor.execute(
                    query,
                    (
                        data.get("last_name"),
                        data.get("first_name"),
                        data.get("fecha_nacimiento"),
                        data.get("select_localidad"),
                        data.get("select_nivel"),
                        data.get("domicilio"),
                        data.get("select_genero"),
                        data.get("select_escuela"),
                        data.get("select_tipo"),
                        data.get("documento_numero"),
                        data.get("telefono_numero"),
                        data.get("select_barrio"),
                        data.get("select_responsable_tipo"),
                        data.get("id"),
                    ),
                )
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def delete(cls, eid):
        sql = """
                UPDATE  estudiante 
                SET     activo = NOT activo
                WHERE  id = %s 
            """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, eid)
                dbconn.commit()
        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def find_by_id(cls, id):
        sql = """
                SELECT  *
                FROM    estudiante
                WHERE   id = %s
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            dbconn.cursor().close()

        return cursor.fetchone()
