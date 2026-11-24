# Healthcare Data Lakehouse

A healthcare data engineering project built with Python, Apache Airflow, PostgreSQL, and Docker. This project demonstrates the design and implementation of an integrated hospital clinical data lakehouse that ingests, processes, standardises, and integrates healthcare data from multiple sources to support analytics, reporting, and evidence-based decision-making.

## Overview

This project focuses on building an end-to-end healthcare data pipeline that brings together clinical and administrative data from different hospital information sources.

The project adopts a Medallion Architecture (Bronze, Silver, and Gold) to organise data processing and transformation into distinct layers:

**Bronze Layer:** Ingests and stores raw healthcare data from different sources while preserving the original structure and values.

**Silver Layer:** Applies data cleaning, standardisation, deduplication, validation, and quality checks to produce consistent and reliable healthcare datasets.

**Gold Layer:** Integrates processed datasets into analytics-ready tables and models to support hospital reporting, operational analytics, and clinical data analysis.

The initial implementation focuses on three major healthcare data domains:

- **Patient Registration Data:** Patient demographic and registration information.
- **Encounter Data:** Outpatient and inpatient visits and associated clinical encounters.
- **Laboratory Data:** Laboratory requests, investigations, and test results.

The architecture is designed to accommodate additional healthcare domains, including radiology, diagnoses, procedures, pharmacy, and billing data as the project evolves.

Both synthetic and publicly available datasets are considered to demonstrate healthcare data integration while maintaining a practical and reproducible development environment.

Data ingestion and transformation workflows are orchestrated using Apache Airflow, while Docker and Docker Compose provide a containerised environment for running the project services.

## Tech Stack

- Python
- Apache Airflow
- PostgreSQL
- Docker & Docker Compose
- Pandas
- SQL
- Git & GitHub
- FHIR (Healthcare Data Interoperability)
- SNOMED CT (Clinical Terminology Standardisation)

## Architecture

The project follows a Medallion Lakehouse Architecture:

**Data Sources → Bronze → Silver → Gold → Analytics & Reporting**

Each layer serves a specific purpose in transforming raw healthcare data into integrated, standardised, and analytics-ready information.

## Objective

Design and implement an end-to-end healthcare data lakehouse that integrates clinical and administrative hospital data from multiple sources, applies data quality controls and standardisation processes, and produces reliable, analytics-ready datasets using Python, SQL, PostgreSQL, and Apache Airflow.
