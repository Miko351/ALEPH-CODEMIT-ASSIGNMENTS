"""PostgreSQL connection boundary; repositories use only connect_db()."""
import os

from flask import current_app
import psycopg


def connect_db() -> psycopg.Connection:
    return psycopg.connect(
        host=current_app.config["DB_HOST"], port=current_app.config["DB_PORT"],
        dbname=current_app.config["DB_NAME"], user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"], sslmode=current_app.config["DB_SSLMODE"], connect_timeout=5,
    )
