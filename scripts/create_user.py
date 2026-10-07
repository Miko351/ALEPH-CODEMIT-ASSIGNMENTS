"""Create a practice account with an interactive password, stored as a hash."""
import argparse
from getpass import getpass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from werkzeug.security import generate_password_hash
import psycopg
from monitor.backend.app import create_app
from monitor.backend.repositories.users import create_user


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    username, name = args.username.strip(), args.name.strip()
    if not username or not name:
        raise SystemExit("Username and name must not be blank.")
    password = getpass("Password (at least 8 characters): ")
    if not password.strip() or len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters.")
    if getpass("Confirm password: ") != password:
        raise SystemExit("Passwords do not match.")
    try:
        with create_app().app_context():
            user = create_user(username, name, generate_password_hash(password))
    except psycopg.errors.UniqueViolation:
        raise SystemExit("This username already exists. Choose another username.") from None
    print(f"Created user: {user['username']} ({user['name']}). Password was stored as a hash.")


if __name__ == "__main__":
    main()
