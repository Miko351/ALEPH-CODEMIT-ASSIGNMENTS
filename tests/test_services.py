"""Real PostgreSQL tests; uses two NEW test DBs, never the existing projects' DBs."""
import importlib.util
import os
from pathlib import Path
import sys
from uuid import uuid4
from unittest.mock import patch

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo, conninfo_to_dict
import pytest
from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'general'))
from app import create_app as create_general
from monitor.backend.app import create_app as create_monitor


@pytest.fixture(scope='module')
def databases():
    admin = os.getenv('TEST_ADMIN_DSN')
    if not admin:
        pytest.skip('TEST_ADMIN_DSN is required for real PostgreSQL tests')
    suffix = uuid4().hex[:10]
    urls = {}
    with psycopg.connect(admin, autocommit=True, connect_timeout=5) as conn:
        for role in ('general', 'monitor'):
            name = f'compose_{role}_test_{suffix}'
            conn.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
            urls[role] = make_conninfo(admin, dbname=name)
            folder = 'general' if role == 'general' else 'monitor/backend'
            with psycopg.connect(urls[role]) as database:
                database.execute((ROOT / folder / 'sql/docker-init.sql').read_text())
                database.execute(
                    'INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s)',
                    ('student' if role == 'general' else 'operator', role, generate_password_hash('Learn123!')),
                )
    # Retain test DBs so persistence can also be inspected. No DROP or production writes.
    return urls


def monitor_app(dsn):
    return create_monitor({'TESTING': True, **db_config(dsn), 'SECRET_KEY': 'test-monitor-session-key-of-32-characters'})


def db_config(dsn):
    values = conninfo_to_dict(dsn)
    return {name: values.get(key, default) for name, key, default in (
        ('DB_HOST', 'host', 'localhost'), ('DB_PORT', 'port', '5432'),
        ('DB_NAME', 'dbname', 'postgres'), ('DB_USER', 'user', ''),
        ('DB_PASSWORD', 'password', ''), ('DB_SSLMODE', 'sslmode', 'prefer'),
    )}


def test_login_events_notes_and_app_restart(databases, tmp_path):
    monitor = monitor_app(databases['monitor']).test_client()
    general = create_general({
        'TESTING': True, **db_config(databases['general']),
        'SECRET_KEY': 'test-general-session-key-of-32-characters',
        'MONITOR_URL': 'http://monitor-api:5000/api/events',
        'REQUEST_LOG_PATH': str(tmp_path / 'requests.log'),
    }).test_client()
    assert monitor.get('/api/auth/me').status_code == 200
    assert monitor.get('/api/auth/me').json['user'] is None
    assert monitor.get('/api/notes').status_code == 401
    assert general.get('/').status_code == 303

    class Delivered:
        def raise_for_status(self):
            pass

    def deliver(url, json, timeout, headers):
        assert url == 'http://monitor-api:5000/api/events'
        assert 'password' not in json
        assert monitor.post('/api/events', json=json, headers=headers).status_code == 201
        return Delivered()

    with patch('request_logging.requests.post', side_effect=deliver):
        assert general.post('/auth/login', json={'username': 'student', 'password': 'wrong'}).status_code == 401
        assert general.post('/auth/login', json={'username': 'student', 'password': 'Learn123!'}).status_code == 200
        assert general.get('/').status_code == 200
        saved = general.post('/board/new', data={'title': 'Compose 게시글', 'body': 'DB에 저장'})
        assert saved.status_code == 303
        assert general.get(saved.location).status_code == 200
    csrf = monitor.get('/api/auth/me').json['csrf_token']
    login = monitor.post('/api/auth/login', json={'username': 'operator', 'password': 'Learn123!'}, headers={'X-CSRF-Token': csrf})
    assert login.status_code == 200
    headers = {'X-CSRF-Token': login.json['csrf_token']}
    events = monitor.get('/api/events').json['events']
    assert any(item['event_kind'] == 'login_failure' and item['status_code'] == 401 for item in events)
    assert any(item['event_kind'] == 'login_success' and item['status_code'] == 200 for item in events)
    saved = monitor.post('/api/notes', json={'title': 'Docker 점검', 'body': '로그인 실패와 성공을 확인했다'}, headers=headers)
    assert saved.status_code == 201
    note_id = saved.json['note']['id']
    assert monitor.put(f'/api/notes/{note_id}', json={'title': ' ', 'body': '내용'}, headers=headers).status_code == 400
    assert monitor.get(f'/api/notes/{note_id}').json['note']['title'] == 'Docker 점검'
    restarted = monitor_app(databases['monitor']).test_client()
    csrf = restarted.get('/api/auth/me').json['csrf_token']
    login = restarted.post('/api/auth/login', json={'username': 'operator', 'password': 'Learn123!'}, headers={'X-CSRF-Token': csrf})
    assert login.status_code == 200
    assert restarted.get(f'/api/notes/{note_id}').json['note']['body'] == '로그인 실패와 성공을 확인했다'
    assert len(restarted.get('/api/events').json['events']) == len(events)
    assert restarted.delete(f'/api/notes/{note_id}', headers={'X-CSRF-Token': login.json['csrf_token']}).status_code == 200
    assert restarted.get(f'/api/notes/{note_id}').status_code == 404
