"""Run the E2E API against a temporary database and independent ephemeral keys."""
from pathlib import Path
import secrets
import sys
from tempfile import TemporaryDirectory

from cryptography.fernet import Fernet
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import Settings
from app.main import create_app


if __name__ == "__main__":
    with TemporaryDirectory(prefix="aleph-e2e-") as directory:
        config = Settings(
            _env_file=None,
            database_url=f"sqlite:///{Path(directory).as_posix()}/members.db",
            encryption_key=Fernet.generate_key().decode(),
            email_hash_key=secrets.token_hex(32),
            cors_origins=["http://127.0.0.1:3001"],
        )
        uvicorn.run(create_app(config), host="127.0.0.1", port=8001)
