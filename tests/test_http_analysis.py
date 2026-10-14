from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from monitor.backend.event_rules import make_event
from monitor.backend.learning.normalize import normalize_event, normalize_events
from monitor.backend.learning.http_rules import select_views, find_following_errors
from monitor.backend.learning.report import build_report
from monitor.backend.app import create_app

BASE = datetime(2026, 10, 14, 0, 0, tzinfo=timezone.utc)


def row(identifier, seconds=0, **changes):
    data = dict(id=identifier, occurred_at=BASE + timedelta(seconds=seconds), method='GET', path='/', status_code=200, event_type='post_list')
    data.update(changes)
    return data


def test_classification_uses_real_response_fields_not_supplied_label():
    assert make_event(dict(method='GET', path='/', status_code=200, event_type='attack'))['event_type'] == 'post_list'
    assert make_event(dict(method='GET', path='/training-missing', status_code=404))['event_type'] == 'request_error'
    assert make_event(dict(method='POST', path='/auth/login', status_code=401))['event_type'] == 'login_failure'
    assert make_event(dict(method='POST', path='/auth/login', status_code=200))['event_type'] == 'login_success'
    assert make_event(dict(method='GET', path='/', status_code=True)) is None


def test_normalization_preserves_original_id_timestamp_fields_and_404():
    original = row(17, 1, path='/training-missing', status_code=404, event_type='request_error')
    before = deepcopy(original)
    normalized = normalize_event(original)
    assert original == before
    assert normalized['id'] == 'http-17' and normalized['source_id'] == 17
    assert normalized['source'] == 'http_live' and normalized['kind'] == 'request_error'
    for key in ('occurred_at', 'method', 'path', 'status_code'):
        assert normalized[key] == original[key]
    assert 'ip' not in normalized and 'user' not in normalized


def test_selection_requires_all_four_conditions():
    records = normalize_events([row(1), row(2, method='POST'), row(3, path='/board/1'), row(4, status_code=404), row(5, event_type='http_request')])
    assert [entry['id'] for entry in select_views(records)] == ['http-1']


@pytest.mark.parametrize('count, threshold, candidate', [(4, 10, False), (10, 10, True), (12, 10, True), (12, 20, False)])
def test_count_boundary_context_and_evidence_share_selected_rows(count, threshold, candidate):
    records = [row(index + 1, index) for index in range(count)] + [row(count + 1, count, path='/training-missing', status_code=404, event_type='request_error')]
    card = build_report(records, threshold)['cards'][0]
    assert card['observed_value'] == count and card['is_candidate'] is candidate
    assert len(card['view_ids']) == count
    assert len(card['following_error_ids']) == 1
    assert len(card['evidence']) == len(card['records']) == count + 1
    assert card['evidence'] == [entry['id'] for entry in card['records']]
    other = build_report(records, 20 if threshold == 10 else 10)['cards'][0]
    assert card['evidence'] == other['evidence'] and card['observed_value'] == other['observed_value']


def test_error_time_limits_use_latest_receive_time_and_no_views_is_empty():
    normalized = normalize_events([row(1, 5), row(2, 3), *[row(index + 3, seconds, status_code=404, event_type='request_error') for index, seconds in enumerate((4, 5, 5.001, 35, 35.001))]])
    assert [entry['id'] for entry in find_following_errors(normalized, select_views(normalized))] == ['http-5', 'http-6']
    assert find_following_errors(normalized, []) == []
    card = build_report([row(1, status_code=404, event_type='request_error')])['cards'][0]
    assert card['observed_value'] == 0 and card['records'] == []


def test_api_auth_validation_and_fixed_reference():
    app = create_app({'TESTING': True})
    client = app.test_client()
    assert client.get('/api/analysis?after_id=0').status_code == 401
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['csrf_token'] = 'test-csrf'
    reference = BASE + timedelta(seconds=20)
    records = [row(index + 1, index) for index in range(12)] + [row(13, 12, path='/training-missing', status_code=404, event_type='request_error')]
    with patch('monitor.backend.authentication.find_user_by_id', return_value={'id': 1}), patch('monitor.backend.repositories.events.database_time', return_value=reference), patch('monitor.backend.repositories.events.last_id', return_value=13), patch('monitor.backend.learning.support.events.read_after', return_value=records) as read:
        assert client.get('/api/analysis?threshold=0&after_id=0').status_code == 400
        assert client.get('/api/analysis?threshold=1.5&after_id=0').status_code == 400
        assert client.get('/api/analysis?threshold=10&after_id=-1').status_code == 400
        assert client.get('/api/analysis?threshold=10&after_id=0&reference_time=not-a-date').status_code == 400
        assert client.post('/api/analysis/start').status_code == 403
        assert client.post('/api/analysis/start', headers={'X-CSRF-Token': 'test-csrf'}).json['after_id'] == 13
        first = client.get('/api/analysis?threshold=10&after_id=0').json
        second = client.get('/api/analysis', query_string=dict(threshold=20, after_id=first['after_id'], reference_time=first['reference_time'])).json
        assert first['reference_time'] == second['reference_time']
        assert first['cards'][0]['evidence'] == second['cards'][0]['evidence']
        assert first['cards'][0]['is_candidate'] and not second['cards'][0]['is_candidate']
        assert read.call_args.kwargs['reference_time'] == reference


def test_educational_sources_remain_separate(tmp_path):
    from monitor.backend.learning.educational_pcap import create_packets, summarize
    from monitor.backend.learning.ioc_example import match_indicator
    packets = create_packets()
    assert summarize(packets, 5) == {'seconds': 5, 'packet_count': 5, 'byte_sum': 360}
    assert summarize(packets, 1) == {'seconds': 1, 'packet_count': 2, 'byte_sum': 114}
    assert match_indicator('203.0.113.7', {'203.0.113.7'})
    assert not match_indicator('203.0.113.8', {'203.0.113.7'})
