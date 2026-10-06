"""Standalone sample monitor for the newly created project."""
import json
import os
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request


def create_app(log_path: str | Path | None = None) -> Flask:
    app = Flask(__name__)
    destination = Path(log_path or Path(__file__).with_name("requests.jsonl"))
    lock = Lock()

    @app.route("/logs", methods=["GET", "POST"])
    def logs():
        if request.method == "POST":
            event = request.get_json(silent=True)
            if not isinstance(event, dict) or not {"method", "path", "status_code"}.issubset(event):
                return jsonify(error="Invalid request event"), 400
            destination.parent.mkdir(parents=True, exist_ok=True)
            with lock, destination.open("a", encoding="utf-8") as file:
                file.write(json.dumps(event, ensure_ascii=False) + "\n")
            return jsonify(status="collected"), 201
        with lock:
            records = destination.read_text(encoding="utf-8").splitlines() if destination.exists() else []
        return jsonify([json.loads(line) for line in records[-100:]])

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.getenv("MONITOR_PORT", "5001")), debug=False)
