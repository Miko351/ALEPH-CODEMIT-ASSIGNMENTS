from datetime import datetime
import math
import hmac
from flask import Blueprint, jsonify, current_app, request
from monitor.backend.repositories import events
from monitor.backend.rules import json_object
from monitor.backend.authentication import require_login

blueprint = Blueprint("events", __name__, url_prefix="/api/events")


@blueprint.get("")
def index():
    rejection = require_login()
    if rejection is not None:
        return rejection
    return jsonify(events=events.list_events())


@blueprint.post("")
def collect():
    received = request.headers.get("X-Event-Token", "")
    if not hmac.compare_digest(received.encode(), current_app.config["EVENT_TOKEN"].encode()):
        return jsonify(error="기록 전송 권한이 없습니다."), 401
    data = json_object()
    method, path, status, duration = (data.get(key) for key in ("method", "path", "status_code", "duration_ms"))
    event_kind = data.get("event_kind", "request")
    try:
        timestamp = datetime.fromisoformat(data.get("timestamp", ""))
    except (ValueError, TypeError):
        return jsonify(error="요청 기록 시각이 올바르지 않습니다."), 400
    if (
        timestamp.tzinfo is None
        or not isinstance(method, str) or not method.strip() or len(method) > 20
        or not isinstance(path, str) or not path.startswith("/")
        or type(status) is not int or not 100 <= status <= 599
        or type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0
        or event_kind not in ("request", "login_success", "login_failure")
    ):
        return jsonify(error="요청 기록 형식이 올바르지 않습니다."), 400
    if (event_kind == "login_failure" and status != 401) or (event_kind == "login_success" and status != 200):
        return jsonify(error="로그인 기록 종류와 상태 코드가 맞지 않습니다."), 400
    return jsonify(event=events.create_event(timestamp, method.upper(), path, status, duration, event_kind)), 201
