from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.member import Member


class MemberRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def email_exists(self, digest: str) -> bool:
        return self.session.scalar(select(Member.id).where(Member.email_digest == digest)) is not None

    def save(self, member: Member) -> Member:
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member
