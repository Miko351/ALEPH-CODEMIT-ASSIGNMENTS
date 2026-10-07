from monitor.backend.db import connect_db


def find_user(username):
    with connect_db() as conn:
        return conn.execute(
            "SELECT id, username, name, password_hash FROM users WHERE username = %s",
            (username,),
        ).fetchone()


def create_user(username, name, password_hash):
    with connect_db() as conn:
        return conn.execute(
            "INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s) RETURNING id, username, name",
            (username, name, password_hash),
        ).fetchone()
