from datetime import timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import MemberSecurity
from app.models.member import Member
from app.repositories.member import MemberRepository
from app.schemas.member import RegisterRequest, RegisterResponse


class DuplicateEmailError(Exception):
    pass


def register_member(
    payload: RegisterRequest, session: Session, security: MemberSecurity
) -> RegisterResponse:
    repository = MemberRepository(session)
    digest = security.email_digest(str(payload.email))
    if repository.email_exists(digest):
        raise DuplicateEmailError
    member = Member(
        name_encrypted=security.encrypt(payload.name),
        email_encrypted=security.encrypt(str(payload.email)),
        email_digest=digest,
        password_hash=security.hash_password(payload.password.get_secret_value()),
    )
    try:
        repository.save(member)
    except IntegrityError:
        # The unique constraint also protects against concurrent registrations.
        session.rollback()
        if repository.email_exists(digest):
            raise DuplicateEmailError from None
        raise
    created_at = member.created_at
    if created_at.tzinfo is None:  # SQLite returns naive timestamps.
        created_at = created_at.replace(tzinfo=timezone.utc)
    return RegisterResponse(
        id=member.id, name=security.decrypt(member.name_encrypted), created_at=created_at
    )
