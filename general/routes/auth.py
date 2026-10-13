from flask import Blueprint, g, jsonify, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from repositories.users import find_user

blueprint = Blueprint("auth", __name__)
DUMMY_HASH = generate_password_hash("unusable-account-placeholder")


@blueprint.get("/login")
def login_page():
    return render_template("login.html")


@blueprint.post("/auth/login")
def login():
    session.clear()
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON 형식으로 입력해 주세요."), 400
    username, password = data.get("username"), data.get("password")
    if not isinstance(username, str) or not username.strip() or not isinstance(password, str) or not password.strip():
        return jsonify(error="아이디와 비밀번호를 입력해 주세요."), 400
    user = find_user(username.strip())
    matches = check_password_hash(user["password_hash"] if user else DUMMY_HASH, password)
    if user is None or not matches:
        g.event_kind = "login_failure"
        return jsonify(error="아이디 또는 비밀번호가 올바르지 않습니다."), 401
    session["user_id"] = user["id"]
    session["name"] = user["name"]
    g.event_kind = "login_success"
    return jsonify(user={key: user[key] for key in ("id", "username", "name")}, redirect=url_for("posts.index"))


@blueprint.post("/auth/logout")
def logout():
    session.clear()
    return jsonify(message="로그아웃했습니다.")
