"""Configure Flask, register API blueprints, and start the monitor service."""
import os
from datetime import timedelta
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import dotenv_values
from flask import Flask, jsonify
import psycopg
from werkzeug.exceptions import HTTPException
from monitor.backend.routes.auth import blueprint as auth_blueprint
from monitor.backend.routes.events import blueprint as events_blueprint
from monitor.backend.routes.notes import blueprint as notes_blueprint


def create_app(config=None):
    settings = dotenv_values(Path(__file__).with_name(".env"))
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL=os.getenv("DATABASE_URL") or settings.get("DATABASE_URL"),
        DB_HOST=os.getenv("DB_HOST", "monitor-db"),
        DB_PORT=os.getenv("DB_PORT", "5432"),
        DB_NAME=os.getenv("DB_NAME", "monitor"),
        DB_USER=os.getenv("DB_USER", "monitor"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        SECRET_KEY=os.getenv("SECRET_KEY") or settings.get("SECRET_KEY"),
        SESSION_COOKIE_NAME="mini_watch_session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_REFRESH_EACH_REQUEST=False,
        SESSION_COOKIE_SECURE=False,  # Local HTTP; enable this when serving HTTPS.
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if config:
        app.config.update(config)
    secret = app.config.get("SECRET_KEY")
    if not isinstance(secret, str) or len(secret) < 32 or secret.startswith("CHANGE_ME"):
        raise RuntimeError("먼저 scripts/configure_session.py를 실행해 SECRET_KEY를 준비하세요.")
    for blueprint in (auth_blueprint, events_blueprint, notes_blueprint):
        app.register_blueprint(blueprint)

    @app.errorhandler(HTTPException)
    def http_error(error):
        message = "요청한 자료를 찾을 수 없습니다." if error.code == 404 else "요청 형식이 올바르지 않습니다."
        return jsonify(error=message), error.code

    @app.errorhandler(psycopg.Error)
    def database_error(error):
        app.logger.exception("Monitor database request failed")
        return jsonify(error="데이터베이스 요청에 실패했습니다. 잠시 후 다시 시도하세요."), 503

    @app.errorhandler(RuntimeError)
    def configuration_error(error):
        app.logger.exception("Monitor configuration error")
        return jsonify(error="서버의 데이터베이스 설정을 확인해 주세요."), 503

    return app


if __name__ == "__main__":
    settings = dotenv_values(Path(__file__).with_name(".env"))
    create_app().run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), debug=False)
