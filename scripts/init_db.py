"""Initialize a fresh posts table without changing an existing Day3 table."""
from contextlib import closing
from pathlib import Path
import sys

GENERAL = Path(__file__).resolve().parents[1] / "mini-watch" / "general"
sys.path.insert(0, str(GENERAL))

from app import create_app
from db import connect_db


def main() -> None:
    application = create_app()
    with application.app_context(), closing(connect_db()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('posts')")
            if cursor.fetchone()[0] is not None:
                cursor.execute("SELECT id, title, body FROM posts LIMIT 0")
                print("Existing posts table preserved; no schema or sequence changes applied.")
                return
            cursor.execute((GENERAL / "sql" / "001_posts.sql").read_text(encoding="utf-8"))
            print("Created posts table and automatic ID sequence.")


if __name__ == "__main__":
    main()
