from flask import Blueprint, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from monitor.backend.repositories.users import find_user
from monitor.backend.rules import json_object
from monitor.backend.authentication import current_user, require_login
from monitor.backend.db import connect_db

blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")
DUMMY_HASH = generate_password_hash("unusable-account-placeholder")


@blueprint.post("/login")
def login():
    session.clear()
    data = json_object()
    username, password = data.get("username"), data.get("password")
    if not isinstance(username, str) or not username.strip() or not isinstance(password, str) or not password.strip():
        return jsonify(error="아이디와 비밀번호를 입력해 주세요."), 400
    user = find_user(username.strip())
    matches = check_password_hash(user["password_hash"] if user else DUMMY_HASH, password)
    if user is None or not matches:
        return jsonify(error="아이디 또는 비밀번호가 올바르지 않습니다."), 401
    session["user_id"] = user["id"]
    session.permanent = True
    return jsonify(user={key: user[key] for key in ("id", "username", "name")})


@blueprint.get("/me")
def me():
    with connect_db() as conn:
        conn.execute("SELECT 1").fetchone()
    return jsonify(user=current_user())


@blueprint.post("/logout")
def logout():
    session.clear()
    return jsonify(message="로그아웃했습니다.")
