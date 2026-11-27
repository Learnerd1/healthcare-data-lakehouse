-- Create the three Medallion schemas

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Track every ingestion batch

CREATE TABLE IF NOT EXISTS bronze.ingestion_batches (
    batch_id UUID PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_file TEXT,
    ingestion_status VARCHAR(30) NOT NULL DEFAULT 'STARTED',
    records_received INTEGER DEFAULT 0,
    records_loaded INTEGER DEFAULT 0,
    records_rejected INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    error_message TEXT
);

-- Preserve original FHIR resources

CREATE TABLE IF NOT EXISTS bronze.fhir_resources (
    bronze_id BIGSERIAL PRIMARY KEY,
    batch_id UUID REFERENCES bronze.ingestion_batches(batch_id),
    source_system VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    source_file TEXT,
    resource_json JSONB NOT NULL,
    content_hash VARCHAR(64),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bronze_fhir_resource_type
    ON bronze.fhir_resources(resource_type);

CREATE INDEX IF NOT EXISTS idx_bronze_fhir_resource_id
    ON bronze.fhir_resources(resource_id);

CREATE INDEX IF NOT EXISTS idx_bronze_fhir_batch
    ON bronze.fhir_resources(batch_id);

-- Preserve imported reference datasets

CREATE TABLE IF NOT EXISTS bronze.reference_records (
    reference_id BIGSERIAL PRIMARY KEY,
    batch_id UUID REFERENCES bronze.ingestion_batches(batch_id),
    dataset_name VARCHAR(100) NOT NULL,
    source_record_id VARCHAR(255),
    record_json JSONB NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
