from flaskps.db import get_db


class SiteConfig(object):

    db = None

    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM config
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql)
        finally:
            cls.db.cursor().close()
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
            with cls.db.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        data["titulo_home"],
                        data["descripcion"],
                        data["email"],
                        data["items_por_pagina"],
                    ),
                )
                cls.db.commit()
        finally:
            cls.db.cursor().close()

    @classmethod
    def update_maintenancee(cls, maintenance):
        sql = """
            UPDATE config
            SET modo_mantenimiento = %s
        """
        try:
            with cls.db.cursor() as cursor:
                cursor.execute(sql, maintenance)
                cls.db.commit()
        finally:
            cls.db.cursor().close()


def get_config():
    SiteConfig.db = get_db()
    return SiteConfig.all()


def update_config(data):
    SiteConfig.db = get_db()
    SiteConfig.update_config(data)


def update_maintenance(maintenance):
    SiteConfig.db = get_db()
    SiteConfig.update_maintenancee(maintenance)
