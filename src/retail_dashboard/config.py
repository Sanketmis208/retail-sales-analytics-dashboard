from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = ROOT / "data" / "raw"
DATA_PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"
SQL_DIR = ROOT / "sql"
DB_PATH = DATA_PROCESSED_DIR / "retail_analytics.db"

