

\# FHIR-Enabled Healthcare Data Engineering

\# and Interoperability Platform



\## Project Overview



This project develops an end-to-end healthcare data

engineering platform for ingesting, preserving,

transforming, standardising and analysing synthetic

clinical data and public healthcare reference data.



The platform integrates Docker, Apache Airflow,

Python and PostgreSQL within a Medallion architecture.



HL7 FHIR R4 provides the interoperability framework,

while LOINC and SNOMED CT support clinical terminology

standardisation.



The Nigeria Health Facility Registry (NHFR) provides

Nigerian healthcare facility reference information.



\## Objectives



1\. Develop repeatable healthcare data ingestion pipelines.

2\. Preserve source data and ingestion metadata.

3\. Transform FHIR resources into relational datasets.

4\. Integrate relevant clinical terminology.

5\. Implement automated data-quality validation.

6\. Develop Bronze, Silver and Gold data layers.

7\. Produce FHIR-compatible output resources.

8\. Create analytics-ready healthcare datasets.



\## Technology Stack



\- Docker

\- Docker Compose

\- Apache Airflow

\- Python

\- PostgreSQL

\- Pandas

\- SQLAlchemy

\- Psycopg

\- HL7 FHIR R4

\- LOINC

\- SNOMED CT

\- Power BI

\- Git



\## Data Sources



\- Synthea: synthetic clinical data

\- LOINC: laboratory and observation terminology

\- SNOMED CT: clinical terminology

\- NHFR: Nigerian healthcare facility reference data



\## Architecture



Bronze -> Silver -> Gold



\## Data Integrity Statement



Synthea records are synthetic and must not be

interpreted as real Nigerian patient records.



NHFR data is maintained as an independent facility

reference domain. No real patient-to-facility

relationship is assumed.



\## Project Status



Implementation in progress.



