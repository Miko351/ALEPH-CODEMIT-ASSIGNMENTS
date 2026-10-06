"""Optional Windows-only portable PostgreSQL, scoped to this project's cache."""
import argparse
from contextlib import closing
import os
from pathlib import Path
import secrets
import subprocess
import sys
from tempfile import TemporaryFile
import urllib.request
import zipfile

from dotenv import dotenv_values
import psycopg2
from psycopg2 import sql

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
BIN = CACHE / "postgres" / "pgsql" / "bin"
DATA = CACHE / "pgdata"
PROFILE = CACHE / "portable.env"
ENV = ROOT / "mini-watch" / "general" / ".env"
PORT = 55432
# Windows x86-64 archive linked by EDB's official binary download page.
DOWNLOAD_URL = "https://sbp.enterprisedb.com/getfile.jsp?fileid=1260609"


def execute(program: str, *arguments: str, check: bool = True):
    # A background PostgreSQL child may retain inherited pipe handles on Windows.
    # A temporary file lets pg_ctl exit without waiting for the server to stop.
    with TemporaryFile() as output:
        result = subprocess.run(
            [str(BIN / program), *arguments], stdout=output, stderr=subprocess.STDOUT,
            check=False, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        output.seek(0)
        result.stdout = output.read().decode("utf-8", errors="replace")
        result.stderr = ""
    if check and result.returncode:
        raise RuntimeError(f"{program} failed:\n{result.stdout}\n{result.stderr}")
    return result


def download() -> None:
    if (BIN / "pg_ctl.exe").exists():
        return
    CACHE.mkdir(exist_ok=True)
    archive = CACHE / "postgresql-binaries.zip"
    if not archive.exists():
        print("Downloading official PostgreSQL Windows binaries...", flush=True)
        urllib.request.urlretrieve(DOWNLOAD_URL, archive)
    target = (CACHE / "postgres").resolve()
    target.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("PostgreSQL archive integrity check failed")
        for entry in bundle.infolist():
            if entry.filename.startswith(("pgsql/bin/", "pgsql/lib/", "pgsql/share/")):
                if not (target / entry.filename).resolve().is_relative_to(target):
                    raise RuntimeError("Unsafe archive path")
                bundle.extract(entry, target)


def is_running() -> bool:
    return DATA.exists() and execute("pg_ctl.exe", "-D", str(DATA), "status", check=False).returncode == 0


def start() -> None:
    if not (DATA / "PG_VERSION").exists():
        raise RuntimeError("Run setup first.")
    if not is_running():
        execute(
            "pg_ctl.exe", "-D", str(DATA), "-l", str(CACHE / "postgres.log"),
            "-o", f"-h 127.0.0.1 -p {PORT}", "-w", "start",
        )
    print(f"Project PostgreSQL is running on 127.0.0.1:{PORT}.")


def setup() -> None:
    download()
    if not PROFILE.exists():
        if (DATA / "PG_VERSION").exists():
            raise RuntimeError("Existing cluster has no credential profile; refusing to reset it.")
        PROFILE.write_text(f"POSTGRES_PASSWORD={secrets.token_urlsafe(32)}\n", encoding="utf-8")
    password = dotenv_values(PROFILE)["POSTGRES_PASSWORD"]
    if not (DATA / "PG_VERSION").exists():
        password_file = CACHE / f"initdb-password-{secrets.token_hex(8)}.tmp"
        try:
            password_file.write_text(password + "\n", encoding="utf-8")
            execute(
                "initdb.exe", "-D", str(DATA), "-U", "postgres", "-E", "UTF8",
                "--locale=C", "-A", "scram-sha-256", f"--pwfile={password_file}",
            )
        finally:
            password_file.unlink(missing_ok=True)
    start()
    with closing(psycopg2.connect(
        host="127.0.0.1", port=PORT, user="postgres", password=password, dbname="postgres"
    )) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ("mini_watch",))
            if cursor.fetchone() is None:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("mini_watch")))
    if not ENV.exists():
        ENV.write_text(
            f"DATABASE_URL=postgresql://postgres:{password}@127.0.0.1:{PORT}/mini_watch\n"
            "MONITOR_URL=http://127.0.0.1:5001/logs\n"
            "REQUEST_LOG_PATH=instance/requests.log\nPORT=5000\n",
            encoding="utf-8",
        )
        print("Created general/.env with independent local credentials.")
    else:
        print("Existing general/.env preserved.")


def main() -> None:
    if os.name != "nt":
        raise RuntimeError("Use your normal PostgreSQL installation on this platform.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["setup", "start", "stop", "status"])
    command = parser.parse_args().command
    if command == "setup":
        setup()
    elif command == "start":
        start()
    elif command == "stop":
        if is_running():
            execute("pg_ctl.exe", "-D", str(DATA), "-m", "fast", "-w", "stop")
        print("Project PostgreSQL stopped.")
    else:
        print("running" if is_running() else "stopped")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from None
