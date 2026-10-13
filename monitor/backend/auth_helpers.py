import hmac
import secrets
from flask import request, session, jsonify


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def csrf_error():
    expected = session.get("csrf_token")
    received = request.headers.get("X-CSRF-Token")
    if not isinstance(expected, str) or not isinstance(received, str) or not hmac.compare_digest(expected.encode(), received.encode()):
        return jsonify(error="요청 확인 값이 올바르지 않습니다. 새로고침 후 다시 시도해 주세요."), 403
    return None
