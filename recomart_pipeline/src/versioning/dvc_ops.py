"""Task 8: DVC integration for data versioning and lineage.

Usage:
    py -3.13 -m src.versioning.dvc_ops --init
    py -3.13 -m src.versioning.dvc_ops --track data/raw
"""

import json
import subprocess
import argparse
import logging
from pathlib import Path
from datetime import datetime

from src.config import PROJECT_ROOT, LOGS_DIR, ensure_dir

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(ensure_dir(LOGS_DIR) / "versioning.log"),
                              logging.StreamHandler()])
log = logging.getLogger(__name__)


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd or PROJECT_ROOT))
    if result.returncode != 0:
        log.warning("Command failed: %s\n%s", " ".join(cmd), result.stderr)
    return result.stdout.strip()


def init_dvc():
    """Initialize DVC in the project if not already initialized."""
    dvc_dir = PROJECT_ROOT / ".dvc"
    if dvc_dir.exists():
        log.info("DVC already initialized")
        return
    _run(["dvc", "init"])
    log.info("DVC initialized at %s", PROJECT_ROOT)


def track(data_path: str | Path):
    """Track a file or directory with DVC."""
    data_path = Path(data_path)
    if not data_path.exists():
        log.warning("Path does not exist: %s", data_path)
        return
    log.info("Tracking with DVC: %s", data_path)
    _run(["dvc", "add", str(data_path)])
    dvc_file = str(data_path) + ".dvc"
    _run(["git", "add", dvc_file, ".gitignore"])
    log.info("DVC tracking added for %s", data_path)


def create_lineage(data_path: str | Path, source: str, transformations: list[str]):
    """Create a lineage metadata JSON sidecar for a data file/directory."""
    data_path = Path(data_path)
    meta = {
        "file": str(data_path),
        "source": source,
        "transformations": transformations,
        "created_at": datetime.now().isoformat(),
    }
    if data_path.is_file():
        meta["size_bytes"] = data_path.stat().st_size
    elif data_path.is_dir():
        meta["file_count"] = sum(1 for _ in data_path.rglob("*") if _.is_file())

    lineage_path = data_path.parent / f"{data_path.name}.lineage.json"
    lineage_path.write_text(json.dumps(meta, indent=2))
    log.info("Lineage metadata written to %s", lineage_path)
    return str(lineage_path)


def track_all():
    """Track all data directories with DVC."""
    init_dvc()
    for subdir in ["data/raw", "data/prepared", "data/transformed", "data/splits"]:
        path = PROJECT_ROOT / subdir
        if path.exists() and any(path.iterdir()):
            track(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DVC data versioning")
    parser.add_argument("--init", action="store_true", help="Initialize DVC")
    parser.add_argument("--track", type=str, default=None, help="Track a path")
    parser.add_argument("--track-all", action="store_true", help="Track all data dirs")
    args = parser.parse_args()

    if args.init:
        init_dvc()
    if args.track:
        track(args.track)
    if args.track_all:
        track_all()
