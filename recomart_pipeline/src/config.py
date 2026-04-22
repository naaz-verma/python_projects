"""Central configuration for all paths, constants, and shared settings."""

from pathlib import Path
from datetime import date

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_CSV_DIR = RAW_DIR / "csv"
RAW_API_DIR = RAW_DIR / "api"
PREPARED_DIR = DATA_DIR / "prepared"
TRANSFORMED_DIR = DATA_DIR / "transformed"
SPLITS_DIR = DATA_DIR / "splits"
DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "features.db"
FEATURE_STORE_DIR = PROJECT_ROOT / "feature_store"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"

# --- Dataset ---
KAGGLE_DATASET = "retailrocket/ecommerce-dataset"

# --- Pseudo-rating mapping ---
EVENT_RATINGS = {"view": 1, "addtocart": 2, "transaction": 3}

# --- Filtering ---
MIN_USER_INTERACTIONS = 5
MIN_ITEM_INTERACTIONS = 3

# --- Model ---
RATING_SCALE = (1, 3)
RELEVANCE_THRESHOLD = 2  # addtocart + transaction are relevant
K_VALUES = [5, 10]
SVD_DEFAULTS = {"n_factors": 100, "n_epochs": 20, "lr": 0.005, "reg": 0.02}

# --- Split ---
TRAIN_PCT = 0.70
VAL_PCT = 0.15

# --- MLflow ---
EXPERIMENT_NAME = "recomart-recommendation"

# --- API ---
API_HOST = "127.0.0.1"
API_PORT = 8000
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
API_MAX_ROWS_LOADED = 100_000  # subset of item_properties to load into API server


def today() -> str:
    return date.today().isoformat()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_raw_csv_path(data_type: str, dt: str | None = None) -> Path:
    return ensure_dir(RAW_CSV_DIR / data_type / (dt or today()))


def get_raw_api_path(data_type: str, dt: str | None = None) -> Path:
    return ensure_dir(RAW_API_DIR / data_type / (dt or today()))


def get_prepared_path(dt: str | None = None) -> Path:
    return ensure_dir(PREPARED_DIR / (dt or today()))


def get_transformed_path(dt: str | None = None) -> Path:
    return ensure_dir(TRANSFORMED_DIR / (dt or today()))
