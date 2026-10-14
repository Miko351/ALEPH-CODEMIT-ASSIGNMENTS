from datetime import timedelta
from monitor.backend.db import connect_db

FIELDS = 'id, occurred_at, method, path, status_code, duration_ms, event_kind, event_type'


def list_events():
    with connect_db() as conn:
        return conn.execute(f'SELECT {FIELDS} FROM http_events ORDER BY id DESC').fetchall()


def create_event(event):
    # id (identity) and occurred_at (DB DEFAULT) are assigned at receipt/storage.
    legacy_kind = event['event_type'] if event['event_type'] in ('login_success', 'login_failure') else 'request'
    with connect_db() as conn:
        return conn.execute(
            'INSERT INTO http_events (method, path, status_code, duration_ms, event_kind, event_type) '
            'VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, occurred_at',
            (event['method'], event['path'], event['status_code'], event['duration_ms'], legacy_kind, event['event_type']),
        ).fetchone()


def last_id():
    with connect_db() as conn:
        return conn.execute('SELECT COALESCE(MAX(id), 0) AS last_id FROM http_events').fetchone()['last_id']


def database_time():
    with connect_db() as conn:
        return conn.execute('SELECT clock_timestamp() AS now').fetchone()['now']


def read_after(after_id, reference_time=None):
    with connect_db() as conn:
        if reference_time is None:
            return conn.execute(f'SELECT {FIELDS} FROM http_events WHERE id > %s ORDER BY id', (after_id,)).fetchall()
        return conn.execute(
            f'SELECT {FIELDS} FROM http_events WHERE id > %s AND occurred_at >= %s AND occurred_at <= %s ORDER BY id',
            (after_id, reference_time - timedelta(seconds=60), reference_time),
        ).fetchall()
