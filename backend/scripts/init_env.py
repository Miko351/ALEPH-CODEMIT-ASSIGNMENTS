"""Create local configuration once without printing or replacing secrets."""
from pathlib import Path
import secrets

from cryptography.fernet import Fernet


def main() -> None:
    destination = Path(__file__).resolve().parents[1] / ".env"
    try:
        with destination.open("x", encoding="utf-8") as file:
            file.write(
                "DATABASE_URL=sqlite:///./members.db\n"
                f"ENCRYPTION_KEY={Fernet.generate_key().decode()}\n"
                f"EMAIL_HASH_KEY={secrets.token_hex(32)}\n"
                'CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]\n'
            )
    except FileExistsError:
        print("Existing .env preserved.")
    else:
        print("Created backend/.env. Keep these keys private and backed up.")


if __name__ == "__main__":
    main()
