"""Apply non-destructive preparation SQL to general and monitor databases."""
from pathlib import Path
import os
from dotenv import dotenv_values
import psycopg

ROOT = Path(__file__).resolve().parents[1]


def main():
    for service, filename in (("general", "001_posts.sql"), ("monitor/backend", "002_monitor.sql")):
        directory = ROOT / service
        dsn = os.getenv("DATABASE_URL") or dotenv_values(directory / ".env").get("DATABASE_URL")
        if not dsn:
            raise SystemExit(f"Configure {service}/.env first.")
        with psycopg.connect(dsn) as conn:
            if service == "general" and conn.execute("SELECT to_regclass('posts')").fetchone()[0] is not None:
                print("Existing posts table and sequence preserved.")
                continue
            conn.execute((directory / "sql" / filename).read_text(encoding="utf-8"))
            if service == "monitor/backend":
                conn.execute((directory / "sql" / "003_note_status.sql").read_text(encoding="utf-8"))
        print(f"Applied {service}/sql/{filename}; existing records preserved.")


if __name__ == "__main__":
    main()
