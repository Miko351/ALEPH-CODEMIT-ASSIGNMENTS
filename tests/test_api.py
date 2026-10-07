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


def test_crud_and_persistence_across_process(client, database):
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
    fresh_client = create_app({'TESTING': True, 'DATABASE_URL': database}).test_client()
    assert fresh_client.get(path).json['note']['body'] == '바뀐 내용'
    code = 'from monitor.backend.app import create_app; c=create_app().test_client(); r=c.get("' + path + '"); assert r.status_code==200; assert r.json["note"]["body"]=="바뀐 내용"; print("persisted")'
    result = subprocess.run([sys.executable, '-c', code], env={**os.environ, 'DATABASE_URL': database}, capture_output=True, text=True)
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
    events = requests.get(monitor_url + '/api/events', timeout=5).json()['events']
    for method, event_path, status in [('GET', '/', 200), ('POST', '/board/new', 400), ('POST', '/board/new', 303), ('GET', path, 404)]:
        assert any(row['method'] == method and row['path'] == event_path and row['status_code'] == status for row in events)
    assert 'password' not in str(events)


def test_events_persist_and_malformed_record_is_rejected(client, database):
    record = {'timestamp': datetime.now(timezone.utc).isoformat(), 'method': 'GET', 'path': '/board/404', 'status_code': 404, 'duration_ms': 3.4}
    assert client.post('/api/events', json=record).status_code == 201
    fresh = create_app({'TESTING': True, 'DATABASE_URL': database}).test_client()
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
