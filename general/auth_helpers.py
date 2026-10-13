from flask import jsonify, session
from repositories.users import find_user_by_id


def api_access_error():
    user_id = session.get("user_id")
    if type(user_id) is not int or find_user_by_id(user_id) is None:
        return jsonify(error="로그인이 필요합니다."), 401
    return None
