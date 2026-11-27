import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Load the warehouse database credentials
ENV_FILE = PROJECT_ROOT / "docker" / "warehouse" / ".env"
load_dotenv(ENV_FILE)


def get_database_url():
    """Build the PostgreSQL connection URL."""
    required_variables = [
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ]

    missing = [v for v in required_variables if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing database environment variables: {missing}")

    # From Windows: localhost:5433
    # From Airflow in Docker: set POSTGRES_HOST=warehouse-db and POSTGRES_PORT=5432
    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        database=os.getenv("POSTGRES_DB"),
    )


def get_engine():
    """Return a SQLAlchemy engine for the healthcare warehouse."""
    return create_engine(get_database_url(), pool_pre_ping=True)


def test_connection():
    """Run a simple query and return (database name, server time)."""
    engine = get_engine()
    with engine.connect() as connection:
        row = connection.execute(
            text("SELECT current_database(), CURRENT_TIMESTAMP;")
        ).fetchone()
    return row
