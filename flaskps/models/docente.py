from pymysql.err import IntegrityError


class Docente(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  id, 
                    apellido, 
                    nombre, 
                    fecha_nac, 
                    localidad_id, 
                    domicilio, 
                    genero_id, 
                    tipo_doc_id, 
                    numero,
                    tel
            FROM    docente
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
                INSERT INTO docente 
                            (apellido, 
                             nombre, 
                             fecha_nac, 
                             localidad_id, 
                             domicilio,
                             genero_id,
                             tipo_doc_id,
                             numero,
                             tel
                             ) 
                VALUES      (%s, 
                             %s, 
                             %s, 
                             %s, 
                             %s,
                             %s,
                             %s,
                             %s,
                             %s
                             )
            """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("apellido"),
                        data.get("nombre"),
                        data.get("fecha_nacimiento"),
                        data.get("select_localidad"),
                        data.get("domicilio"),
                        data.get("select_genero"),
                        data.get("select_tipo"),
                        data.get("documento_numero"),
                        data.get("telefono_numero"),
                    ),
                )
                cls.db.commit()

        except IntegrityError:
            return False
        finally:
            cls.db.cursor().close()
        return True

    @classmethod
    def genero(cls, did):
        sql = """
                SELECT  g.nombre
                FROM    docente AS d
                        INNER JOIN genero g
                        ON d.genero_id = g.id
                WHERE   d.id = %s
            """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, did)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()
