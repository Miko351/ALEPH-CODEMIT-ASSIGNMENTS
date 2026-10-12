"""Create a portable source archive without local data or secret configuration."""
import ast
import os
from pathlib import Path
import zipfile

EXCLUDED_DIRECTORIES = {
    ".git", ".venv", "venv", "node_modules", ".next", "__pycache__",
    ".pytest_cache", ".cache", ".npm-cache", ".pip-cache",
    "test-results", "playwright-report", "coverage",
}
EXCLUDED_SUFFIXES = (
    ".pyc", ".pyo", ".tsbuildinfo", ".db", ".db-journal", ".db-wal",
    ".db-shm", ".sqlite", ".sqlite3", ".zip", ".tmp", ".log",
)


def should_include(relative_path: Path) -> bool:
    if any(part in EXCLUDED_DIRECTORIES for part in relative_path.parts):
        return False
    name = relative_path.name
    if name.startswith(".env") and name != ".env.example":
        return False
    return not name.endswith(EXCLUDED_SUFFIXES)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    destination = project_root / "sign-up.zip"
    temporary_archive = destination.with_suffix(".zip.tmp")
    file_count = 0
    with zipfile.ZipFile(
        temporary_archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for directory, subdirectories, filenames in os.walk(project_root):
            subdirectories[:] = sorted(
                name for name in subdirectories
                if name not in EXCLUDED_DIRECTORIES
                and not (Path(directory) / name).is_symlink()
            )
            for filename in sorted(filenames):
                source = Path(directory) / filename
                relative = source.relative_to(project_root)
                if source.is_symlink() or not should_include(relative):
                    continue
                archive.write(source, f"sign-up/{relative.as_posix()}")
                file_count += 1

    with zipfile.ZipFile(temporary_archive) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Archive integrity check failed")
        for entry in archive.infolist():
            relative = Path(entry.filename).relative_to("sign-up")
            if not should_include(relative):
                raise RuntimeError(f"Unexpected private or generated file: {relative}")
            if relative.suffix == ".py":
                ast.parse(archive.read(entry).decode("utf-8"), filename=entry.filename)
        required = {
            "sign-up/README.md", "sign-up/.gitignore",
            "sign-up/backend/app/main.py", "sign-up/backend/.env.example",
            "sign-up/backend/requirements-dev.lock.txt",
            "sign-up/frontend/src/app/page.tsx", "sign-up/frontend/package-lock.json",
            "sign-up/frontend/.env.example",
        }
        if not required.issubset(archive.namelist()):
            raise RuntimeError("Archive is missing a required source file")
    temporary_archive.replace(destination)
    print(f"Created {destination} ({file_count} files, {destination.stat().st_size:,} bytes)")
    print("Integrity, required files, excluded secrets and Python syntax verified.")


if __name__ == "__main__":
    main()
