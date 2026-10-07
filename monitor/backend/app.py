"""Configure Flask, register API blueprints, and start the monitor service."""
import os
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
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if config:
        app.config.update(config)
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
    create_app().run(host="127.0.0.1", port=int(os.getenv("PORT") or settings.get("PORT", "5200")), debug=False)
