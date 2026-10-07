from datetime import datetime
import math
from flask import Blueprint, jsonify
from monitor.backend.repositories import events
from monitor.backend.rules import json_object

blueprint = Blueprint("events", __name__, url_prefix="/api/events")


@blueprint.get("")
def index():
    return jsonify(events=events.list_events())


@blueprint.post("")
def collect():
    data = json_object()
    method, path, status, duration = (data.get(key) for key in ("method", "path", "status_code", "duration_ms"))
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
    ):
        return jsonify(error="요청 기록 형식이 올바르지 않습니다."), 400
    return jsonify(event=events.create_event(timestamp, method.upper(), path, status, duration)), 201
