"""Recreate both Compose projects WITHOUT deleting volumes and verify saved data."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import requests

ROOT = Path(__file__).resolve().parents[1]


def main():
    executable = shutil.which('docker')
    if not executable:
        executable = str(Path(os.environ['LOCALAPPDATA']) / 'Programs/DockerDesktop/resources/bin/docker.exe')
    state_file = ROOT / 'monitor/next-frontend/.cache/runtime-state.json'
    if not state_file.is_file():
        raise SystemExit('Run the Docker browser test first to create the persistence checkpoint.')
    state = json.loads(state_file.read_text())

    def compose(role, *args):
        subprocess.run([executable, 'compose', '-f', f'compose-{role}.yaml', *args], cwd=ROOT, check=True)

    volumes = ['m5d1-general_general-data', 'm5d1-monitor_monitor-data']
    subprocess.run([executable, 'volume', 'inspect', *volumes, '--format', '{{.Name}}'], check=True)
    compose('general', 'down')
    compose('monitor', 'down')
    subprocess.run([executable, 'volume', 'inspect', *volumes, '--format', '{{.Name}}'], check=True)
    compose('monitor', 'up', '-d')
    response = requests.get('http://localhost:8082/api/auth/me', timeout=10)
    assert response.status_code == 200
    compose('general', 'up', '-d')
    monitor = requests.Session()
    assert monitor.post('http://localhost:8082/api/auth/login', json={'username': 'operator', 'password': 'Learn123!'}, timeout=10).status_code == 200
    detail = monitor.get(f"http://localhost:8082/api/notes/{state['noteId']}", timeout=10)
    assert detail.status_code == 200
    assert detail.json()['note']['title'] == 'Docker 점검'
    assert detail.json()['note']['body'] == '로그인 실패와 성공을 확인했다'
    events = monitor.get('http://localhost:8082/api/events', timeout=10).json()['events']
    assert set(state['eventIds']) <= {event['id'] for event in events}
    general = requests.Session()
    assert general.post('http://localhost:8081/auth/login', json={'username': 'student', 'password': 'Learn123!'}, timeout=10).status_code == 200
    assert general.get('http://localhost:8081/', timeout=10).status_code == 200
    print(f"두 프로젝트 down/up 후 로그인 기록 {state['eventIds']}와 메모 #{state['noteId']} 보존 확인; 볼륨 삭제 없음.")


if __name__ == '__main__':
    main()
