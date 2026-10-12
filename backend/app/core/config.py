from pathlib import Path

from cryptography.fernet import Fernet
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./members.db"
    encryption_key: SecretStr
    email_hash_key: SecretStr
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @field_validator("encryption_key")
    @classmethod
    def valid_encryption_key(cls, value: SecretStr) -> SecretStr:
        try:
            Fernet(value.get_secret_value().encode())
        except (ValueError, TypeError) as error:
            raise ValueError("ENCRYPTION_KEY must be a valid Fernet key") from error
        return value

    @field_validator("email_hash_key")
    @classmethod
    def valid_lookup_key(cls, value: SecretStr) -> SecretStr:
        try:
            key = bytes.fromhex(value.get_secret_value())
        except ValueError as error:
            raise ValueError("EMAIL_HASH_KEY must be hex encoded") from error
        if len(key) < 32:
            raise ValueError("EMAIL_HASH_KEY must contain at least 32 random bytes")
        return value
