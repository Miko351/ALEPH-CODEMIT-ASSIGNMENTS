"""PostgreSQL connection boundary; repositories use only connect_db()."""
import os

from flask import current_app
import psycopg


def connect_db() -> psycopg.Connection:
    database_url = current_app.config.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url, connect_timeout=5)
    return psycopg.connect(
        host=current_app.config["DB_HOST"], port=current_app.config["DB_PORT"],
        dbname=current_app.config["DB_NAME"], user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"], connect_timeout=5,
    )
