"""Check the signed session and look up the current account in PostgreSQL."""
from flask import g, jsonify, session
from monitor.backend.repositories.users import find_user_by_id
from monitor.backend.auth_helpers import csrf_error
from flask import request


def current_user():
    if "current_user" not in g:
        user_id = session.get("user_id")
        g.current_user = find_user_by_id(user_id) if type(user_id) is int else None
        if g.current_user is None and session:
            session.clear()
    return g.current_user


def require_login():
    if current_user() is None:
        return jsonify(error="로그인이 필요합니다. 다시 로그인해 주세요."), 401
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        return csrf_error()
    return None
