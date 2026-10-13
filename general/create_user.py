"""Prepare the public classroom account without replacing existing accounts."""
import argparse
import os
from getpass import getpass
from werkzeug.security import generate_password_hash
from app import create_app
from repositories.users import create_user


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='student')
    parser.add_argument('--name', default='학생')
    args = parser.parse_args()
    password = os.getenv('ACCOUNT_PASSWORD')
    if password is None:
        password = getpass('Password (at least 8 characters): ')
        if getpass('Confirm password: ') != password:
            raise SystemExit('Passwords do not match.')
    if len(password) < 8 or not password.strip():
        raise SystemExit('Password must contain at least 8 characters.')
    with create_app().app_context():
        user = create_user(args.username, args.name, generate_password_hash(password))
    print('Created account: ' + args.username if user else 'Account already exists; unchanged: ' + args.username)


if __name__ == '__main__':
    main()
