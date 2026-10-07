"""One connection function for every monitor repository."""
import psycopg
from psycopg.rows import dict_row
from flask import current_app


def connect_db():
    dsn = current_app.config.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("monitor/backend/.env의 DATABASE_URL을 설정하세요.")
    return psycopg.connect(dsn, row_factory=dict_row, connect_timeout=5)
