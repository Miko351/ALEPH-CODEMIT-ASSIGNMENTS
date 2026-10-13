"""Prepare the public classroom account without replacing existing accounts."""
import argparse
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from werkzeug.security import generate_password_hash
from monitor.backend.app import create_app
from monitor.backend.db import connect_db


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='operator')
    parser.add_argument('--name', default='운영자')
    args = parser.parse_args()
    with create_app().app_context(), connect_db() as conn:
        user = conn.execute(
            'INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s) '
            'ON CONFLICT (username) DO NOTHING RETURNING id',
            (args.username, args.name, generate_password_hash(os.getenv('PRACTICE_PASSWORD', 'Learn123!'))),
        ).fetchone()
    print('Created account: ' + args.username if user else 'Account already exists; unchanged: ' + args.username)


if __name__ == '__main__':
    main()
