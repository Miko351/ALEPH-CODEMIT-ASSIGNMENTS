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


def create_app(config: dict | None = None) -> Flask:
    load_dotenv(Path(__file__).with_name(".env"), override=False)
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL=os.getenv("DATABASE_URL"),
        DB_HOST=os.getenv("DB_HOST", "general-db"),
        DB_PORT=os.getenv("DB_PORT", "5432"),
        DB_NAME=os.getenv("DB_NAME", "general"),
        DB_USER=os.getenv("DB_USER", "general"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        SECRET_KEY=os.getenv("SECRET_KEY"),
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
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(posts_blueprint)
    register_request_logging(app)

    @app.get("/health")
    def health():
        with connect_db() as conn:
            conn.execute("SELECT 1").fetchone()
        return jsonify(status="ok")

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


if __name__ == "__main__":
    create_app().run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), debug=False)
