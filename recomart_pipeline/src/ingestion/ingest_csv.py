"""Task 2/3: CSV file ingestion into the data lake.

Copies raw Kaggle CSV files into a date-partitioned data lake structure.

Usage:
    py -3.13 -m src.ingestion.ingest_csv --source <kaggle_download_path>
"""

import shutil
import json
import hashlib
import logging
import argparse
from pathlib import Path
from datetime import datetime

from src.config import get_raw_csv_path, LOGS_DIR, ensure_dir, KAGGLE_DATASET

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ensure_dir(LOGS_DIR) / "ingestion.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

FILE_MAP = {
    "events": ["events.csv"],
    "item_properties": ["item_properties_part1.csv", "item_properties_part2.csv"],
    "category_tree": ["category_tree.csv"],
}


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_metadata(target_dir: Path, source_path: Path, files: list[str]):
    meta = {
        "source": str(source_path),
        "ingestion_time": datetime.now().isoformat(),
        "files": {},
    }
    for fname in files:
        fpath = target_dir / fname
        if fpath.exists():
            meta["files"][fname] = {
                "size_bytes": fpath.stat().st_size,
                "md5": _md5(fpath),
            }
    (target_dir / "_metadata.json").write_text(json.dumps(meta, indent=2))


def ingest_csv(source_dir: str | Path, dt: str | None = None) -> dict:
    """Ingest all CSV files from the Kaggle download directory.

    Args:
        source_dir: Path to the directory containing the Kaggle CSV files.
        dt: Date partition string (YYYY-MM-DD). Defaults to today.

    Returns:
        Dict mapping data_type to the target directory path.
    """
    source_dir = Path(source_dir)
    if not source_dir.exists():
        log.error("Source directory does not exist: %s", source_dir)
        raise FileNotFoundError(f"Source not found: {source_dir}")

    results = {}
    for data_type, filenames in FILE_MAP.items():
        target_dir = get_raw_csv_path(data_type, dt)
        log.info("Ingesting %s → %s", data_type, target_dir)

        copied = []
        for fname in filenames:
            src = source_dir / fname
            if not src.exists():
                log.warning("File not found, skipping: %s", src)
                continue
            dst = target_dir / fname
            shutil.copy2(str(src), str(dst))
            size_mb = dst.stat().st_size / (1024 * 1024)
            log.info("  Copied %s (%.1f MB)", fname, size_mb)
            copied.append(fname)

        if copied:
            _write_metadata(target_dir, source_dir, copied)
            log.info("  Metadata written. Files ingested: %d/%d", len(copied), len(filenames))
        else:
            log.warning("  No files ingested for %s", data_type)

        results[data_type] = str(target_dir)

    return results


def download_dataset() -> Path:
    """Download dataset from Kaggle using kagglehub. Returns path to files."""
    import kagglehub
    path = kagglehub.dataset_download(KAGGLE_DATASET)
    log.info("Dataset downloaded to: %s", path)
    return Path(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV files into data lake")
    parser.add_argument("--source", type=str, default=None,
                        help="Path to Kaggle download directory. If omitted, downloads via kagglehub.")
    parser.add_argument("--date", type=str, default=None, help="Date partition (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.source:
        src = Path(args.source)
    else:
        log.info("No source specified. Downloading from Kaggle...")
        src = download_dataset()

    results = ingest_csv(src, args.date)
    log.info("Ingestion complete: %s", results)
