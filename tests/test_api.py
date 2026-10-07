from datetime import datetime, timezone
import os
import subprocess
import sys

import psycopg
import pytest
import requests

from monitor.backend.app import create_app


def test_login_checks_db_hash_and_never_returns_password(client, database):
    response = client.post('/api/auth/login', json={'username': ' tester ', 'password': 'temporary-test-password'})
    assert response.status_code == 200
    assert response.json['user']['name'] == '테스트 운영자'
    assert set(response.json['user']) == {'id', 'username', 'name'}
    with psycopg.connect(database) as conn:
        stored = conn.execute('SELECT password_hash FROM users WHERE username = %s', ('tester',)).fetchone()[0]
    assert stored.startswith('scrypt:') and stored != 'temporary-test-password'


@pytest.mark.parametrize('username,password,status', [
    ('', '', 400), ('   ', 'password', 400), ('tester', ' \n ', 400),
    ('tester', 'wrong', 401), ('missing', 'temporary-test-password', 401),
    ("tester' OR 1=1 --", 'temporary-test-password', 401), (None, 1, 400),
])
def test_login_rejects_bad_inputs(client, username, password, status):
    response = client.post('/api/auth/login', json={'username': username, 'password': password})
    assert response.status_code == status and response.json['error']


def test_crud_and_persistence_across_process(client, database, application):
    assert client.get('/api/notes').json['notes'] == []
    response = client.post('/api/notes', json={'title': '  관찰 기록  ', 'body': '  첫 내용\n '})
    assert response.status_code == 201
    note = response.json['note']
    assert note['title'] == '관찰 기록' and note['body'] == '첫 내용'
    path = f"/api/notes/{note['id']}"
    assert client.get(path).json['note']['body'] == '첫 내용'
    assert client.get('/api/notes').json['notes'][0]['id'] == note['id']
    # Opening the edit/delete confirmation in React uses GET; no mutation here.
    assert client.get(path).json['note']['body'] == '첫 내용'
    response = client.put(path, json={'title': ' 바뀐 제목 ', 'body': ' 바뀐 내용 '})
    assert response.status_code == 200 and response.json['note']['title'] == '바뀐 제목'
    fresh_client = create_app({'TESTING': True, 'DATABASE_URL': database, 'SECRET_KEY': application.config['SECRET_KEY']}).test_client()
    fresh_client.set_cookie('mini_watch_session', client.get_cookie('mini_watch_session').value)
    assert fresh_client.get(path).json['note']['body'] == '바뀐 내용'
    code = 'import os; from monitor.backend.app import create_app; c=create_app().test_client(); c.set_cookie("mini_watch_session", os.environ["TEST_SESSION_COOKIE"]); r=c.get("' + path + '"); assert r.status_code==200; assert r.json["note"]["body"]=="바뀐 내용"; print("persisted")'
    result = subprocess.run([sys.executable, '-c', code], env={**os.environ, 'DATABASE_URL': database, 'SECRET_KEY': application.config['SECRET_KEY'], 'TEST_SESSION_COOKIE': client.get_cookie('mini_watch_session').value}, capture_output=True, text=True)
    assert result.returncode == 0 and 'persisted' in result.stdout
    other = client.post('/api/notes', json={'title': '보존할 글', 'body': '보존할 내용'}).json['note']
    assert client.delete(path).json['deleted_id'] == note['id']
    assert client.get(f"/api/notes/{other['id']}").status_code == 200
    assert [row['id'] for row in client.get('/api/notes').json['notes']] == [other['id']]
    for method in ('get', 'put', 'delete'):
        assert getattr(client, method)(path, json={'title': '제목', 'body': '내용'}).status_code == 404


@pytest.mark.parametrize('values', [
    {'title': '', 'body': '내용'}, {'title': ' \n\t ', 'body': '내용'},
    {'title': '제목', 'body': ''}, {'title': '제목', 'body': ' \n\t '},
    {'title': 3, 'body': '내용'}, {'title': '제목', 'body': None}, {},
])
def test_invalid_create_edit_never_change_data(client, values):
    existing = client.post('/api/notes', json={'title': '원래 제목', 'body': '원래 내용'}).json['note']
    response = client.post('/api/notes', json=values)
    assert response.status_code == 400 and response.json['fields']
    response = client.put(f"/api/notes/{existing['id']}", json=values)
    assert response.status_code == 400
    assert client.get('/api/notes').json['notes'][0]['title'] == '원래 제목'
    assert len(client.get('/api/notes').json['notes']) == 1
    assert client.get(f"/api/notes/{existing['id']}").json['note']['body'] == '원래 내용'


