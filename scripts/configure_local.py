"""Generate private local Compose configuration; never print keys or tokens."""
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / '.env'
    if target.exists():
        raise SystemExit('Root .env exists; keep it and add required fields manually.')
    target.write_text(
        f'GENERAL_DB_PASSWORD={secrets.token_urlsafe(24)}\n'
        f'MONITOR_DB_PASSWORD={secrets.token_urlsafe(24)}\n'
        f'GENERAL_SECRET_KEY={secrets.token_urlsafe(48)}\n'
        f'MONITOR_SECRET_KEY={secrets.token_urlsafe(48)}\n'
        f'EVENT_TOKEN={secrets.token_urlsafe(48)}\n', encoding='utf-8',
    )
    print('Created ignored root .env with separate DB passwords/session keys and a shared event token.')


if __name__ == '__main__':
    main()
