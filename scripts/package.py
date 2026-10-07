"""Build the submission ZIP from committed source, never from local secrets."""
from pathlib import Path
import ast
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    files = [name for name in files if name]
    if not files:
        raise SystemExit("Commit project source before packaging.")
    for name in files:
        parts = Path(name).parts
        if any(part in {".cache", ".venv", "node_modules", ".git", "instance", "dist", "__pycache__"} for part in parts):
            raise RuntimeError(f"Private/generated directory is tracked: {name}")
        if any(part.startswith(".env") and part != ".env.example" for part in parts):
            raise RuntimeError(f"Private environment file is tracked: {name}")
        if name.endswith(".py"):
            ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
    archive = ROOT / "monitor-dashboard.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in files:
            bundle.write(ROOT / name, f"monitor-dashboard/{name}")
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("ZIP integrity verification failed.")
    print(f"Created {archive.name}: {len(files)} source files, {archive.stat().st_size} bytes.")


if __name__ == "__main__":
    main()
