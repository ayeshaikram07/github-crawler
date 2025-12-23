-- 1. Create database
CREATE DATABASE github_data;

-- 2. Connect to database
\c github_data

-- 3. Create table with primary key & unique constraint
CREATE TABLE repos (
    id SERIAL PRIMARY KEY,
    repo_name TEXT NOT NULL,
    owner TEXT NOT NULL,
    stars INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (repo_name, owner)
);

-- 4. Check table structure
\d repos;

-- 5. Insert example data
INSERT INTO repos (repo_name, owner, stars)
VALUES ('example-repo', 'example-owner', 123)
ON CONFLICT (repo_name, owner)
DO UPDATE SET stars = EXCLUDED.stars, last_updated = CURRENT_TIMESTAMP;

-- 6. Select top 10 rows
SELECT * FROM repos LIMIT 10;
