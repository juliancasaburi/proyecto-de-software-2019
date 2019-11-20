from pymysql.err import IntegrityError


class Docente(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    docente
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT  *
            FROM    docente
            WHERE   id = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()

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
    def delete(cls, d_id):
        sql = """
            UPDATE  docente 
            SET     activo = NOT activo
            WHERE  id = %s 
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, d_id)
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
