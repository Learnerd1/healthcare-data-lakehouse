DROP TABLE IF EXISTS gold.patient_summary;
DROP TABLE IF EXISTS gold.patient_demographics;
DROP TABLE IF EXISTS gold.encounters_monthly;

CREATE TABLE gold.patient_summary AS
WITH enc AS (
    SELECT patient_id,
           COUNT(*) AS total_encounters,
           MIN(start_time) AS first_encounter,
           MAX(start_time) AS last_encounter
    FROM silver.encounters
    GROUP BY patient_id
),
bmi AS (
    SELECT DISTINCT ON (patient_id) patient_id, value_number AS latest_bmi
    FROM silver.observations
    WHERE code = '39156-5' AND value_number IS NOT NULL
    ORDER BY patient_id, effective_time DESC
)
SELECT
    p.patient_id,
    p.gender,
    p.city,
    p.state,
    DATE_PART('year', AGE(COALESCE(p.death_date::DATE, CURRENT_DATE), p.birth_date))::INT AS age,
    (p.death_date IS NOT NULL) AS is_deceased,
    COALESCE(e.total_encounters, 0) AS total_encounters,
    e.first_encounter,
    e.last_encounter,
    b.latest_bmi
FROM silver.patients p
LEFT JOIN enc e ON e.patient_id = p.patient_id
LEFT JOIN bmi b ON b.patient_id = p.patient_id;

CREATE TABLE gold.patient_demographics AS
SELECT
    gender,
    CASE
        WHEN age < 18 THEN '0-17'
        WHEN age < 40 THEN '18-39'
        WHEN age < 65 THEN '40-64'
        ELSE '65+'
    END AS age_group,
    COUNT(*) AS patient_count
FROM gold.patient_summary
GROUP BY 1, 2;

CREATE TABLE gold.encounters_monthly AS
SELECT
    DATE_TRUNC('month', start_time)::DATE AS month,
    encounter_class,
    COUNT(*) AS encounter_count,
    COUNT(DISTINCT patient_id) AS unique_patients
FROM silver.encounters
WHERE start_time IS NOT NULL
GROUP BY 1, 2;
