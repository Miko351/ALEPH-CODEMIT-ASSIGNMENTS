-- Non-destructive upgrade. Keep all existing IDs, timestamps, accounts and notes.
ALTER TABLE http_events ALTER COLUMN occurred_at SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE http_events ADD COLUMN IF NOT EXISTS event_type text;
UPDATE http_events SET event_type = CASE
    WHEN method = 'POST' AND path = '/auth/login' AND status_code = 200 THEN 'login_success'
    WHEN method = 'POST' AND path = '/auth/login' AND status_code = 401 THEN 'login_failure'
    WHEN method = 'GET' AND path = '/' AND status_code = 200 THEN 'post_list'
    WHEN status_code >= 400 THEN 'request_error'
    ELSE 'http_request' END WHERE event_type IS NULL;
ALTER TABLE http_events ALTER COLUMN event_type SET NOT NULL;
ALTER TABLE http_events ALTER COLUMN event_type SET DEFAULT 'http_request';
