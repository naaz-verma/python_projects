"""Task 10: Prefect-orchestrated end-to-end pipeline.

Wires all stages into a DAG:
  ingest_csv + ingest_api (parallel) -> validate -> prepare ->
  transform -> sqlite + feature_store -> version -> split -> train

Usage:
    py -3.13 -m src.orchestration.pipeline --source <kaggle_dir>
    py -3.13 -m src.orchestration.pipeline --source <kaggle_dir> --skip-api
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
from prefect import flow, task

from src.config import (
    RAW_CSV_DIR, API_BASE_URL, REPORTS_DIR,
    LOGS_DIR, ensure_dir, today,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ensure_dir(LOGS_DIR) / "pipeline.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Prefect tasks — thin wrappers around module functions
# ---------------------------------------------------------------------------

@task(name="ingest_csv", retries=1, log_prints=True)
def task_ingest_csv(source_dir: str, dt: str) -> dict:
    from src.ingestion.ingest_csv import ingest_csv
    return ingest_csv(source_dir, dt)


@task(name="ingest_api", retries=1, log_prints=True)
def task_ingest_api(base_url: str, dt: str) -> dict:
    from src.ingestion.ingest_api import ingest_all_api
    return ingest_all_api(base_url, dt)


@task(name="validate", log_prints=True)
def task_validate(raw_csv_dir: str) -> dict:
    from src.validation.validators import validate_all
    return validate_all(raw_csv_dir)


@task(name="quality_report", log_prints=True)
def task_quality_report(validation: dict):
    from src.validation.quality_report import generate_report
    output = ensure_dir(REPORTS_DIR) / "data_quality_report.pdf"
    generate_report(validation, str(output))
    return str(output)


@task(name="prepare", log_prints=True)
def task_prepare(raw_csv_dir: str, dt: str) -> dict:
    from src.preparation.cleaner import prepare_all
    return prepare_all(raw_csv_dir, dt)


@task(name="transform", log_prints=True)
def task_transform(prepared_dir: str, dt: str) -> dict:
    from src.transformation.features import transform_all
    return transform_all(prepared_dir, dt)


@task(name="load_sqlite", log_prints=True)
def task_load_sqlite(transformed_dir: str):
    from src.transformation.sqlite_loader import create_schema, load_features
    create_schema()
    load_features(transformed_dir)


@task(name="register_features", log_prints=True)
def task_register_features(transformed_dir: str) -> dict:
    from src.feature_store.store import register_features
    return register_features(transformed_dir)


@task(name="version_data", log_prints=True)
def task_version_data():
    from src.versioning.dvc_ops import init_dvc, track_all
    init_dvc()
    track_all()


@task(name="split_data", log_prints=True)
def task_split_data(prepared_dir: str) -> dict:
    from src.training.splitter import temporal_split, save_splits
    interactions = pd.read_csv(Path(prepared_dir) / "interactions.csv")
    train, val, test = temporal_split(interactions)
    return save_splits(train, val, test)


@task(name="train_model", log_prints=True)
def task_train_model() -> dict:
    from src.training.train import run_training
    return run_training()


# ---------------------------------------------------------------------------
# Prefect flow
# ---------------------------------------------------------------------------

@flow(name="recomart-pipeline", log_prints=True)
def recomart_pipeline(
    source_dir: str,
    dt: str | None = None,
    skip_api: bool = False,
    base_url: str = API_BASE_URL,
):
    """Full RecoMart data + ML pipeline.

    Args:
        source_dir: Path to Kaggle download directory with CSV files.
        dt: Date partition string (YYYY-MM-DD). Defaults to today.
        skip_api: If True, skip API ingestion (useful when API server is not running).
        base_url: Base URL of mock FastAPI server.
    """
    dt = dt or today()
    log.info("=== RecoMart Pipeline START (dt=%s) ===", dt)

    # --- Stage 1: Ingestion (parallel) ---
    csv_result = task_ingest_csv.submit(source_dir, dt)

    api_result = None
    if not skip_api:
        api_result = task_ingest_api.submit(base_url, dt)

    csv_paths = csv_result.result()
    log.info("CSV ingestion done: %s", csv_paths)

    if api_result is not None:
        api_paths = api_result.result()
        log.info("API ingestion done: %s", api_paths)

    # --- Stage 2: Validation ---
    raw_csv_dir = str(RAW_CSV_DIR)
    validation = task_validate(raw_csv_dir)
    log.info("Validation: %d checks, %d passed",
             validation["summary"]["total_checks"],
             validation["summary"]["passed"])

    # --- Stage 3: Quality report ---
    report_path = task_quality_report(validation)
    log.info("DQ report: %s", report_path)

    # --- Stage 4: Preparation ---
    prep_result = task_prepare(raw_csv_dir, dt)
    prepared_dir = prep_result["prepared_dir"]
    log.info("Preparation done: %s", prepared_dir)

    # --- Stage 5: Feature engineering ---
    transform_result = task_transform(prepared_dir, dt)
    transformed_dir = transform_result["transformed_dir"]
    log.info("Transformation done: %s", transformed_dir)

    # --- Stage 6: SQLite + Feature store (parallel) ---
    sqlite_future = task_load_sqlite.submit(transformed_dir)
    fs_future = task_register_features.submit(transformed_dir)

    sqlite_future.result()
    log.info("SQLite loaded")

    fs_versions = fs_future.result()
    log.info("Feature store: %s", fs_versions)

    # --- Stage 7: Data versioning ---
    task_version_data()
    log.info("DVC versioning done")

    # --- Stage 8: Split + Train ---
    split_paths = task_split_data(prepared_dir)
    log.info("Splits: %s", split_paths)

    train_result = task_train_model()
    log.info("Training done: %s", train_result)

    log.info("=== RecoMart Pipeline COMPLETE ===")
    return {
        "dt": dt,
        "validation_summary": validation["summary"],
        "prepared_dir": prepared_dir,
        "transformed_dir": transformed_dir,
        "feature_store_versions": fs_versions,
        "split_paths": split_paths,
        "training": train_result,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RecoMart pipeline")
    parser.add_argument("--source", type=str, required=True,
                        help="Path to Kaggle CSV directory")
    parser.add_argument("--date", type=str, default=None,
                        help="Date partition (YYYY-MM-DD)")
    parser.add_argument("--skip-api", action="store_true",
                        help="Skip API ingestion")
    parser.add_argument("--base-url", type=str, default=API_BASE_URL,
                        help="Mock API base URL")
    args = parser.parse_args()

    result = recomart_pipeline(
        source_dir=args.source,
        dt=args.date,
        skip_api=args.skip_api,
        base_url=args.base_url,
    )
    print("Pipeline result:", result)
