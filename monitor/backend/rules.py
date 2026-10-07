"""Validate JSON and share the same title/body rule for create and edit."""
from flask import request
from werkzeug.exceptions import BadRequest


def json_object():
    value = request.get_json(silent=True)
    if not isinstance(value, dict):
        raise BadRequest()
    return value


def validate_note(data):
    values, errors = {}, {}
    for key, label in (("title", "제목"), ("body", "내용")):
        value = data.get(key)
        values[key] = value.strip() if isinstance(value, str) else ""
        if not values[key]:
            errors[key] = f"{label}을 입력해 주세요. 공백만 입력할 수 없습니다."
    return values, errors
