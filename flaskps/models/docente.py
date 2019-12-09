from pymysql.err import IntegrityError

from flaskps.db import get_db
from flaskps.helpers.localidades import localidad
from flaskps.helpers.tipos_documento import tipo_documento
from flaskps.models.genero import Genero
from flaskps.models.user import User


class Docente(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT  *
            FROM    docente
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
            FROM    docente
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
                INSERT INTO docente 
                            (usuario_id,
                             apellido, 
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
                             %s,
                             %s
                             )
            """

        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("usuario_id"),
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
                dbconn.commit()

        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
        return True

    @classmethod
    def delete(cls, d_id):
        sql = """
            UPDATE  docente 
            SET     activo = NOT activo
            WHERE  id = %s 
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, d_id)
                dbconn.commit()
        except IntegrityError:
            dbconn.cursor().close()
            return False
        finally:
            dbconn.cursor().close()
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
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, did)
        finally:
            dbconn.cursor().close()
        return cursor.fetchall()

    @classmethod
    def update(cls, data):

        sql = """
                    UPDATE docente 
                    SET usuario_id = %s,
                        apellido = %s, 
                        nombre = %s, 
                        fecha_nac = %s, 
                        localidad_id = %s, 
                        domicilio = %s, 
                        genero_id = %s,
                        tipo_doc_id = %s,
                        numero = %s,
                        tel = %s
                    WHERE id = %s 
            """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data.get("usuario_id"),
                        data.get("apellido"),
                        data.get("nombre"),
                        data.get("fecha_nacimiento"),
                        data.get("select_localidad"),
                        data.get("domicilio"),
                        data.get("select_genero"),
                        data.get("select_tipo"),
                        data.get("documento_numero"),
                        data.get("telefono_numero"),
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
    def all_table(cls):
        docentes = cls.all()

        for dict_item in docentes:
            usuario_id = dict_item["usuario_id"]
            if usuario_id:

                user = User.find_by_id(usuario_id)
                dict_item["username"] = user["username"]
            dict_item["fecha_nacimiento"] = dict_item["fecha_nac"].strftime("%d-%m-%Y")
            del dict_item["fecha_nac"]
            loc = localidad(dict_item["localidad_id"])
            dict_item["localidad"] = loc["nombre"]
            del dict_item["localidad_id"]

            dict_item["genero"] = Genero.find_by_id(dict_item["genero_id"])[0]["nombre"]
            del dict_item["genero_id"]
            tipo_doc = tipo_documento(dict_item["tipo_doc_id"])
            dict_item["tipo_documento"] = tipo_doc["nombre"]
            del dict_item["tipo_doc_id"]
            dict_item["created_at"] = dict_item["created_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )
            dict_item["updated_at"] = dict_item["updated_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        return docentes


    @classmethod
    def talleres_by_id(cls, id):
        sql = """
            SELECT  t.id, t.nombre, t.nombre_corto
            FROM    docente d INNER JOIN 
            WHERE   id = %s
        """

        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, id)
        finally:
            cls.db.cursor().close()

        return cursor.fetchone()