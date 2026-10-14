from datetime import datetime


def event_time(value):
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('A timezone-aware DB receive timestamp is required.')
    return parsed


def normalize_event(original):
    identifier = original['id']
    if type(identifier) is not int or identifier <= 0:
        raise ValueError('A positive original DB ID is required.')
    event_time(original['occurred_at'])
    row = original.copy()
    row.update(id=f'http-{identifier}', source_id=identifier, source='http_live', kind=original['event_type'])
    return row


def normalize_events(rows):
    return [normalize_event(row) for row in rows]
