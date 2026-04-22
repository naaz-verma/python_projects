"""Task 4: Data profiling and validation checks.

Runs schema, null, duplicate, and range checks on raw data.

Usage:
    py -3.13 -m src.validation.validators --raw-dir data/raw/csv
"""

import argparse
import logging
from dataclasses import dataclass, asdict
from pathlib import Path

import pandas as pd

from src.config import LOGS_DIR, ensure_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ensure_dir(LOGS_DIR) / "validation.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    dataset: str
    check_name: str
    passed: bool
    details: str
    severity: str = "error"  # "error" or "warning"

    def to_dict(self):
        return asdict(self)


# --- Generic checks ---

def check_schema(df: pd.DataFrame, expected_cols: list[str], name: str) -> ValidationResult:
    actual = set(df.columns)
    expected = set(expected_cols)
    missing = expected - actual
    extra = actual - expected
    passed = len(missing) == 0
    details = f"Expected {expected_cols}. Missing: {missing or 'none'}. Extra: {extra or 'none'}."
    return ValidationResult(name, "schema_check", passed, details)


def check_nulls(df: pd.DataFrame, required_cols: list[str], name: str) -> ValidationResult:
    null_counts = {c: int(df[c].isnull().sum()) for c in required_cols if c in df.columns}
    total_nulls = sum(null_counts.values())
    passed = total_nulls == 0
    details = f"Null counts in required columns: {null_counts}" if not passed else "No nulls in required columns."
    return ValidationResult(name, "null_check", passed, details, "error" if not passed else "error")


def check_duplicates(df: pd.DataFrame, subset: list[str], name: str) -> ValidationResult:
    valid_cols = [c for c in subset if c in df.columns]
    dup_count = int(df.duplicated(subset=valid_cols).sum())
    passed = dup_count == 0
    details = f"Duplicate rows (on {valid_cols}): {dup_count} / {len(df)}"
    return ValidationResult(name, "duplicate_check", passed, details, "warning")


def check_value_set(df: pd.DataFrame, col: str, valid_values: set, name: str) -> ValidationResult:
    if col not in df.columns:
        return ValidationResult(name, f"value_set_{col}", False, f"Column '{col}' not found.")
    actual = set(df[col].dropna().unique())
    invalid = actual - valid_values
    passed = len(invalid) == 0
    details = f"Valid: {valid_values}. Found invalid: {invalid}" if not passed else f"All values in {valid_values}."
    return ValidationResult(name, f"value_set_{col}", passed, details)


def check_positive(df: pd.DataFrame, cols: list[str], name: str) -> ValidationResult:
    issues = {}
    for c in cols:
        if c in df.columns:
            neg = int((df[c].dropna() < 0).sum())
            if neg > 0:
                issues[c] = neg
    passed = len(issues) == 0
    details = f"Negative values: {issues}" if not passed else "All IDs positive."
    return ValidationResult(name, "positive_check", passed, details)


# --- Dataset-specific validators ---

def validate_events(df: pd.DataFrame) -> list[ValidationResult]:
    name = "events"
    return [
        check_schema(df, ["timestamp", "visitorid", "event", "itemid", "transactionid"], name),
        check_nulls(df, ["timestamp", "visitorid", "event", "itemid"], name),
        check_duplicates(df, ["timestamp", "visitorid", "event", "itemid"], name),
        check_value_set(df, "event", {"view", "addtocart", "transaction"}, name),
        check_positive(df, ["visitorid", "itemid"], name),
    ]


def validate_item_properties(df: pd.DataFrame) -> list[ValidationResult]:
    name = "item_properties"
    return [
        check_schema(df, ["timestamp", "itemid", "property", "value"], name),
        check_nulls(df, ["timestamp", "itemid", "property"], name),
        check_positive(df, ["itemid"], name),
    ]


def validate_category_tree(df: pd.DataFrame) -> list[ValidationResult]:
    name = "category_tree"
    results = [
        check_schema(df, ["categoryid", "parentid"], name),
        check_nulls(df, ["categoryid"], name),
    ]
    # Check for self-referencing
    if "categoryid" in df.columns and "parentid" in df.columns:
        self_ref = df[df["categoryid"] == df["parentid"]]
        results.append(ValidationResult(
            name, "self_reference_check",
            len(self_ref) == 0,
            f"Self-referencing categories: {len(self_ref)}"
        ))
    return results


# --- Profiling ---

def profile_dataframe(df: pd.DataFrame, name: str) -> dict:
    """Generate profiling statistics for a DataFrame."""
    profile = {
        "name": name,
        "rows": len(df),
        "columns": len(df.columns),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_stats": {},
    }
    for col in df.columns:
        stats = {
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isnull().sum()),
            "null_pct": round(df[col].isnull().mean() * 100, 2),
            "unique_count": int(df[col].nunique()),
        }
        if pd.api.types.is_numeric_dtype(df[col]):
            stats["min"] = float(df[col].min()) if not df[col].isnull().all() else None
            stats["max"] = float(df[col].max()) if not df[col].isnull().all() else None
            stats["mean"] = round(float(df[col].mean()), 4) if not df[col].isnull().all() else None
        profile["column_stats"][col] = stats
    return profile


def validate_all(raw_csv_dir: str | Path) -> dict:
    """Run validation on all raw datasets.

    Returns:
        Dict with 'results' (list of ValidationResult dicts) and 'profiles' (dict of profiles).
    """
    raw_csv_dir = Path(raw_csv_dir)
    all_results = []
    profiles = {}

    # Events
    events_dirs = sorted((raw_csv_dir / "events").glob("*"))
    if events_dirs:
        events_path = events_dirs[-1] / "events.csv"  # latest partition
        if events_path.exists():
            log.info("Validating events: %s", events_path)
            df = pd.read_csv(events_path)
            all_results.extend(validate_events(df))
            profiles["events"] = profile_dataframe(df, "events")

    # Item properties (just part 1 for validation)
    ip_dirs = sorted((raw_csv_dir / "item_properties").glob("*"))
    if ip_dirs:
        ip_path = ip_dirs[-1] / "item_properties_part1.csv"
        if ip_path.exists():
            log.info("Validating item_properties: %s", ip_path)
            df = pd.read_csv(ip_path, nrows=500_000)
            all_results.extend(validate_item_properties(df))
            profiles["item_properties"] = profile_dataframe(df, "item_properties")

    # Category tree
    ct_dirs = sorted((raw_csv_dir / "category_tree").glob("*"))
    if ct_dirs:
        ct_path = ct_dirs[-1] / "category_tree.csv"
        if ct_path.exists():
            log.info("Validating category_tree: %s", ct_path)
            df = pd.read_csv(ct_path)
            all_results.extend(validate_category_tree(df))
            profiles["category_tree"] = profile_dataframe(df, "category_tree")

    # Log results
    passed = sum(1 for r in all_results if r.passed)
    total = len(all_results)
    log.info("Validation: %d/%d checks passed", passed, total)
    for r in all_results:
        status = "PASS" if r.passed else "FAIL"
        log.info("  [%s] %s.%s: %s", status, r.dataset, r.check_name, r.details)

    return {
        "results": [r.to_dict() for r in all_results],
        "profiles": profiles,
        "summary": {"passed": passed, "failed": total - passed, "total": total},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate raw data")
    parser.add_argument("--raw-dir", type=str, default="data/raw/csv")
    args = parser.parse_args()

    from src.validation.quality_report import generate_report
    validation = validate_all(args.raw_dir)
    generate_report(validation)
