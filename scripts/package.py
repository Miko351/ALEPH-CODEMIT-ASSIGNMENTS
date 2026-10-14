"""Archive only tracked source files; excludes private and generated data."""
from pathlib import Path
import ast
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = {'.git', '.venv', 'venv', '.cache', 'node_modules', '.next', '__pycache__', '.pytest_cache', 'instance', 'test-results', 'playwright-report'}


def main():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    names = [name for name in names if name]
    required = {'compose-general.yaml', 'compose-monitor.yaml', 'README.md', '.env.example',
                'general/Dockerfile', 'monitor/backend/Dockerfile', 'monitor/next-frontend/Dockerfile',
                'monitor/next-frontend/package-lock.json', 'general/sql/docker-init.sql',
                'monitor/backend/sql/docker-init.sql', 'gateways/general.conf', 'gateways/monitor.conf',
                'deployment-plan.md', 'general/sql/deploy.sql', 'monitor/backend/sql/deploy.sql',
                'general/.env.example', 'monitor/backend/.env.example', 'monitor/next-frontend/.env.example',
                'monitor/next-frontend/app/api/[...path]/route.js', 'general/observability.py', 'monitor/backend/observability.py'}
    required.update({'monitor/backend/event_rules.py', 'monitor/backend/routes/analysis.py',
                     'monitor/backend/learning/capture_case.py', 'monitor/backend/learning/normalize.py',
                     'monitor/backend/learning/http_rules.py', 'monitor/backend/learning/report.py',
                     'monitor/next-frontend/components/AnalysisClient.js'})
    assert required <= set(names)
    for name in names:
        path = Path(name)
        assert not any(part in PRIVATE or (part.startswith('.env') and part != '.env.example') for part in path.parts)
        assert path.suffix not in {'.zip', '.log', '.db', '.pyc', '.sqlite'}
        assert path.suffix not in {'.pcap', '.pcapng'}
        assert not (path.suffix == '.json' and 'learning/data' in path.as_posix())
        if path.suffix == '.py':
            ast.parse((ROOT / path).read_text(encoding='utf-8'))
    target = ROOT / 'mini-watch-analysis.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(ROOT / name, f'mini-watch-analysis/{name}')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name in names:
            assert archive.read(f'mini-watch-analysis/{name}') == (ROOT / name).read_bytes()
    print(f'{target.name}: {len(names)} files, {target.stat().st_size} bytes; ZIP CRC and source equality verified.')


if __name__ == '__main__':
    main()
