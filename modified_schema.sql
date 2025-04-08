CREATE EXTENSION IF NOT EXISTS citext;
-- Removed TimescaleDB extension

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email CITEXT NOT NULL,
    name TEXT,
    institution TEXT,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS users_email_idx ON users (email);

CREATE TABLE IF NOT EXISTS utilities (
    id BIGSERIAL PRIMARY KEY,
    utlsrvid TEXT NOT NULL,
    name TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS utilties_utlsrvid_idx ON utilities (utlsrvid);

CREATE TABLE IF NOT EXISTS balancing_authorities (
    id BIGSERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS balancing_authorities_code_idx ON balancing_authorities (code);

CREATE TABLE IF NOT EXISTS arp (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    ba_id BIGINT NOT NULL REFERENCES balancing_authorities(id),
    demand DOUBLE PRECISION,
    net_imports DOUBLE PRECISION,
    thermal DOUBLE PRECISION,
    hydro DOUBLE PRECISION,
    wind DOUBLE PRECISION,
    solar DOUBLE PRECISION,
    other DOUBLE PRECISION,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS arp_ba_id_idx ON arp (ba_id);
CREATE INDEX IF NOT EXISTS arp_timestamp_idx ON arp (timestamp);
CREATE INDEX IF NOT EXISTS arp_timestamp_ba_id_idx ON arp (timestamp, ba_id);

-- Removed TimescaleDB hypertable creation

CREATE TABLE IF NOT EXISTS pathway_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS pathway_versions (
    id BIGSERIAL PRIMARY KEY,
    pathway_id BIGINT NOT NULL REFERENCES pathway_metadata(id),
    version TEXT NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

SELECT setval('pathway_metadata_id_seq', 1000);

CREATE INDEX IF NOT EXISTS pathway_versions_pathway_id_idx ON pathway_versions (pathway_id);
CREATE INDEX IF NOT EXISTS pathway_versions_pathway_id_version_idx ON pathway_versions (pathway_id, version);

CREATE FUNCTION pathway_versions_update_trigger() RETURNS trigger AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE VIEW pathway_latest_versions AS
    SELECT DISTINCT ON (pathway_id) *
    FROM pathway_versions
    ORDER BY pathway_id, created_at DESC;

SELECT setval('pathway_versions_id_seq', 1000);
