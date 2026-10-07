"""Validate JSON and share the same title/body rule for create and edit."""
from flask import request
from werkzeug.exceptions import BadRequest


def json_object():
    value = request.get_json(silent=True)
    if not isinstance(value, dict):
        raise BadRequest()
    return value


NOTE_STATUSES = {"pending", "in_progress", "completed"}


def validate_note(data, default_status="pending"):
    values, errors = {}, {}
    for key, label in (("title", "제목"), ("body", "내용")):
        value = data.get(key)
        values[key] = value.strip() if isinstance(value, str) else ""
        if not values[key]:
            errors[key] = f"{label}을 입력해 주세요. 공백만 입력할 수 없습니다."
    status = data.get("status", default_status)
    if not isinstance(status, str) or status not in NOTE_STATUSES:
        errors["status"] = "처리 상태는 확인 전, 확인 중, 완료 중에서 선택해 주세요."
    values["status"] = status
    return values, errors
