"""Post SQL operations. Return data only; HTTP concerns belong to routes."""
from contextlib import closing

from db import connect_db


def _post(row) -> dict | None:
    return None if row is None else {"id": row[0], "title": row[1], "body": row[2]}


def list_posts() -> list[dict]:
    with closing(connect_db()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute("SELECT id, title, body FROM posts ORDER BY id ASC")
            return [_post(row) for row in cursor.fetchall()]


def find_post(post_id: int) -> dict | None:
    with closing(connect_db()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute("SELECT id, title, body FROM posts WHERE id = %s", (post_id,))
            return _post(cursor.fetchone())


def create_post(title: str, body: str) -> dict:
    with closing(connect_db()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO posts (title, body) VALUES (%s, %s) RETURNING id, title, body",
                (title, body),
            )
            return _post(cursor.fetchone())


def update_post(post_id: int, title: str, body: str) -> dict | None:
    with closing(connect_db()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute(
                "UPDATE posts SET title = %s, body = %s WHERE id = %s RETURNING id, title, body",
                (title, body, post_id),
            )
            return _post(cursor.fetchone())


def delete_post(post_id: int) -> dict | None:
    with closing(connect_db()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM posts WHERE id = %s RETURNING id, title, body", (post_id,)
            )
            return _post(cursor.fetchone())
