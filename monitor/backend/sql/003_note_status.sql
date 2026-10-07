-- Upgrade existing notes without deleting or rewriting their title/body.
-- Existing notes receive the initial status; repeated initialization is safe.
ALTER TABLE notes ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'in_progress', 'completed'));
