"""Task 2: REST API ingestion with retry, pagination, and logging.

Fetches product data from the mock FastAPI server and stores as JSON.

Usage:
    py -3.13 -m src.ingestion.ingest_api
"""

import json
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config import API_BASE_URL, get_raw_api_path, LOGS_DIR, ensure_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ensure_dir(LOGS_DIR) / "ingestion.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def _get_session() -> requests.Session:
    """Create a session with retry logic."""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def ingest_item_properties(base_url: str, dt: str | None = None, max_pages: int = 200) -> str:
    """Fetch item properties from API with pagination.

    Returns:
        Path to the saved JSON file.
    """
    session = _get_session()
    target_dir = get_raw_api_path("item_properties", dt)
    all_data = []
    page = 1

    log.info("Ingesting item_properties from API: %s", base_url)

    while page <= max_pages:
        url = f"{base_url}/api/v1/item_properties?page={page}&page_size=5000"
        start = time.time()
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            log.error("API request failed at page %d: %s", page, e)
            break

        elapsed = time.time() - start
        body = resp.json()
        rows = body.get("data", [])
        all_data.extend(rows)
        log.info("  Page %d: %d rows (%.2fs)", page, len(rows), elapsed)

        if not body.get("has_next", False):
            break
        page += 1

    # Save
    out_path = target_dir / "item_properties.json"
    out_path.write_text(json.dumps(all_data, indent=2))

    meta = {
        "source_url": f"{base_url}/api/v1/item_properties",
        "ingestion_time": datetime.now().isoformat(),
        "pages_fetched": page,
        "total_rows": len(all_data),
    }
    (target_dir / "_metadata.json").write_text(json.dumps(meta, indent=2))
    log.info("  Saved %d rows to %s", len(all_data), out_path)

    return str(target_dir)


def ingest_category_tree(base_url: str, dt: str | None = None) -> str:
    """Fetch category tree from API.

    Returns:
        Path to the saved JSON file.
    """
    session = _get_session()
    target_dir = get_raw_api_path("category_tree", dt)
    url = f"{base_url}/api/v1/category_tree"

    log.info("Ingesting category_tree from API: %s", url)

    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        log.error("API request failed: %s", e)
        raise

    body = resp.json()
    data = body.get("data", [])

    out_path = target_dir / "category_tree.json"
    out_path.write_text(json.dumps(data, indent=2))

    meta = {
        "source_url": url,
        "ingestion_time": datetime.now().isoformat(),
        "total_rows": len(data),
    }
    (target_dir / "_metadata.json").write_text(json.dumps(meta, indent=2))
    log.info("  Saved %d rows to %s", len(data), out_path)

    return str(target_dir)


def ingest_all_api(base_url: str, dt: str | None = None) -> dict:
    """Ingest all data from the mock API."""
    return {
        "item_properties": ingest_item_properties(base_url, dt),
        "category_tree": ingest_category_tree(base_url, dt),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data from mock REST API")
    parser.add_argument("--url", type=str, default=API_BASE_URL, help="API base URL")
    parser.add_argument("--date", type=str, default=None, help="Date partition")
    args = parser.parse_args()

    results = ingest_all_api(args.url, args.date)
    log.info("API ingestion complete: %s", results)
