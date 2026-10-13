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


def find_user_by_id(user_id):
    with connect_db() as conn:
        return conn.execute("SELECT id, username, name FROM users WHERE id = %s", (user_id,)).fetchone()
