from pathlib import Path
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'general'))
from app import create_app as create_general
from monitor.backend.app import create_app as create_monitor
from observability import remove_request_secrets, configure_errors


def general_app(**config):
    return create_general({'TESTING': True, 'MONITOR_URL': '', 'REQUEST_LOG_PATH': str(ROOT / '.cache/unit-requests.log'), **config})


def test_health_does_not_claim_database_connection():
    with patch('db.psycopg.connect', side_effect=RuntimeError('DB offline')):
        assert general_app().test_client().get('/health').status_code == 200
        assert create_monitor({'TESTING': True}).test_client().get('/health').status_code == 200


def test_sentry_test_is_gated_and_reproduces_error():
    assert general_app().test_client().get('/api/sentry-test').status_code == 404
    app = general_app(ENABLE_SENTRY_TEST=True)
    client = app.test_client()
    assert client.get('/api/sentry-test').status_code == 401
    with client.session_transaction() as session:
        session['user_id'] = 1
    with patch('auth_helpers.find_user_by_id', return_value={'id': 1}):
        with pytest.raises(ZeroDivisionError):
            client.get('/api/sentry-test')


def test_sentry_removes_sensitive_fields_and_configures_service(monkeypatch):
    original = {'request': {'data': 'private body', 'cookies': {'session': 'private'}, 'headers': {'token': 'private'}, 'query_string': 'private'}, 'user': {'email': 'private'}}
    clean = remove_request_secrets(original, {})
    assert clean['request'] == {} and 'user' not in clean
    monkeypatch.setenv('SENTRY_DSN', 'https://public@example.invalid/1')
    monkeypatch.setenv('SENTRY_ENVIRONMENT', 'mini-general')
    monkeypatch.setenv('APP_VERSION', 'test-release')
    with patch('observability.sentry_sdk.init') as initialize, patch('observability.sentry_sdk.set_tag') as tag:
        configure_errors('mini-general')
        options = initialize.call_args.kwargs
        assert options['environment'] == 'mini-general'
        assert options['release'] == 'test-release'
        assert options['send_default_pii'] is False
        assert options['include_local_variables'] is False
        assert options['max_request_body_size'] == 'never'
        assert options['before_send'] == remove_request_secrets
        tag.assert_called_once_with('service', 'mini-general')


def test_event_token_and_csrf_are_required():
    app = create_monitor({'TESTING': True})
    client = app.test_client()
    event = {'timestamp': '2026-10-13T00:00:00+00:00', 'method': 'POST', 'path': '/auth/login', 'status_code': 401, 'duration_ms': 1, 'event_kind': 'login_failure'}
    assert client.post('/api/events', json=event).status_code == 401
    with patch('monitor.backend.repositories.events.create_event', return_value={'id': 1}):
        assert client.post('/api/events', json=event, headers={'X-Event-Token': app.config['EVENT_TOKEN']}).status_code == 201
    assert client.post('/api/auth/login', json={'username': 'operator', 'password': 'fake'}).status_code == 403
    token = client.get('/api/auth/me').json['csrf_token']
    assert token
    with patch('monitor.backend.routes.auth.find_user', return_value=None):
        assert client.post('/api/auth/login', json={'username': 'operator', 'password': 'fake'}, headers={'X-CSRF-Token': token}).status_code == 401


@pytest.mark.parametrize('role', ['general', 'monitor'])
def test_database_uses_all_six_config_fields(role):
    settings = {'DB_HOST': f'{role}-pooler.example.invalid', 'DB_PORT': '5432', 'DB_NAME': 'postgres', 'DB_USER': f'postgres.{role}_ref', 'DB_PASSWORD': 'test-only-placeholder', 'DB_SSLMODE': 'require'}
    app = general_app(**settings) if role == 'general' else create_monitor(settings)
    module = 'db' if role == 'general' else 'monitor.backend.db'
    with app.app_context(), patch(f'{module}.psycopg.connect') as connect:
        if role == 'general':
            from db import connect_db
        else:
            from monitor.backend.db import connect_db
        connect_db()
        assert connect.call_args.kwargs['host'] == settings['DB_HOST']
        assert connect.call_args.kwargs['port'] == '5432'
        assert connect.call_args.kwargs['dbname'] == 'postgres'
        assert connect.call_args.kwargs['user'] == settings['DB_USER']
        assert connect.call_args.kwargs['password'] == settings['DB_PASSWORD']
        assert connect.call_args.kwargs['sslmode'] == 'require'
