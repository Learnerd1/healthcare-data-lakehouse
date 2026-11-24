# Healthcare Data Lakehouse

A healthcare data engineering project built with Python, Apache Airflow, PostgreSQL, and Docker. This project demonstrates the design and implementation of an integrated hospital clinical data lakehouse that ingests, preserves, processes, standardises, validates, and integrates healthcare data from multiple sources to support analytics, reporting, and evidence-based decision-making.

## Overview

Healthcare data is generated across different systems, formats, and healthcare domains. Bringing these datasets together requires reliable data pipelines, consistent terminology, data quality controls, and interoperability standards.

This project explores these challenges through the development of an end-to-end healthcare data engineering platform.

The project adopts a **Medallion Architecture (Bronze, Silver, and Gold)** to organise data ingestion, processing, and transformation into distinct layers:

- **Bronze Layer:** Ingests and preserves raw healthcare data from different sources while retaining their original structures and values for traceability and future processing.
- **Silver Layer:** Applies data cleaning, standardisation, deduplication, validation, and data quality checks to produce structured and consistent healthcare datasets.
- **Gold Layer:** Integrates processed datasets into analytics-ready tables and models to support healthcare reporting, operational analytics, and clinical data analysis.

The initial implementation focuses on three major clinical data domains:

- **Patient Data:** Patient demographic and identification information.
- **Encounter Data:** Patient visits and associated healthcare encounters.
- **Observation Data:** Clinical observations, including laboratory results and other measurable clinical information.

The architecture is designed to accommodate additional healthcare domains, including diagnoses, procedures, medications, radiology, and billing data as the project evolves.

## Data Sources

The project combines synthetic clinical data with publicly available healthcare reference data to demonstrate healthcare data integration in a practical and reproducible environment.

| Data Source | Purpose |
|---|---|
| [Synthea](https://github.com/synthetichealth/synthea) | Generates synthetic patient records and clinical data, including FHIR R4 resources. |
| [Nigeria Health Facility Registry (NHFR)](https://hfr.fmohconnect.gov.ng/) | Provides Nigerian healthcare facility reference data. |
| [LOINC](https://loinc.org/) | Supports the identification and standardisation of laboratory tests and clinical observations. |
| [SNOMED CT](https://www.snomed.org/) | Supports clinical terminology standardisation and consistent representation of clinical concepts. |

Synthea serves as the primary source of synthetic clinical data, allowing the project to demonstrate healthcare data ingestion and interoperability without relying on identifiable patient records.

NHFR provides a Nigerian healthcare context through facility reference information. These datasets will be ingested and processed independently, with appropriate validation before any relationships are established.

The project does not assume that synthetic patients represent Nigeria's actual patient population or that they received care at facilities listed in NHFR.

## Architecture

The project follows a **Medallion Lakehouse Architecture**:

**Data Sources → Data Ingestion → Bronze → Silver → Gold → Analytics and Reporting**

Each layer serves a specific purpose in transforming raw healthcare data into structured, standardised, integrated, and analytics-ready information.

**FHIR R4 (Fast Healthcare Interoperability Resources)** is incorporated as the primary healthcare data interoperability format. Original FHIR resources are preserved in the Bronze layer before selected resources are parsed into relational structures for subsequent processing.

Clinical terminology integration is supported through **SNOMED CT** and **LOINC**, helping maintain consistent representations of clinical concepts and observations.

**Apache Airflow** orchestrates data ingestion, transformation, and validation workflows, while **PostgreSQL** provides the relational storage environment.

**Docker and Docker Compose** provide containerisation and service management to support a reproducible development environment.

## Tech Stack

| Technology | Application |
|---|---|
| Python | Data ingestion, processing, transformation, and validation |
| Apache Airflow | Workflow orchestration and pipeline scheduling |
| PostgreSQL | Healthcare data storage and management |
| Docker | Application and service containerisation |
| Docker Compose | Multi-container service management |
| Pandas | Data manipulation and transformation |
| SQLAlchemy | Database connectivity and interaction |
| Psycopg | PostgreSQL database driver |
| SQL | Data querying and transformation |
| HL7 FHIR R4 | Healthcare data interoperability |
| SNOMED CT | Clinical terminology standardisation |
| LOINC | Laboratory and observation terminology |
| Pytest | Testing and validation |
| Power BI | Analytics and reporting |
| Git and GitHub | Version control and project documentation |

## Project Objectives

The project aims to:

1. Design and implement an end-to-end healthcare data engineering pipeline.
2. Ingest clinical and healthcare reference data from multiple sources and formats.
3. Implement a Medallion Architecture for organised healthcare data processing.
4. Integrate FHIR R4 resources into a relational data environment.
5. Apply clinical terminology standardisation using SNOMED CT and LOINC.
6. Implement data quality checks, validation, deduplication, and data traceability mechanisms.
7. Orchestrate data pipelines using Apache Airflow.
8. Develop integrated, analytics-ready healthcare datasets for reporting and decision support.
9. Demonstrate practical applications of healthcare data interoperability and data engineering.

## Repository Structure

```text
healthcare-data-lakehouse/
│
├── airflow/
│   ├── dags/
│   ├── logs/
│   ├── plugins/
│   └── config/
│
├── data/
│   ├── raw/
│   │   ├── synthea/
│   │   ├── loinc/
│   │   ├── snomed/
│   │   └── nhfr/
│   ├── processed/
│   └── rejected/
│
├── docker/
│   └── warehouse/
│
├── scripts/
│
├── sql/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   └── health_lakehouse/
│       ├── common/
│       ├── database/
│       ├── ingestion/
│       ├── transformation/
│       └── validation/
│
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

## Project Status

**Currently under development.**

The initial project setup includes:

- Git and GitHub repository configuration.
- Project directory structure.
- Docker-based PostgreSQL infrastructure.
- Initial Bronze, Silver, and Gold database schemas.
- Python environment and database connectivity components.

The subsequent implementation stages will cover:

- Integration of PostgreSQL with the existing Apache Airflow environment.
- Synthea data generation and FHIR R4 ingestion.
- Bronze, Silver, and Gold pipeline implementation.
- Clinical terminology integration.
- Data quality validation and testing.
- Healthcare data integration and analytics.

## Expected Outcome

The expected outcome is a functional and reproducible healthcare data engineering platform that demonstrates how clinical and healthcare reference data can be ingested, preserved, standardised, validated, integrated, and transformed into reliable datasets for healthcare analytics, operational reporting, and evidence-based decision-making.
