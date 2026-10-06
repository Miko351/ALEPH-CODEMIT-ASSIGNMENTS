from contextlib import closing
import os
from pathlib import Path
from uuid import uuid4

from dotenv import dotenv_values
import psycopg2
from psycopg2 import extensions, sql
import pytest

from app import create_app

ROOT = Path(__file__).resolve().parents[1]
GENERAL = ROOT / "mini-watch" / "general"


@pytest.fixture
def application(tmp_path):
    dsn = os.getenv("TEST_DATABASE_URL") or dotenv_values(GENERAL / ".env").get("DATABASE_URL")
    if not dsn:
        pytest.fail("Set TEST_DATABASE_URL or configure general/.env before PostgreSQL tests.")
    schema = f"test_posts_{uuid4().hex}"
    with closing(psycopg2.connect(dsn)) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    isolated_dsn = extensions.make_dsn(dsn, options=f"-csearch_path={schema}")
    with closing(psycopg2.connect(isolated_dsn)) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute((GENERAL / "sql" / "001_posts.sql").read_text(encoding="utf-8"))
    application = create_app({
        "TESTING": True,
        "DATABASE_URL": isolated_dsn,
        "MONITOR_URL": "",
        "REQUEST_LOG_PATH": str(tmp_path / "requests.log"),
    })
    yield application
    for handler in application.extensions["request_logger"].handlers:
        handler.close()
    # Drop only this test's newly created random schema; never touch public posts.
    assert schema.startswith("test_posts_") and len(schema) == len("test_posts_") + 32
    with closing(psycopg2.connect(dsn)) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture
def client(application):
    return application.test_client()


@pytest.fixture
def rows(application):
    def fetch():
        with closing(psycopg2.connect(application.config["DATABASE_URL"])) as connection:
            with connection, connection.cursor() as cursor:
                cursor.execute("SELECT id, title, body FROM posts ORDER BY id ASC")
                return cursor.fetchall()
    return fetch
