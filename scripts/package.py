"""Create a submission ZIP inside the project, excluding secrets and runtime."""
import ast
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", ".cache", "__pycache__", ".pytest_cache", "instance"}


def main() -> None:
    destination = ROOT / "posts-crud.zip"
    staging = ROOT / "posts-crud.zip.tmp"
    count = 0
    with zipfile.ZipFile(staging, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for directory, folders, files in os.walk(ROOT):
            folders[:] = sorted(name for name in folders if name not in EXCLUDED)
            for name in sorted(files):
                path = Path(directory) / name
                if path.is_symlink() or (name.startswith(".env") and name != ".env.example"):
                    continue
                if name.endswith((".zip", ".tmp", ".pyc", ".log", ".jsonl")):
                    continue
                archive.write(path, f"posts-crud/{path.relative_to(ROOT).as_posix()}")
                count += 1
    with zipfile.ZipFile(staging) as archive:
        assert archive.testzip() is None
        for entry in archive.infolist():
            if entry.filename.endswith(".py"):
                ast.parse(archive.read(entry).decode("utf-8"))
        required = {f"posts-crud/mini-watch/general/templates/{name}.html" for name in [
            "index", "detail", "new", "edit", "delete", "error"
        ]}
        assert required.issubset(archive.namelist())
    staging.replace(destination)
    print(f"Created {destination} ({count} files; {destination.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
