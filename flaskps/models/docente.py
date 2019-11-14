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
            INSERT INTO usuario 
                        (first_name, 
                         last_name, 
                         email, 
                         username, 
                         PASSWORD) 
            VALUES      (%s, 
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
                        data.get("first_name"),
                        data.get("last_name"),
                        data.get("email"),
                        data.get("username"),
                        data.get("password"),
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
