"""Classify actual response metadata, never trust a caller's analysis label."""
import math


def make_event(data):
    if not isinstance(data, dict):
        return None
    method, path, status = (data.get(key) for key in ('method', 'path', 'status_code'))
    duration = data.get('duration_ms', 0)
    if (not isinstance(method, str) or not method.strip() or len(method) > 20
            or not isinstance(path, str) or not path.startswith('/') or len(path) > 2048
            or type(status) is not int or not 100 <= status <= 599
            or type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0):
        return None
    method = method.upper()
    if method == 'POST' and path == '/auth/login' and status in (200, 401):
        kind = 'login_success' if status == 200 else 'login_failure'
    elif method == 'GET' and path == '/' and status == 200:
        kind = 'post_list'
    elif status >= 400:
        kind = 'request_error'
    else:
        kind = 'http_request'
    return dict(method=method, path=path, status_code=status, duration_ms=duration, event_type=kind)
