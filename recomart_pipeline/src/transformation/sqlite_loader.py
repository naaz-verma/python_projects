"""Task 6: SQLite schema creation and feature loading.

Usage:
    py -3.13 -m src.transformation.sqlite_loader --transformed-dir data/transformed/<date>
"""

import argparse
import sqlite3
import logging
from pathlib import Path

import pandas as pd

from src.config import DB_PATH, ensure_dir, LOGS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(ensure_dir(LOGS_DIR) / "transformation.log"),
                              logging.StreamHandler()])
log = logging.getLogger(__name__)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS user_features (
    user_id INTEGER PRIMARY KEY, total_interactions INTEGER, unique_items INTEGER,
    avg_rating REAL, view_count INTEGER, cart_count INTEGER, transaction_count INTEGER,
    activity_days INTEGER, avg_daily_interactions REAL, recency_days INTEGER,
    conversion_rate REAL, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS item_features (
    item_id INTEGER PRIMARY KEY, total_interactions INTEGER, unique_users INTEGER,
    avg_rating REAL, view_count INTEGER, cart_count INTEGER, transaction_count INTEGER,
    popularity_rank INTEGER, categoryid INTEGER, created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS item_cooccurrence (
    item_a INTEGER, item_b INTEGER, co_occurrence_count INTEGER,
    PRIMARY KEY (item_a, item_b)
);
CREATE TABLE IF NOT EXISTS feature_metadata (
    feature_name TEXT PRIMARY KEY, description TEXT, source_table TEXT,
    computation TEXT, version TEXT, created_at TEXT DEFAULT (datetime('now'))
);
"""

METADATA_ROWS = [
    ("total_interactions", "Total event count", "user_features/item_features", "COUNT(*)"),
    ("unique_items", "Distinct items per user", "user_features", "COUNT(DISTINCT item_id)"),
    ("avg_rating", "Mean pseudo-rating (1=view,2=cart,3=txn)", "user_features/item_features", "AVG(rating)"),
    ("conversion_rate", "Transactions / views", "user_features", "transaction_count / view_count"),
    ("popularity_rank", "Rank by interaction count", "item_features", "RANK() OVER (ORDER BY total_interactions DESC)"),
    ("co_occurrence_count", "Users interacting with both items", "item_cooccurrence", "COUNT intersecting users"),
]


def create_schema(db_path: str | Path | None = None):
    db_path = Path(db_path or DB_PATH)
    ensure_dir(db_path.parent)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA_SQL)
    for name, desc, table, comp in METADATA_ROWS:
        conn.execute(
            "INSERT OR REPLACE INTO feature_metadata (feature_name, description, source_table, computation, version) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, desc, table, comp, "v1"),
        )
    conn.commit()
    conn.close()
    log.info("Schema created at %s", db_path)


def load_features(transformed_dir: str | Path, db_path: str | Path | None = None):
    """Load feature CSVs into SQLite."""
    transformed_dir = Path(transformed_dir)
    db_path = Path(db_path or DB_PATH)
    create_schema(db_path)

    conn = sqlite3.connect(str(db_path))

    for fname, table in [("user_features.csv", "user_features"),
                          ("item_features.csv", "item_features"),
                          ("cooccurrence.csv", "item_cooccurrence")]:
        fpath = transformed_dir / fname
        if fpath.exists():
            df = pd.read_csv(fpath)
            df.to_sql(table, conn, if_exists="replace", index=False)
            log.info("Loaded %d rows into %s", len(df), table)

    conn.close()
    log.info("Features loaded into %s", db_path)


def query_features(table: str, ids: list | None = None, db_path: str | Path | None = None) -> pd.DataFrame:
    """Query features from SQLite."""
    db_path = Path(db_path or DB_PATH)
    conn = sqlite3.connect(str(db_path))
    if ids:
        id_col = "user_id" if table == "user_features" else "item_id"
        placeholders = ",".join("?" * len(ids))
        df = pd.read_sql(f"SELECT * FROM {table} WHERE {id_col} IN ({placeholders})", conn, params=ids)
    else:
        df = pd.read_sql(f"SELECT * FROM {table} LIMIT 100", conn)
    conn.close()
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transformed-dir", type=str, required=True)
    args = parser.parse_args()
    load_features(args.transformed_dir)
