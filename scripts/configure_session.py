"""Persist a random session signing key in the private backend environment."""
from pathlib import Path
import secrets
from dotenv import dotenv_values, set_key

ROOT = Path(__file__).resolve().parents[1]


def configure():
    path = ROOT / "monitor/backend/.env"
    if not path.exists():
        raise SystemExit("먼저 monitor/backend/.env를 준비하세요. (.env.example 복사 또는 dev_postgres.py setup)")
    existing = dotenv_values(path).get("SECRET_KEY", "")
    if existing and len(existing) >= 32 and not existing.startswith("CHANGE_ME"):
        print("Existing session key preserved.")
        return
    set_key(str(path), "SECRET_KEY", secrets.token_hex(32))
    print("Created a private persistent session key in monitor/backend/.env.")


if __name__ == "__main__":
    configure()
