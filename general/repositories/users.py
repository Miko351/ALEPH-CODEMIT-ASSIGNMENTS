from psycopg.rows import dict_row
from db import connect_db


def find_user(username):
    with connect_db() as conn, conn.cursor(row_factory=dict_row) as cursor:
        return cursor.execute(
            "SELECT id, username, name, password_hash FROM users WHERE username = %s",
            (username,),
        ).fetchone()


def create_user(username, name, password_hash):
    with connect_db() as conn, conn.cursor(row_factory=dict_row) as cursor:
        return cursor.execute(
            "INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s) "
            "ON CONFLICT (username) DO NOTHING RETURNING id, username",
            (username, name, password_hash),
        ).fetchone()
