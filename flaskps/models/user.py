class User(object):

    db = None

    @classmethod
    def all(cls):
        sql = 'SELECT * FROM usuarios'
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = """
            INSERT INTO usuarios (email, username, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()

        return True

    @classmethod
    def find_by_user_and_pass(cls, username, password):
        sql = """
            SELECT * FROM usuarios AS u
            WHERE u.username = %s AND u.password = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (username, password))

        return cursor.fetchone()

    @classmethod
    def find_by_user(cls, username):
        sql = """
            SELECT * FROM usuarios AS u
            WHERE u.username = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, username)

        return cursor.fetchone()
