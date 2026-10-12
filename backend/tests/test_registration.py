from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.main import create_app
from app.models.member import Member

PASSWORD = "correct-horse-123"
PAYLOAD = {"name": "홍길동", "email": "member@example.com", "password": PASSWORD}


@pytest.fixture
def application(tmp_path):
    settings = Settings(
        _env_file=None,
        database_url=f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        encryption_key=Fernet.generate_key().decode(),
        email_hash_key="ab" * 32,
    )
    return create_app(settings)


@pytest.fixture
def client(application):
    with TestClient(application) as test_client:
        yield test_client


def test_registration_is_encrypted_and_persisted(client, application):
    response = client.post("/api/auth/register", json=PAYLOAD)
    assert response.status_code == 201
    assert response.json()["name"] == PAYLOAD["name"]
    assert datetime.fromisoformat(response.json()["created_at"]).utcoffset() == timedelta(0)
    assert "password" not in response.text
    with application.state.session_factory() as session:
        member = session.scalar(select(Member))
        assert member.id == response.json()["id"]
        assert PAYLOAD["name"] not in member.name_encrypted
        assert PAYLOAD["email"] not in member.email_encrypted
        assert application.state.security.decrypt(member.name_encrypted) == PAYLOAD["name"]
        assert application.state.security.decrypt(member.email_encrypted) == PAYLOAD["email"]
        assert member.password_hash.startswith("$argon2id$")
        assert application.state.security.password_hasher.verify(PASSWORD, member.password_hash)
        assert PASSWORD not in member.password_hash
        database_path = session.get_bind().url.database
    raw = Path(database_path).read_bytes()
    for plaintext in (PAYLOAD["name"], PAYLOAD["email"], PASSWORD):
        assert plaintext.encode() not in raw
    # A new engine and app can read the record with the same environment keys.
    from app.db.session import build_engine
    engine = build_engine(f"sqlite:///{database_path}")
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(Member)) == 1
    engine.dispose()


def test_duplicate_email_is_normalized(client, application):
    first = client.post("/api/auth/register", json=PAYLOAD)
    duplicate = client.post(
        "/api/auth/register", json={**PAYLOAD, "email": "  MEMBER@EXAMPLE.COM  "}
    )
    assert first.status_code == 201
    assert duplicate.status_code == 409
    with application.state.session_factory() as session:
        assert session.scalar(select(func.count()).select_from(Member)) == 1


@pytest.mark.parametrize("changes", [
    {"name": " "}, {"name": "x" * 81}, {"email": "invalid"},
    {"password": "short"}, {"password": " " * 10},
    {"password": "x" * 129}, {"unexpected": "field"},
])
def test_invalid_payload_is_rejected_without_leaking_inputs(client, application, changes):
    response = client.post("/api/auth/register", json={**PAYLOAD, **changes})
    assert response.status_code == 422
    assert "input" not in response.text
    assert PASSWORD not in response.text
    with application.state.session_factory() as session:
        assert session.scalar(select(func.count()).select_from(Member)) == 0


def test_simultaneous_duplicate_registration(client, application):
    with ThreadPoolExecutor(max_workers=2) as executor:
        responses = list(executor.map(
            lambda _: client.post("/api/auth/register", json=PAYLOAD), range(2)
        ))
    assert sorted(response.status_code for response in responses) == [201, 409]


def test_health_and_cors(client):
    assert client.get("/api/health").json() == {"status": "ok"}
    response = client.options("/api/auth/register", headers={
        "Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST"
    })
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_invalid_key_fails_fast():
    with pytest.raises(ValueError):
        Settings(_env_file=None, encryption_key="invalid", email_hash_key="ab" * 32)
