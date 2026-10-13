"""Build a source ZIP from Git-tracked app files and actual Git practice documents."""
import ast
from pathlib import Path
import subprocess
import zipfile

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parent
PRIVATE = {'.git', '.cache', 'node_modules', '.next', '.venv', 'venv', '__pycache__', '.pytest_cache', 'instance', 'test-results', 'playwright-report'}


def allowed(name):
    path = Path(name)
    return not any(part in PRIVATE or (part.startswith('.env') and part != '.env.example') for part in path.parts) and path.suffix not in {'.pyc', '.log', '.db', '.zip', '.bundle', '.sqlite', '.sqlite3'}


def main():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=APP).decode().split('\0')
    files = [(APP / name, f'nextjs-notes/next-practice/{name}') for name in names if name]
    for source, target in files:
        if not allowed(target):
            raise RuntimeError(f'Private/generated file is tracked: {target}')
        if source.suffix == '.py':
            ast.parse(source.read_text(encoding='utf-8'))
    files.append((APP / 'GIT_WORK.md', 'nextjs-notes/GIT_WORK.md'))
    files.append((APP / 'README.md', 'nextjs-notes/README.md'))
    for role in ('minsu', 'jiyun'):
        folder = ROOT / f'git-practice-{role}'
        if subprocess.check_output(['git', 'branch', '--show-current'], cwd=folder).decode().strip() != 'main':
            raise RuntimeError('Git practice folder must be on merged main before packaging.')
        for name in ('minsu.md', 'jiyun.md', 'checklist.md'):
            files.append((folder / name, f'nextjs-notes/git-practice-{role}/{name}'))
    destination = ROOT / 'nextjs-notes.zip'
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for source, target in files:
            archive.write(source, target)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('ZIP integrity failed.')
        assert all(allowed(name) for name in archive.namelist())
        assert 'nextjs-notes/next-practice/app/notes/page.js' in archive.namelist()
        for name in ('app/db-notes/page.js', 'components/DatabaseNotes.js', 'lib/api/notes.js', 'tests/db-notes.spec.js'):
            assert f'nextjs-notes/next-practice/{name}' in archive.namelist()
        assert 'nextjs-notes/next-practice/mini-watch/monitor/next-frontend/package-lock.json' in archive.namelist()
    print(f'Created {destination.name}: {len(files)} files, {destination.stat().st_size} bytes; secrets/builds/installed packages excluded.')


if __name__ == '__main__':
    main()
