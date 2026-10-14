import json
import re
from datetime import timedelta
from flask import Blueprint, jsonify, request
from monitor.backend.authentication import require_login
from monitor.backend.repositories import events
from monitor.backend.learning.normalize import event_time
from monitor.backend.learning.support import read_live, json_default
from monitor.backend.learning.report import build_report

blueprint = Blueprint('analysis', __name__, url_prefix='/api/analysis')
blueprint.before_request(require_login)


def integer_argument(name, minimum, maximum, default=None):
    value = request.args.get(name, default)
    if not isinstance(value, str) or not re.fullmatch(r'\d+', value) or len(value) > 19:
        raise ValueError(f'{name} must be an integer')
    number = int(value)
    if not minimum <= number <= maximum:
        raise ValueError(f'{name} is out of range')
    return number


@blueprint.post('/start')
def start():
    return jsonify(after_id=events.last_id(), reference_time=None, window_seconds=60,
                   message='이전 행을 삭제하지 않고 새 ID 경계로 관찰합니다.')


@blueprint.get('')
def analyze():
    try:
        threshold = integer_argument('threshold', 1, 10000, '10')
        after_id = integer_argument('after_id', 0, 9223372036854775807)
        now = events.database_time()
        supplied_time = request.args.get('reference_time')
        reference = now if supplied_time is None else event_time(supplied_time)
        if reference > now + timedelta(seconds=5):
            raise ValueError('reference_time cannot be in the future')
    except (ValueError, TypeError, AttributeError):
        return jsonify(error='기준은 1~10000의 정수, after_id는 0 이상의 정수, 기준시각은 시간대가 있는 ISO 시각이어야 합니다.'), 400
    rows = read_live(after_id, reference)
    report = build_report(rows, threshold)
    report.update(after_id=after_id, reference_time=reference.isoformat(), window_seconds=60)
    # Keep the DB receive timestamp explicit as ISO 8601, not a browser-generated time.
    return jsonify(json.loads(json.dumps(report, default=json_default)))
