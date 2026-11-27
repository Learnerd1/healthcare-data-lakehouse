import sys
from pathlib import Path

# Make the src directory importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from health_lakehouse.database.connection import test_connection


def main():
    try:
        result = test_connection()
        print("DATABASE CONNECTION SUCCESSFUL")
        print(f"Database: {result[0]}")
        print(f"Server time: {result[1]}")
    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
