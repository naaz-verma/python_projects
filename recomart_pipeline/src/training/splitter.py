"""Task 9: Train/validation/test split logic.

Usage:
    py -3.13 -m src.training.splitter --interactions data/prepared/<date>/interactions.csv
"""

import argparse
import logging
from pathlib import Path

import pandas as pd

from src.config import SPLITS_DIR, TRAIN_PCT, VAL_PCT, ensure_dir, LOGS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(ensure_dir(LOGS_DIR) / "training.log"),
                              logging.StreamHandler()])
log = logging.getLogger(__name__)


def temporal_split(interactions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split interactions by timestamp: 70% train, 15% val, 15% test."""
    df = interactions.sort_values("timestamp").reset_index(drop=True)
    n = len(df)
    train_end = int(n * TRAIN_PCT)
    val_end = int(n * (TRAIN_PCT + VAL_PCT))

    train = df.iloc[:train_end]
    val = df.iloc[train_end:val_end]
    test = df.iloc[val_end:]

    log.info("Temporal split: train=%d, val=%d, test=%d", len(train), len(val), len(test))
    return train, val, test


def save_splits(train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame,
                output_dir: str | Path | None = None) -> dict:
    """Save split DataFrames to CSV."""
    output_dir = Path(output_dir or SPLITS_DIR)
    ensure_dir(output_dir)

    paths = {}
    for name, df in [("train", train), ("validation", val), ("test", test)]:
        path = output_dir / f"{name}.csv"
        df.to_csv(path, index=False)
        paths[name] = str(path)
        log.info("Saved %s: %d rows", name, len(df))

    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactions", type=str, required=True)
    args = parser.parse_args()

    interactions = pd.read_csv(args.interactions)
    train, val, test = temporal_split(interactions)
    paths = save_splits(train, val, test)
    log.info("Splits saved: %s", paths)
