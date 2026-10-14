"""Send real local requests and export only their received DB rows to stdout."""
import argparse
import json
import os
import sys
import time
import requests
from monitor.backend.app import app
from monitor.backend.repositories import events
from .support import json_default


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('count', type=int)
    args = parser.parse_args()
    if not 1 <= args.count <= 1000:
        raise SystemExit('count must be 1..1000')
    password = os.getenv('CAPTURE_PASSWORD')
    if not password:
        raise SystemExit('Set CAPTURE_PASSWORD in the process environment; never put it in submitted files.')
    base = os.getenv('GENERAL_URL', 'http://general-api:5000').rstrip('/')
    client = requests.Session()
    login = client.post(base + '/auth/login', json={'username': os.getenv('CAPTURE_USERNAME', 'student'), 'password': password}, timeout=10)
    if login.status_code != 200:
        raise SystemExit(f'General login failed with HTTP {login.status_code}; no observation was exported.')
    with app.app_context():
        after_id = events.last_id()
    for _ in range(args.count):
        response = client.get(base + '/', allow_redirects=False, timeout=10)
        if response.status_code != 200:
            raise SystemExit(f'Expected GET / 200, received {response.status_code}; no observation was exported.')
    missing = client.get(base + '/training-missing', allow_redirects=False, timeout=10)
    if missing.status_code != 404:
        raise SystemExit(f'Expected missing path 404, received {missing.status_code}.')
    for _ in range(20):
        with app.app_context():
            rows = events.read_after(after_id)
        if len(rows) >= args.count + 1:
            break
        time.sleep(0.25)
    views = [row for row in rows if row['method'] == 'GET' and row['path'] == '/' and row['status_code'] == 200 and row['event_type'] == 'post_list']
    errors = [row for row in rows if row['path'] == '/training-missing' and row['status_code'] == 404]
    if len(rows) != args.count + 1 or len(views) != args.count or len(errors) != 1:
        raise SystemExit('Unexpected received rows. Check event delivery and other traffic; repeat a fresh capture instead of editing data.')
    json.dump({'after_id': after_id, 'requested_views': args.count, 'records': rows}, sys.stdout, ensure_ascii=False, indent=2, default=json_default)
    sys.stdout.write('\n')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Capture failed: {type(error).__name__}. Check service settings/logs.', file=sys.stderr)
        raise SystemExit(1) from None
