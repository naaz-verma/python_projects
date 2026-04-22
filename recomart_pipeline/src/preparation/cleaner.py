"""Task 5: Data cleaning, preparation, and pseudo-rating assignment.

Usage:
    py -3.13 -m src.preparation.cleaner --raw-dir data/raw/csv
"""

import argparse
import logging
from pathlib import Path

import pandas as pd

from src.config import (
    EVENT_RATINGS, MIN_USER_INTERACTIONS, MIN_ITEM_INTERACTIONS,
    get_prepared_path, LOGS_DIR, ensure_dir,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ensure_dir(LOGS_DIR) / "preparation.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def load_events(raw_csv_dir: Path) -> pd.DataFrame:
    events_dirs = sorted((raw_csv_dir / "events").glob("*"))
    if not events_dirs:
        raise FileNotFoundError("No events partitions found")
    path = events_dirs[-1] / "events.csv"
    log.info("Loading events from %s", path)
    return pd.read_csv(path)


def load_item_properties(raw_csv_dir: Path) -> pd.DataFrame:
    ip_dirs = sorted((raw_csv_dir / "item_properties").glob("*"))
    if not ip_dirs:
        raise FileNotFoundError("No item_properties partitions found")
    parts = sorted(ip_dirs[-1].glob("item_properties*.csv"))
    log.info("Loading %d item_properties files", len(parts))
    return pd.concat([pd.read_csv(p) for p in parts], ignore_index=True)


def load_category_tree(raw_csv_dir: Path) -> pd.DataFrame:
    ct_dirs = sorted((raw_csv_dir / "category_tree").glob("*"))
    if not ct_dirs:
        raise FileNotFoundError("No category_tree partitions found")
    path = ct_dirs[-1] / "category_tree.csv"
    log.info("Loading category_tree from %s", path)
    return pd.read_csv(path)


def resolve_item_snapshot(item_props: pd.DataFrame) -> pd.DataFrame:
    """Resolve latest property per (itemid, property) and pivot to one row per item."""
    log.info("Resolving item properties snapshot (%d rows)...", len(item_props))
    latest = (
        item_props.sort_values("timestamp")
        .drop_duplicates(subset=["itemid", "property"], keep="last")
    )
    pivoted = latest.pivot_table(
        index="itemid", columns="property", values="value", aggfunc="first"
    ).reset_index()
    pivoted.columns.name = None

    # Keep useful columns if available
    keep = ["itemid"]
    for col in ["categoryid", "available"]:
        if col in pivoted.columns:
            keep.append(col)
    result = pivoted[keep] if len(keep) > 1 else pivoted[["itemid"]]
    log.info("Item snapshot: %d items", len(result))
    return result


def create_interactions(events: pd.DataFrame) -> pd.DataFrame:
    """Convert events to pseudo-rated interactions.

    - Maps event types to pseudo-ratings: view=1, addtocart=2, transaction=3
    - For duplicate (user, item) pairs, keeps the maximum rating (strongest signal)
    """
    log.info("Creating interactions from %d events...", len(events))
    df = events[["timestamp", "visitorid", "event", "itemid"]].copy()
    df["rating"] = df["event"].map(EVENT_RATINGS)
    df = df.dropna(subset=["rating"])

    # Dedup: keep max rating per (user, item)
    interactions = (
        df.groupby(["visitorid", "itemid"])
        .agg(rating=("rating", "max"), timestamp=("timestamp", "max"))
        .reset_index()
    )
    interactions.rename(columns={"visitorid": "user_id", "itemid": "item_id"}, inplace=True)
    interactions["rating"] = interactions["rating"].astype(int)

    log.info("Interactions after dedup: %d (from %d events)", len(interactions), len(events))
    return interactions


def filter_cold(interactions: pd.DataFrame) -> pd.DataFrame:
    """Remove cold users and items below interaction thresholds."""
    before = len(interactions)

    # Filter cold users
    user_counts = interactions["user_id"].value_counts()
    valid_users = user_counts[user_counts >= MIN_USER_INTERACTIONS].index
    interactions = interactions[interactions["user_id"].isin(valid_users)]
    log.info("After cold-user filter (>=%d): %d → %d", MIN_USER_INTERACTIONS, before, len(interactions))

    # Filter cold items
    before2 = len(interactions)
    item_counts = interactions["item_id"].value_counts()
    valid_items = item_counts[item_counts >= MIN_ITEM_INTERACTIONS].index
    interactions = interactions[interactions["item_id"].isin(valid_items)]
    log.info("After cold-item filter (>=%d): %d → %d", MIN_ITEM_INTERACTIONS, before2, len(interactions))

    return interactions.reset_index(drop=True)


def prepare_all(raw_csv_dir: str | Path, dt: str | None = None) -> dict:
    """Full preparation pipeline.

    Returns:
        Dict with paths to prepared files.
    """
    raw_csv_dir = Path(raw_csv_dir)
    out_dir = get_prepared_path(dt)

    # Load
    events = load_events(raw_csv_dir)
    item_props = load_item_properties(raw_csv_dir)
    categories = load_category_tree(raw_csv_dir)

    # Process
    interactions = create_interactions(events)
    interactions = filter_cold(interactions)
    items = resolve_item_snapshot(item_props)

    # Save
    interactions_path = out_dir / "interactions.csv"
    items_path = out_dir / "items.csv"
    categories_path = out_dir / "categories.csv"

    interactions.to_csv(interactions_path, index=False)
    items.to_csv(items_path, index=False)
    categories.to_csv(categories_path, index=False)

    log.info("Prepared data saved to %s", out_dir)
    log.info("  interactions: %d rows", len(interactions))
    log.info("  items: %d rows", len(items))
    log.info("  categories: %d rows", len(categories))

    return {
        "interactions": str(interactions_path),
        "items": str(items_path),
        "categories": str(categories_path),
        "output_dir": str(out_dir),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and prepare data")
    parser.add_argument("--raw-dir", type=str, default="data/raw/csv")
    parser.add_argument("--date", type=str, default=None)
    args = parser.parse_args()

    results = prepare_all(args.raw_dir, args.date)
    log.info("Preparation complete: %s", results)
