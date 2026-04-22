"""Task 6: Feature engineering — user, item, and co-occurrence features.

Usage:
    py -3.13 -m src.transformation.features --prepared-dir data/prepared/<date>
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
import numpy as np

from src.config import get_transformed_path, LOGS_DIR, ensure_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ensure_dir(LOGS_DIR) / "transformation.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def compute_user_features(interactions: pd.DataFrame) -> pd.DataFrame:
    """Compute per-user aggregated features."""
    log.info("Computing user features...")

    # Convert timestamp to days
    interactions = interactions.copy()
    interactions["day"] = pd.to_datetime(interactions["timestamp"], unit="ms").dt.date

    user = interactions.groupby("user_id").agg(
        total_interactions=("item_id", "count"),
        unique_items=("item_id", "nunique"),
        avg_rating=("rating", "mean"),
        activity_days=("day", "nunique"),
    ).reset_index()

    # Per-event counts
    for rating_val, event_name in [(1, "view"), (2, "cart"), (3, "transaction")]:
        counts = interactions[interactions["rating"] == rating_val].groupby("user_id").size()
        user[f"{event_name}_count"] = user["user_id"].map(counts).fillna(0).astype(int)

    # Derived features
    user["avg_daily_interactions"] = (user["total_interactions"] / user["activity_days"]).round(4)
    max_ts = interactions["timestamp"].max()
    last_ts = interactions.groupby("user_id")["timestamp"].max()
    user["recency_days"] = user["user_id"].map(
        lambda uid: int((max_ts - last_ts.get(uid, max_ts)) / (1000 * 86400))
    )
    user["conversion_rate"] = (user["transaction_count"] / user["view_count"].replace(0, np.nan)).fillna(0).round(4)

    log.info("User features computed: %d users, %d features", len(user), len(user.columns) - 1)
    return user


def compute_item_features(interactions: pd.DataFrame, items: pd.DataFrame | None = None) -> pd.DataFrame:
    """Compute per-item aggregated features."""
    log.info("Computing item features...")

    item = interactions.groupby("item_id").agg(
        total_interactions=("user_id", "count"),
        unique_users=("user_id", "nunique"),
        avg_rating=("rating", "mean"),
    ).reset_index()

    for rating_val, event_name in [(1, "view"), (2, "cart"), (3, "transaction")]:
        counts = interactions[interactions["rating"] == rating_val].groupby("item_id").size()
        item[f"{event_name}_count"] = item["item_id"].map(counts).fillna(0).astype(int)

    item["popularity_rank"] = item["total_interactions"].rank(ascending=False, method="min").astype(int)

    # Merge category from items snapshot if available
    if items is not None and "categoryid" in items.columns:
        items_sub = items[["itemid", "categoryid"]].rename(columns={"itemid": "item_id"})
        items_sub["item_id"] = items_sub["item_id"].astype(item["item_id"].dtype)
        item = item.merge(items_sub, on="item_id", how="left")
        item["categoryid"] = item["categoryid"].fillna(-1)
    else:
        item["categoryid"] = -1

    log.info("Item features computed: %d items, %d features", len(item), len(item.columns) - 1)
    return item


def compute_cooccurrence(interactions: pd.DataFrame, top_n: int = 100) -> pd.DataFrame:
    """Compute item co-occurrence for top-N popular items."""
    log.info("Computing co-occurrence for top %d items...", top_n)

    # Get top-N items
    top_items = interactions["item_id"].value_counts().head(top_n).index.tolist()
    filtered = interactions[interactions["item_id"].isin(top_items)]

    # Build user-item sets
    user_items = filtered.groupby("user_id")["item_id"].apply(set).to_dict()

    # Compute pairwise co-occurrence
    pairs = {}
    for items_set in user_items.values():
        items_list = sorted(items_set)
        for i in range(len(items_list)):
            for j in range(i + 1, len(items_list)):
                key = (items_list[i], items_list[j])
                pairs[key] = pairs.get(key, 0) + 1

    cooc = pd.DataFrame(
        [(a, b, c) for (a, b), c in pairs.items()],
        columns=["item_a", "item_b", "co_occurrence_count"],
    )
    cooc = cooc.sort_values("co_occurrence_count", ascending=False).reset_index(drop=True)
    log.info("Co-occurrence pairs: %d", len(cooc))
    return cooc


def transform_all(prepared_dir: str | Path, dt: str | None = None) -> dict:
    """Run all feature computations and save results."""
    prepared_dir = Path(prepared_dir)
    out_dir = get_transformed_path(dt)

    interactions = pd.read_csv(prepared_dir / "interactions.csv")
    items_path = prepared_dir / "items.csv"
    items = pd.read_csv(items_path) if items_path.exists() else None

    user_feat = compute_user_features(interactions)
    item_feat = compute_item_features(interactions, items)
    cooc = compute_cooccurrence(interactions)

    user_path = out_dir / "user_features.csv"
    item_path = out_dir / "item_features.csv"
    cooc_path = out_dir / "cooccurrence.csv"

    user_feat.to_csv(user_path, index=False)
    item_feat.to_csv(item_path, index=False)
    cooc.to_csv(cooc_path, index=False)

    log.info("Transformed data saved to %s", out_dir)
    return {
        "user_features": str(user_path),
        "item_features": str(item_path),
        "cooccurrence": str(cooc_path),
        "output_dir": str(out_dir),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute features")
    parser.add_argument("--prepared-dir", type=str, required=True)
    parser.add_argument("--date", type=str, default=None)
    args = parser.parse_args()

    results = transform_all(args.prepared_dir, args.date)
    log.info("Feature engineering complete: %s", results)
