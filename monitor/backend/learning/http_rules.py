from .normalize import event_time


def select_views(rows):
    return [row for row in rows if row.get('method') == 'GET' and row.get('path') == '/'
            and row.get('status_code') == 200 and row.get('kind') == 'post_list']


def find_following_errors(rows, views):
    if not views:
        return []
    last_received = max(event_time(row['occurred_at']) for row in views)
    return [row for row in rows if row.get('status_code') == 404
            and 0 < (event_time(row['occurred_at']) - last_received).total_seconds() <= 30]
