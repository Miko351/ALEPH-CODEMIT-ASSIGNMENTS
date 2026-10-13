"""Prepare the public classroom account without replacing existing accounts."""
import argparse
import os
from werkzeug.security import generate_password_hash
from app import create_app
from repositories.users import create_user


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='student')
    parser.add_argument('--name', default='학생')
    args = parser.parse_args()
    password = os.getenv('PRACTICE_PASSWORD', 'Learn123!')
    with create_app().app_context():
        user = create_user(args.username, args.name, generate_password_hash(password))
    print('Created account: ' + args.username if user else 'Account already exists; unchanged: ' + args.username)


if __name__ == '__main__':
    main()
