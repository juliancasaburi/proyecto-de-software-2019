from pymysql.err import IntegrityError

from flaskps.db import get_db


class SiteConfig(object):
    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM config
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql)
        finally:
            dbconn.cursor().close()
        return cursor.fetchone()

    @classmethod
    def update_config(cls, data):
        sql = """
            UPDATE config
            SET titulo = %s,
                descripcion = %s,
                email_contacto = %s,
                items_por_pagina = %s
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data["titulo"],
                        data["descripcion"],
                        data["email"],
                        data["items_por_pagina"],
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
    def update_maintenance(cls, maintenance):
        sql = """
            UPDATE config
            SET modo_mantenimiento = %s
        """
        try:
            dbconn = get_db()
            with dbconn.cursor() as cursor:
                cursor.execute(sql, maintenance)
                dbconn.commit()
        finally:
            dbconn.cursor().close()


def get_config():

    return SiteConfig.all()


def update_config(data):

    return SiteConfig.update_config(data)


def update_maintenance(maintenance):

    SiteConfig.update_maintenance(maintenance)
