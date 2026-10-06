"""PostgreSQL connection boundary; repositories use only connect_db()."""
import os

from flask import current_app
import psycopg


def connect_db() -> psycopg.Connection:
    database_url = current_app.config.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL을 설정해 주세요. .env.example을 참고하세요.")
    return psycopg.connect(database_url, connect_timeout=5)
