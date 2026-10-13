import os

# Only test defaults; real app processes require their own environment settings.
os.environ.setdefault('SECRET_KEY', 'unit-test-session-key-not-for-deployment')
os.environ.setdefault('EVENT_TOKEN', 'unit-test-event-token-not-for-deployment')
os.environ.setdefault('SENTRY_DSN', '')
