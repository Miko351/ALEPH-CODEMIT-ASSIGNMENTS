"""Application assembly and server entry point."""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template
import psycopg2
from werkzeug.exceptions import HTTPException

from request_logging import register_request_logging
from routes.posts import blueprint as posts_blueprint


def create_app(config: dict | None = None) -> Flask:
    load_dotenv(Path(__file__).with_name(".env"), override=False)
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL=os.getenv("DATABASE_URL"),
        MONITOR_URL=os.getenv("MONITOR_URL", ""),
        REQUEST_LOG_PATH=os.getenv("REQUEST_LOG_PATH", "instance/requests.log"),
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if config:
        app.config.update(config)
    app.register_blueprint(posts_blueprint)
    register_request_logging(app)

    @app.errorhandler(HTTPException)
    def http_error(error):
        message = "요청한 화면을 찾을 수 없습니다." if error.code == 404 else "요청을 처리할 수 없습니다."
        return render_template(
            "error.html", status_code=error.code, message=message,
            description="주소와 요청 내용을 확인한 뒤 다시 시도해 주세요.",
        ), error.code

    @app.errorhandler(psycopg2.Error)
    def database_error(error):
        app.logger.exception("PostgreSQL request failed")
        return render_template(
            "error.html", status_code=503, message="데이터베이스에 연결할 수 없습니다.",
            description="DB 서버와 연결 설정을 확인한 뒤 다시 시도해 주세요.",
        ), 503

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
