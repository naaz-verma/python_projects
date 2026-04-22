"""Task 2: Mock FastAPI server for product data.

Serves item_properties and category_tree as REST API endpoints,
satisfying the "at least 2 ingestion types" requirement.

Usage:
    py -3.13 -m src.api.server
"""

import argparse
from pathlib import Path
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Query, HTTPException
import uvicorn

from src.config import API_HOST, API_PORT, API_MAX_ROWS_LOADED

# Global state filled on startup
_item_props: pd.DataFrame = pd.DataFrame()
_category_tree: pd.DataFrame = pd.DataFrame()


def _load_data(data_dir: Path):
    """Load CSVs into memory for serving."""
    global _item_props, _category_tree

    # Load item properties (subset for memory)
    ip_files = sorted(data_dir.glob("item_properties*.csv"))
    if ip_files:
        chunks = []
        for f in ip_files:
            chunks.append(pd.read_csv(f, nrows=API_MAX_ROWS_LOADED // len(ip_files)))
        _item_props = pd.concat(chunks, ignore_index=True)
        # Resolve to latest snapshot per (itemid, property)
        _item_props = (
            _item_props.sort_values("timestamp")
            .drop_duplicates(subset=["itemid", "property"], keep="last")
        )

    # Load category tree (small file)
    ct_path = data_dir / "category_tree.csv"
    if ct_path.exists():
        _category_tree = pd.read_csv(ct_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: data is loaded via CLI arg, see __main__
    yield


app = FastAPI(title="RecoMart Product Data API", version="1.0", lifespan=lifespan)


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "item_properties_rows": len(_item_props),
        "category_tree_rows": len(_category_tree),
    }


@app.get("/api/v1/item_properties")
def get_item_properties(
    page: int = Query(1, ge=1),
    page_size: int = Query(1000, ge=1, le=10000),
    item_id: int | None = Query(None),
):
    df = _item_props
    if item_id is not None:
        df = df[df["itemid"] == item_id]

    total = len(df)
    start = (page - 1) * page_size
    end = start + page_size
    subset = df.iloc[start:end]

    return {
        "data": subset.to_dict(orient="records"),
        "page": page,
        "page_size": page_size,
        "total_count": total,
        "has_next": end < total,
    }


@app.get("/api/v1/category_tree")
def get_category_tree():
    return {
        "data": _category_tree.to_dict(orient="records"),
        "total_count": len(_category_tree),
    }


@app.get("/api/v1/category_tree/{category_id}")
def get_category(category_id: int):
    row = _category_tree[_category_tree["categoryid"] == category_id]
    if row.empty:
        raise HTTPException(404, f"Category {category_id} not found")
    return row.iloc[0].to_dict()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start mock product data API")
    parser.add_argument("--data-dir", type=str, required=True,
                        help="Directory containing Kaggle CSV files")
    parser.add_argument("--host", type=str, default=API_HOST)
    parser.add_argument("--port", type=int, default=API_PORT)
    args = parser.parse_args()

    _load_data(Path(args.data_dir))
    print(f"Loaded {len(_item_props)} item properties, {len(_category_tree)} categories")
    uvicorn.run(app, host=args.host, port=args.port)
