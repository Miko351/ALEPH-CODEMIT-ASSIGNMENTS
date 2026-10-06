"""Initialize a fresh posts table without changing an existing Day3 table."""
from pathlib import Path
import sys

GENERAL = Path(__file__).resolve().parents[1] / "mini-watch" / "general"
sys.path.insert(0, str(GENERAL))

from app import create_app
from db import connect_db


def main() -> None:
    application = create_app()
    with application.app_context(), connect_db() as conn:
        if conn.execute("SELECT to_regclass('posts')").fetchone()[0] is not None:
            conn.execute("SELECT id, title, body FROM posts LIMIT 0")
            print("Existing posts table preserved; no schema or sequence changes applied.")
            return
        conn.execute((GENERAL / "sql" / "001_posts.sql").read_text(encoding="utf-8"))
        print("Created posts table and automatic ID sequence.")


if __name__ == "__main__":
    main()