@pytest.mark.parametrize('method', ['get', 'put', 'delete'])
def test_missing_note_returns_404(client, method):
    response = getattr(client, method)('/api/notes/2147483647', json={'title': '', 'body': ''})
    assert response.status_code == 404 and response.json['error']


@pytest.mark.parametrize('path', ['/api/auth/login', '/api/notes', '/api/events'])
def test_non_object_json_returns_400(client, path):
    assert client.post(path, json=['invalid']).status_code == 400
    assert client.post(path, data='{', content_type='application/json').status_code == 400


def test_parameter_binding_keeps_sql_and_markup_as_data(client):
    title = "<script>alert(1)</script>' ; DROP TABLE notes; --"
    note = client.post('/api/notes', json={'title': title, 'body': 'safe'}).json['note']
    assert client.get(f"/api/notes/{note['id']}").json['note']['title'] == title
    assert len(client.get('/api/notes').json['notes']) == 1


def test_real_general_crud_forwards_requests_to_postgres(services, client):
    monitor_url, general_url = services
    assert requests.get(general_url, timeout=5).status_code == 200
    invalid = requests.post(general_url + '/board/new', data={'title': ' ', 'body': ' '}, timeout=5)
    assert invalid.status_code == 400
    response = requests.post(general_url + '/board/new', data={'title': '기존 게시판', 'body': '내용'}, allow_redirects=False, timeout=5)
    assert response.status_code == 303
    path = response.headers['Location']
    assert requests.get(general_url + path, timeout=5).status_code == 200
    assert requests.get(general_url + path + '/edit', timeout=5).status_code == 200
    assert requests.post(general_url + path + '/edit', data={'title': '수정 제목', 'body': '수정 내용'}, allow_redirects=False, timeout=5).status_code == 303
    assert requests.get(general_url + path + '/delete', timeout=5).status_code == 200
    assert requests.get(general_url + path, timeout=5).status_code == 200
    assert requests.post(general_url + path + '/delete', allow_redirects=False, timeout=5).status_code == 303
    for suffix in ('', '/edit', '/delete'):
        assert requests.get(general_url + path + suffix, timeout=5).status_code == 404
    with requests.Session() as browser:
        assert browser.post(monitor_url + '/api/auth/login', json={'username': 'tester', 'password': 'temporary-test-password'}, timeout=5).status_code == 200
        events = browser.get(monitor_url + '/api/events', timeout=5).json()['events']
    for method, event_path, status in [('GET', '/', 200), ('POST', '/board/new', 400), ('POST', '/board/new', 303), ('GET', path, 404)]:
        assert any(row['method'] == method and row['path'] == event_path and row['status_code'] == status for row in events)
    assert 'password' not in str(events)


def test_events_persist_and_malformed_record_is_rejected(client, database, application):
    record = {'timestamp': datetime.now(timezone.utc).isoformat(), 'method': 'GET', 'path': '/board/404', 'status_code': 404, 'duration_ms': 3.4}
    assert client.post('/api/events', json=record).status_code == 201
    fresh = create_app({'TESTING': True, 'DATABASE_URL': database, 'SECRET_KEY': application.config['SECRET_KEY']}).test_client()
    fresh.set_cookie('mini_watch_session', client.get_cookie('mini_watch_session').value)
    assert fresh.get('/api/events').json['events'][0]['status_code'] == 404
    for key, value in [('status_code', 999), ('method', ''), ('path', 'no-slash'), ('duration_ms', -1), ('timestamp', 'bad-date')]:
        assert client.post('/api/events', json={**record, key: value}).status_code == 400
    assert len(client.get('/api/events').json['events']) == 1


def test_database_failure_is_json_503(client, monkeypatch):
    def failed_connection():
        raise psycopg.OperationalError('simulated unavailable database')
    monkeypatch.setattr('monitor.backend.repositories.notes.connect_db', failed_connection)
    response = client.get('/api/notes')
    assert response.status_code == 503 and response.json['error']


@pytest.mark.parametrize('method,path', [
    ('get', '/api/events'), ('get', '/api/notes'), ('get', '/api/notes/1'),
    ('post', '/api/notes'), ('put', '/api/notes/1'), ('delete', '/api/notes/1'),
    ('get', '/api/auth/me'),
])
def test_anonymous_protected_apis_return_401(application, method, path):
    anonymous = application.test_client()
    response = getattr(anonymous, method)(path, json={'title': 'test', 'body': 'test', 'status': 'completed'})
    assert response.status_code == 401 and response.json['error']


