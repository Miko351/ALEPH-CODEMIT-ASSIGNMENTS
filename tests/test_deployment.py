"""Validate isolation, service contracts and the Docker build inputs without a daemon."""
import ast
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_isolation_and_persistence():
    projects = {
        'general': {'general-db', 'general-api', 'general-gateway'},
        'monitor': {'monitor-db', 'monitor-api', 'monitor-web', 'monitor-gateway'},
    }
    for role, expected in projects.items():
        data = yaml.safe_load((ROOT / f'compose-{role}.yaml').read_text())
        assert data['name'] == f'm5d1-{role}'
        assert set(data['services']) == expected
        assert data['networks']['events'] == {'external': True, 'name': 'm5d1-events'}
        assert data['networks'][f'{role}-web'] == {'driver': 'bridge'}
        assert data['networks'][f'{role}-data']['internal'] is True
        services = data['services']
        db, api, gateway = [services[f'{role}-{name}'] for name in ('db', 'api', 'gateway')]
        assert db['networks'] == [f'{role}-data']
        assert api['networks'] == [f'{role}-web', f'{role}-data', 'events']
        assert gateway['networks'] == [f'{role}-web']
        for name, service in services.items():
            assert ('ports' in service) == name.endswith('-gateway')
            for dependency in service.get('depends_on', {}):
                assert dependency in services
            if 'build' in service:
                context = ROOT / service['build']
                assert (context / 'Dockerfile').is_file()
                ignore = (context / '.dockerignore').read_text()
                assert all(pattern in ignore for pattern in ('.venv', 'node_modules', '.next', '.env'))
        assert gateway['ports'] == [f"{'8081' if role == 'general' else '8082'}:80"]
        assert api['environment']['DB_HOST'] == f'{role}-db'
        assert api['environment']['DB_PORT'] == '5432'
        assert api['environment']['DB_NAME'] == db['environment']['POSTGRES_DB']
        assert api['environment']['DB_USER'] == db['environment']['POSTGRES_USER']
        assert api['environment']['DB_PASSWORD'] == db['environment']['POSTGRES_PASSWORD']
        assert api['depends_on'][f'{role}-db']['condition'] == 'service_healthy'
        assert db['healthcheck']['test'][0] == 'CMD-SHELL'
        assert f'{role}-data:/var/lib/postgresql/data' in db['volumes']
        assert f'{role}-data' in data['volumes']
        sql_mount = next(item for item in db['volumes'] if 'docker-init.sql' in item)
        assert (ROOT / sql_mount.split(':')[0]).is_file()
    general = yaml.safe_load((ROOT / 'compose-general.yaml').read_text())
    assert general['services']['general-api']['environment']['MONITOR_URL'] == 'http://monitor-api:5000/api/events'
    monitor = yaml.safe_load((ROOT / 'compose-monitor.yaml').read_text())
    assert monitor['services']['monitor-gateway']['depends_on']['monitor-web']['condition'] == 'service_healthy'
    assert monitor['services']['monitor-web']['healthcheck']['test'][:2] == ['CMD', 'node']


def test_build_commands_and_gateway_routes():
    package = json.loads((ROOT / 'monitor/next-frontend/package.json').read_text())
    assert package['scripts']['start'] == 'next start --hostname 0.0.0.0'
    dockerfile = (ROOT / 'monitor/next-frontend/Dockerfile').read_text()
    assert 'npm ci' in dockerfile and 'npm run build' in dockerfile and '"start"' in dockerfile
    assert 'http://general-api:5000;' in (ROOT / 'gateways/general.conf').read_text()
    monitor = (ROOT / 'gateways/monitor.conf').read_text()
    assert 'http://monitor-web:3000;' in monitor and 'http://monitor-api:5000;' not in monitor
    assert (ROOT / 'monitor/next-frontend/app/api/[...path]/route.js').is_file()
    for folder in ('general', 'monitor/backend'):
        assert 'waitress-serve' in (ROOT / folder / 'Dockerfile').read_text()
    for source in ROOT.rglob('*.py'):
        if not any(part in {'.venv', '.cache', 'node_modules'} for part in source.parts):
            ast.parse(source.read_text(encoding='utf-8'))
