import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM list_user WHERE user_id = ?", (user_id,)
            ).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, first_name):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO list_user (user_id, first_name) VALUES (?, ?)",
                (
                    user_id,
                    first_name,
                ),
            )
