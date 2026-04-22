"""Task 7: Simple feature store with JSON registry and versioned snapshots.

Usage:
    py -3.13 -m src.feature_store.store --demo
"""

import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd

from src.config import FEATURE_STORE_DIR, ensure_dir


class FeatureStore:
    """File-based feature store with versioned CSV snapshots and JSON registry."""

    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir or FEATURE_STORE_DIR)
        self.registry_path = self.base_dir / "registry.json"
        self.versions_dir = self.base_dir / "versions"
        ensure_dir(self.versions_dir)
        self._registry = self._load_registry()

    def _load_registry(self) -> dict:
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text())
        return {"store_version": "1.0", "created_at": datetime.now().isoformat(), "features": {}}

    def _save_registry(self):
        self.registry_path.write_text(json.dumps(self._registry, indent=2))

    @staticmethod
    def _data_hash(df: pd.DataFrame) -> str:
        csv_bytes = df.to_csv(index=False).encode()
        return hashlib.sha256(csv_bytes).hexdigest()[:16]

    def register(self, name: str, df: pd.DataFrame, description: str,
                 source: str, entity_key: str = "id") -> str:
        """Register a versioned feature snapshot.

        Returns:
            Version ID string (e.g., "v3_20260422").
        """
        # Determine version number
        existing = self._registry.get("features", {}).get(name, {}).get("versions", [])
        version_num = len(existing) + 1
        version_id = f"v{version_num}_{datetime.now().strftime('%Y%m%d')}"

        # Save CSV snapshot
        version_dir = ensure_dir(self.versions_dir / version_id)
        csv_path = version_dir / f"{name}.csv"
        df.to_csv(csv_path, index=False)

        # Update registry
        if name not in self._registry.setdefault("features", {}):
            self._registry["features"][name] = {
                "description": description,
                "entity_key": entity_key,
                "columns": [{"name": c, "dtype": str(df[c].dtype)} for c in df.columns],
                "source_code": source,
                "versions": [],
            }

        self._registry["features"][name]["versions"].append({
            "version_id": version_id,
            "created_at": datetime.now().isoformat(),
            "row_count": len(df),
            "file_path": str(csv_path.relative_to(self.base_dir)),
            "data_hash": self._data_hash(df),
        })
        self._save_registry()

        print(f"Registered {name} as {version_id} ({len(df)} rows)")
        return version_id

    def get(self, name: str, version: str = "latest") -> pd.DataFrame:
        """Retrieve a feature DataFrame by name and version."""
        feat = self._registry.get("features", {}).get(name)
        if not feat or not feat["versions"]:
            raise KeyError(f"Feature '{name}' not found or has no versions")

        if version == "latest":
            ver = feat["versions"][-1]
        else:
            ver = next((v for v in feat["versions"] if v["version_id"] == version), None)
            if not ver:
                raise KeyError(f"Version '{version}' not found for '{name}'")

        csv_path = self.base_dir / ver["file_path"]
        return pd.read_csv(csv_path)

    def list_versions(self, name: str | None = None) -> list[dict]:
        """List all versions, optionally filtered by feature name."""
        if name:
            feat = self._registry.get("features", {}).get(name, {})
            return feat.get("versions", [])
        result = []
        for fname, fdata in self._registry.get("features", {}).items():
            for v in fdata.get("versions", []):
                result.append({"feature": fname, **v})
        return result

    def get_metadata(self, name: str) -> dict:
        """Return metadata for a feature."""
        return self._registry.get("features", {}).get(name, {})


def register_features(transformed_dir: str | Path) -> dict:
    """Register all transformed features into the feature store."""
    transformed_dir = Path(transformed_dir)
    store = FeatureStore()
    versions = {}

    for fname, desc, entity in [
        ("user_features.csv", "Per-user aggregated interaction statistics", "user_id"),
        ("item_features.csv", "Per-item aggregated interaction statistics", "item_id"),
        ("cooccurrence.csv", "Pairwise item co-occurrence counts", "item_a"),
    ]:
        path = transformed_dir / fname
        if path.exists():
            df = pd.read_csv(path)
            name = fname.replace(".csv", "")
            vid = store.register(name, df, desc, f"src/transformation/features.py::{name}", entity)
            versions[name] = vid

    return versions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transformed-dir", type=str, default=None)
    parser.add_argument("--demo", action="store_true", help="Show retrieval demo")
    args = parser.parse_args()

    if args.transformed_dir:
        versions = register_features(args.transformed_dir)
        print("Registered:", versions)

    if args.demo:
        store = FeatureStore()
        print("\nAll versions:")
        for v in store.list_versions():
            print(f"  {v['feature']}: {v['version_id']} ({v['row_count']} rows)")
        print("\nSample user_features (latest):")
        try:
            print(store.get("user_features").head())
        except KeyError as e:
            print(f"  {e}")
