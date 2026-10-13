from monitor.backend.db import connect_db


def list_events():
    with connect_db() as conn:
        return conn.execute(
            "SELECT id, occurred_at, method, path, status_code, duration_ms, event_kind FROM events ORDER BY id DESC"
        ).fetchall()


def create_event(timestamp, method, path, status_code, duration_ms, event_kind="request"):
    with connect_db() as conn:
        return conn.execute(
            "INSERT INTO events (occurred_at, method, path, status_code, duration_ms, event_kind) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (timestamp, method, path, status_code, duration_ms, event_kind),
        ).fetchone()
