from contextlib import contextmanager
import os
from pathlib import Path
import socket
import subprocess
import threading
import time
from uuid import uuid4

from dotenv import dotenv_values
import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
import pytest
import requests
from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server

from app import create_app as create_general
from monitor.backend.app import create_app
from monitor.backend.repositories.users import create_user

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def database():
    dsn = os.getenv("TEST_DATABASE_URL") or dotenv_values(ROOT / "monitor/backend/.env").get("DATABASE_URL")
    if not dsn:
        pytest.fail("Configure monitor/backend/.env or TEST_DATABASE_URL before tests.")
    schema = f"test_dashboard_{uuid4().hex}"
    with psycopg.connect(dsn) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    isolated = make_conninfo(dsn, options=f"-csearch_path={schema}")
    try:
        with psycopg.connect(isolated) as conn:
            for path in ("general/sql/001_posts.sql", "monitor/backend/sql/002_monitor.sql"):
                conn.execute((ROOT / path).read_text(encoding="utf-8"))
        yield isolated
    finally:
        assert schema.startswith("test_dashboard_") and len(schema) == 47
        with psycopg.connect(dsn) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture
def application(database):
    app = create_app({"TESTING": True, "DATABASE_URL": database})
    with app.app_context():
        create_user("tester", "테스트 운영자", generate_password_hash("temporary-test-password"))
    return app


@pytest.fixture
def client(application):
    return application.test_client()


@contextmanager
def serve(app):
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def services(application, database, tmp_path):
    with serve(application) as monitor_url:
        general = create_general({
            "TESTING": True, "DATABASE_URL": database,
            "MONITOR_URL": f"{monitor_url}/api/events", "REQUEST_LOG_PATH": str(tmp_path / "requests.log"),
        })
        try:
            with serve(general) as general_url:
                yield monitor_url, general_url
        finally:
            for handler in general.extensions["request_logger"].handlers:
                handler.close()


@pytest.fixture
def frontend(services, tmp_path):
    monitor_url, general_url = services
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    directory = ROOT / "monitor/frontend"
    env = {**os.environ, "MONITOR_API_TARGET": monitor_url, "VITE_GENERAL_URL": general_url}
    with (tmp_path / "vite.log").open("w", encoding="utf-8") as output:
        process = subprocess.Popen(
            ["node", "node_modules/vite/bin/vite.js", "--port", str(port)], cwd=directory,
            env=env, stdout=output, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        url = f"http://127.0.0.1:{port}"
        try:
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError("Vite exited before startup; check its test log.")
                try:
                    if requests.get(url, timeout=1).status_code == 200:
                        break
                except requests.RequestException:
                    time.sleep(0.2)
            else:
                raise RuntimeError("Vite startup timed out.")
            yield url, monitor_url, general_url
        finally:
            process.terminate()
            process.wait(timeout=10)
