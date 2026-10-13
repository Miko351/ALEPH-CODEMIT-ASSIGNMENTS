"""Shared input rules for creating and editing posts."""


def validate_post(title: str | None, body: str | None) -> tuple[str, str, dict[str, str]]:
    clean_title = (title or "").strip()
    clean_body = (body or "").strip()
    errors = {}
    if not clean_title:
        errors["title"] = "제목을 입력해 주세요."
    if not clean_body:
        errors["body"] = "내용을 입력해 주세요."
    return clean_title, clean_body, errors
