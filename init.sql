CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    language VARCHAR(10),
    duration_s INT,
    status VARCHAR(20)
);

CREATE TABLE video_segments (
    id SERIAL PRIMARY KEY,
    video_id INT REFERENCES videos(id),
    start_s INT,
    end_s INT,
    title VARCHAR(255),
    tags TEXT[],
    transcript_fragment TEXT
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    parameters JSONB
);

CREATE TABLE reference_profiles (
    id SERIAL PRIMARY KEY,
    bpm INT,
    musical_key VARCHAR(10),
    sections JSONB,
    density FLOAT
);

CREATE TABLE midi_patterns (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50),
    bars INT,
    file_path VARCHAR(255),
    tags TEXT[],
    meta JSONB
);

CREATE TABLE arrangement_plans (
    id SERIAL PRIMARY KEY,
    plan_data JSONB
);

CREATE TABLE action_sequences (
    id SERIAL PRIMARY KEY,
    dsl_commands JSONB,
    validated BOOLEAN DEFAULT FALSE
);

CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    preset_name VARCHAR(255),
    fx_chain JSONB,
    macros JSONB
);

CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    owner_type VARCHAR(50),
    owner_id INT,
    model VARCHAR(50),
    embedding vector(384)
);

CREATE INDEX ON video_segments (video_id);
CREATE INDEX ON recipes USING GIN (parameters);
CREATE INDEX ON arrangement_plans USING GIN (plan_data);
CREATE INDEX ON embeddings USING HNSW (embedding vector_l2_ops);
