"""Application assembly and server entry point."""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import psycopg
from werkzeug.exceptions import HTTPException

from request_logging import register_request_logging
from routes.posts import blueprint as posts_blueprint
from routes.auth import blueprint as auth_blueprint
from db import connect_db
from auth_helpers import api_access_error
from observability import configure_errors


def create_app(config: dict | None = None) -> Flask:
    load_dotenv(Path(__file__).with_name(".env"), override=False, interpolate=False)
    app = Flask(__name__)
    app.config.from_mapping(
        DB_HOST=os.getenv("DB_HOST", "general-db"),
        DB_PORT=os.getenv("DB_PORT", "5432"),
        DB_NAME=os.getenv("DB_NAME", "general"),
        DB_USER=os.getenv("DB_USER", "general"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        DB_SSLMODE=os.getenv("DB_SSLMODE", "prefer"),
        SECRET_KEY=os.getenv("SECRET_KEY"),
        EVENT_TOKEN=os.getenv("EVENT_TOKEN", ""),
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
        ENABLE_SENTRY_TEST=os.getenv("ENABLE_SENTRY_TEST", "false").lower() == "true",
        SESSION_COOKIE_NAME="general_watch_session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        MONITOR_URL=os.getenv("MONITOR_URL", ""),
        REQUEST_LOG_PATH=os.getenv("REQUEST_LOG_PATH", "instance/requests.log"),
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if config:
        app.config.update(config)
    if not app.config.get("SECRET_KEY") or len(app.config["SECRET_KEY"]) < 32:
        raise RuntimeError("SECRET_KEY를 32자 이상으로 설정하세요. Compose에는 실습값이 제공됩니다.")
    if len(app.config["EVENT_TOKEN"]) < 32 or app.config["EVENT_TOKEN"].startswith("CHANGE_ME"):
        raise RuntimeError("EVENT_TOKEN을 32자 이상의 별도 값으로 설정하세요.")
    configure_errors("mini-general")
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(posts_blueprint)
    register_request_logging(app)

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="general")

    @app.get("/api/sentry-test")
    def sentry_test():
        from flask import abort
        if not app.config["ENABLE_SENTRY_TEST"]:
            abort(404)
        error = api_access_error()
        if error is not None:
            return error
        # The test endpoint now reports success instead of dividing by zero.
        result = 1
        return jsonify(result=result)

    @app.errorhandler(HTTPException)
    def http_error(error):
        message = "요청한 화면을 찾을 수 없습니다." if error.code == 404 else "요청을 처리할 수 없습니다."
        return render_template(
            "error.html", status_code=error.code, message=message,
            description="주소와 요청 내용을 확인한 뒤 다시 시도해 주세요.",
        ), error.code

    @app.errorhandler(psycopg.Error)
    def database_error(error):
        app.logger.exception("PostgreSQL request failed")
        return render_template(
            "error.html", status_code=503, message="데이터베이스에 연결할 수 없습니다.",
            description="DB 서버와 연결 설정을 확인한 뒤 다시 시도해 주세요.",
        ), 503

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), debug=False)
