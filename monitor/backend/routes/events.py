from datetime import datetime
import math
import hmac
from flask import Blueprint, jsonify, current_app, request
from monitor.backend.repositories import events
from monitor.backend.rules import json_object
from monitor.backend.authentication import require_login
from monitor.backend.event_rules import make_event

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
    event = make_event(json_object())
    if event is None:
        return jsonify(error="요청 기록 형식이 올바르지 않습니다."), 400
    return jsonify(event=events.create_event(event)), 201