def test_session_cookie_me_logout_and_tamper_protection(client, application):
    assert client.get('/api/auth/me').json['user']['username'] == 'tester'
    cookie = client.get_cookie('mini_watch_session')
    assert cookie.http_only and cookie.same_site == 'Lax'
    anonymous = application.test_client()
    anonymous.set_cookie('mini_watch_session', cookie.value + 'tampered')
    assert anonymous.get('/api/notes').status_code == 401
    assert client.post('/api/auth/logout').status_code == 200
    for path in ('/api/auth/me', '/api/events', '/api/notes'):
        assert client.get(path).status_code == 401


def test_session_expires_or_deleted_account_is_denied(client, database, application):
    from datetime import timedelta
    import time
    application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=-1)
    time.sleep(1.1)
    assert client.get('/api/notes').status_code == 401
    application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    assert client.post('/api/auth/login', json={'username': 'tester', 'password': 'temporary-test-password'}).status_code == 200
    with psycopg.connect(database) as conn:
        conn.execute('DELETE FROM users WHERE username = %s', ('tester',))
    assert client.get('/api/notes').status_code == 401


@pytest.mark.parametrize('status', ['pending', 'in_progress', 'completed'])
def test_note_status_create_update_and_restart_persistence(client, application, database, status):
    note = client.post('/api/notes', json={'title': '상태 관찰', 'body': '확인 내용', 'status': status}).json['note']
    assert note['status'] == status
    path = f"/api/notes/{note['id']}"
    for updated in ('in_progress', 'completed', 'pending'):
        result = client.put(path, json={'title': '상태 관찰', 'body': '확인 내용', 'status': updated})
        assert result.status_code == 200 and result.json['note']['status'] == updated
        assert client.get('/api/notes').json['notes'][0]['status'] == updated
    # Title/body-only updates preserve the current status.
    client.put(path, json={'title': '상태 관찰', 'body': '내용 변경', 'status': 'completed'})
    client.put(path, json={'title': '제목만 변경', 'body': '내용 변경'})
    with psycopg.connect(database) as conn:
        assert conn.execute('SELECT status FROM notes WHERE id = %s', (note['id'],)).fetchone()[0] == 'completed'
    fresh = create_app({'TESTING': True, 'DATABASE_URL': database, 'SECRET_KEY': application.config['SECRET_KEY']}).test_client()
    fresh.set_cookie('mini_watch_session', client.get_cookie('mini_watch_session').value)
    assert fresh.get(path).json['note']['status'] == 'completed'


@pytest.mark.parametrize('status', ['', 'unknown', None, 1, ['completed']])
def test_invalid_status_returns_400_and_preserves_db(client, status):
    note = client.post('/api/notes', json={'title': '보존', 'body': '내용', 'status': 'completed'}).json['note']
    values = {'title': '변경', 'body': '변경 내용', 'status': status}
    response = client.post('/api/notes', json=values)
    assert response.status_code == 400 and 'status' in response.json['fields']
    response = client.put(f"/api/notes/{note['id']}", json=values)
    assert response.status_code == 400
    preserved = client.get(f"/api/notes/{note['id']}").json['note']
    assert (preserved['title'], preserved['body'], preserved['status']) == ('보존', '내용', 'completed')
    assert len(client.get('/api/notes').json['notes']) == 1


def test_status_migration_preserves_existing_notes(database):
    from pathlib import Path
    script = Path(__file__).resolve().parents[1] / 'monitor/backend/sql/003_note_status.sql'
    with psycopg.connect(database) as conn:
        conn.execute('ALTER TABLE notes DROP COLUMN status')
        note_id = conn.execute('INSERT INTO notes (title, body) VALUES (%s, %s) RETURNING id', ('기존 메모', '기존 내용')).fetchone()[0]
        conn.execute(script.read_text(encoding='utf-8'))
        assert conn.execute('SELECT title, body, status FROM notes WHERE id = %s', (note_id,)).fetchone() == ('기존 메모', '기존 내용', 'pending')
        conn.execute('UPDATE notes SET status = %s WHERE id = %s', ('completed', note_id))
        conn.execute(script.read_text(encoding='utf-8'))
        assert conn.execute('SELECT status FROM notes WHERE id = %s', (note_id,)).fetchone()[0] == 'completed'
