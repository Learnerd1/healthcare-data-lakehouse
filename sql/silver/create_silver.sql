CREATE TABLE IF NOT EXISTS silver.patients (
    patient_id     VARCHAR(255) PRIMARY KEY,
    bronze_id      BIGINT NOT NULL,
    given_name     TEXT,
    family_name    TEXT,
    gender         VARCHAR(20),
    birth_date     DATE,
    death_date     TIMESTAMPTZ,
    marital_status VARCHAR(20),
    city           TEXT,
    state          TEXT
);

CREATE TABLE IF NOT EXISTS silver.encounters (
    encounter_id     VARCHAR(255) PRIMARY KEY,
    bronze_id        BIGINT NOT NULL,
    patient_id       VARCHAR(255),
    encounter_class  VARCHAR(50),
    encounter_type   TEXT,
    reason           TEXT,
    start_time       TIMESTAMPTZ,
    end_time         TIMESTAMPTZ,
    provider_org_id  VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS silver.observations (
    observation_id   VARCHAR(255) PRIMARY KEY,
    bronze_id        BIGINT NOT NULL,
    patient_id       VARCHAR(255),
    encounter_id     VARCHAR(255),
    category         VARCHAR(50),
    code             VARCHAR(50),
    description      TEXT,
    value_number     NUMERIC,
    value_unit       VARCHAR(50),
    value_text       TEXT,
    effective_time   TIMESTAMPTZ
);

TRUNCATE silver.patients, silver.encounters, silver.observations;

INSERT INTO silver.patients
SELECT
    resource_id,
    bronze_id,
    resource_json #>> '{name,0,given,0}',
    resource_json #>> '{name,0,family}',
    resource_json ->> 'gender',
    (resource_json ->> 'birthDate')::DATE,
    (resource_json ->> 'deceasedDateTime')::TIMESTAMPTZ,
    resource_json #>> '{maritalStatus,coding,0,code}',
    resource_json #>> '{address,0,city}',
    resource_json #>> '{address,0,state}'
FROM bronze.fhir_resources
WHERE resource_type = 'Patient'
ON CONFLICT (patient_id) DO NOTHING;

INSERT INTO silver.encounters
SELECT
    resource_id,
    bronze_id,
    regexp_replace(resource_json #>> '{subject,reference}', '^(urn:uuid:|Patient/)', ''),
    resource_json #>> '{class,code}',
    resource_json #>> '{type,0,coding,0,display}',
    resource_json #>> '{reasonCode,0,coding,0,display}',
    (resource_json #>> '{period,start}')::TIMESTAMPTZ,
    (resource_json #>> '{period,end}')::TIMESTAMPTZ,
    regexp_replace(resource_json #>> '{serviceProvider,reference}', '^(urn:uuid:|Organization/)', '')
FROM bronze.fhir_resources
WHERE resource_type = 'Encounter'
ON CONFLICT (encounter_id) DO NOTHING;

INSERT INTO silver.observations
SELECT
    resource_id,
    bronze_id,
    regexp_replace(resource_json #>> '{subject,reference}', '^(urn:uuid:|Patient/)', ''),
    regexp_replace(resource_json #>> '{encounter,reference}', '^(urn:uuid:|Encounter/)', ''),
    resource_json #>> '{category,0,coding,0,code}',
    resource_json #>> '{code,coding,0,code}',
    resource_json #>> '{code,coding,0,display}',
    (resource_json #>> '{valueQuantity,value}')::NUMERIC,
    resource_json #>> '{valueQuantity,unit}',
    COALESCE(resource_json ->> 'valueString',
             resource_json #>> '{valueCodeableConcept,coding,0,display}'),
    (resource_json ->> 'effectiveDateTime')::TIMESTAMPTZ
FROM bronze.fhir_resources
WHERE resource_type = 'Observation'
ON CONFLICT (observation_id) DO NOTHING;
