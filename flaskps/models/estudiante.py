from pymysql.err import IntegrityError


class Estudiante(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  e.id, 
                    e.apellido, 
                    e.nombre, 
                    e.fecha_nac, 
                    e.localidad_id,
                    n.nombre, 
                    e.domicilio, 
                    g.nombre,
                    es.nombre,
                    e.tipo_doc_id, 
                    e.numero,
                    e.tel,
                    b.nombre 
            FROM    estudiante AS e
                    INNER JOIN nivel AS n
                            ON n.id = e.nivel_id
                    INNER JOIN genero AS g
                            ON g.id = e.genero_id
                    INNER JOIN escuela AS es
                            ON es.id = e.escuela_id
                    INNER JOIN barrio AS b
                            ON b.id = e.barrio_id
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
                         barrio_id) 
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
                         %s)
        """

        try:
            with cls.db.cursor() as cursor:
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
                        data.get("select_barrio")
                    ),
                )
                cls.db.commit()

        except IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True
