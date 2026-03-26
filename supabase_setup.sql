-- Run this in your Supabase SQL Editor to set up the students table

-- 1. Create the students table
CREATE TABLE IF NOT EXISTS students (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    math       INTEGER NOT NULL CHECK (math >= 0 AND math <= 100),
    physics    INTEGER NOT NULL CHECK (physics >= 0 AND physics <= 100),
    cs         INTEGER NOT NULL CHECK (cs >= 0 AND cs <= 100),
    english    INTEGER NOT NULL CHECK (english >= 0 AND english <= 100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Enable Row Level Security (optional but recommended for production)
ALTER TABLE students ENABLE ROW LEVEL SECURITY;

-- 3. Allow all operations for anon key (for development — tighten for production)
CREATE POLICY "Allow all for anon" ON students
    FOR ALL TO anon USING (true) WITH CHECK (true);

-- 4. Insert example data
INSERT INTO students (name, math, physics, cs, english) VALUES
    ('Alex',  78, 65, 89, 70),
    ('Bob',   90, 88, 95, 85),
    ('Sara',  55, 60, 70, 62),
    ('Diana', 82, 79, 88, 91),
    ('Ethan', 45, 50, 60, 55),
    ('Fiona', 95, 92, 97, 89),
    ('George',70, 68, 75, 72),
    ('Hana',  38, 42, 55, 48);

-- 5. Verify
SELECT * FROM students ORDER BY id;
