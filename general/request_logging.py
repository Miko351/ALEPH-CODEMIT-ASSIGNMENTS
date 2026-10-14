"""Record request metadata and forward it to a configurable monitor."""
from datetime import datetime, timezone
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import time

from flask import g, request
import requests


def register_request_logging(app) -> None:
    logger = logging.Logger(f"board.requests.{id(app)}", level=logging.INFO)
    log_path = Path(app.config["REQUEST_LOG_PATH"])
    if not log_path.is_absolute():
        log_path = Path(app.root_path) / log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=2, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    app.extensions["request_logger"] = logger

    @app.before_request
    def start_timer():
        g.request_started = time.perf_counter()

def record_request(response):
    from flask import current_app
    app = current_app
    event = {
        "event_kind": g.get("event_kind", "request"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "duration_ms": round((time.perf_counter() - g.request_started) * 1000, 2),
    }
    # stdout and HTTP delivery are separate; neither logs passwords or bodies.
    serialized = json.dumps(event, ensure_ascii=False)
    print(serialized, flush=True)
    app.extensions["request_logger"].info(serialized)
    monitor_url = app.config.get("MONITOR_URL") if request.path != "/health" else None
    if monitor_url:
        try:
            result = requests.post(monitor_url, json=event, headers={"X-Event-Token": app.config["EVENT_TOKEN"]}, timeout=3)
            result.raise_for_status()
        except requests.RequestException:
            app.logger.warning("감시 서버로 요청 기록을 보내지 못했습니다.")
    return response
