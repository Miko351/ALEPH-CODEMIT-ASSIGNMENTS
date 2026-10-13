-- New-project setup only. Existing Day3 tables/sequences must be kept as-is.
-- No DROP, DELETE or sequence restart is performed.
CREATE SEQUENCE IF NOT EXISTS posts_id_seq;

CREATE TABLE IF NOT EXISTS posts (
    id integer PRIMARY KEY DEFAULT nextval('posts_id_seq'),
    title text NOT NULL,
    body text NOT NULL
);

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;
