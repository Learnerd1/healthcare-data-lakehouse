import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from health_lakehouse.ingestion.fhir_loader import load_fhir_folder


def main():
    folder = PROJECT_ROOT / "data" / "raw" / "synthea"
    result = load_fhir_folder(folder, source_system="synthea_r4_100")
    print("BRONZE LOAD RESULT")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
