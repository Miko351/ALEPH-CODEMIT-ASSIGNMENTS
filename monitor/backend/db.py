"""One connection function for every monitor repository."""
import psycopg
from psycopg.rows import dict_row
from flask import current_app


def connect_db():
    dsn = current_app.config.get("DATABASE_URL")
    if dsn:
        return psycopg.connect(dsn, row_factory=dict_row, connect_timeout=5)
    return psycopg.connect(
        host=current_app.config["DB_HOST"], port=current_app.config["DB_PORT"],
        dbname=current_app.config["DB_NAME"], user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"], row_factory=dict_row, connect_timeout=5,
    )
