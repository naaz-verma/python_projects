"""
MLflow configuration and helper utilities for RecoMart.

Centralizes all MLflow setup so that training scripts (REC-12) only need to:
    from src.tracking.mlflow_config import init_tracking, log_recommendation_run
"""

import os
import json
from pathlib import Path
from datetime import datetime

import mlflow

# ---------------------------------------------------------------------------
# Constants (aligned with REC-4 modelling protocol, section 5)
# ---------------------------------------------------------------------------
EXPERIMENT_NAME = "recomart-recommendation"
TRACKING_URI = str(Path(__file__).resolve().parents[2] / "mlruns")

ARTIFACT_SUBDIRS = {
    "model": "model",
    "reports": "reports",
    "samples": "samples",
}

REQUIRED_PARAMS = [
    "model_type", "n_factors", "n_epochs", "lr_all", "reg_all",
    "k_values", "split_method", "relevance_threshold",
    "min_user_interactions", "train_size", "test_size",
]

REQUIRED_METRICS = [
    "precision_at_5", "precision_at_10",
    "recall_at_5", "recall_at_10",
    "ndcg_at_5", "ndcg_at_10",
    "rmse", "num_users_evaluated",
]


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
def init_tracking() -> str:
    """Initialize MLflow tracking and return the experiment ID.

    - Sets the tracking URI to a local ``mlruns/`` directory inside the project.
    - Creates the experiment if it does not exist.

    Returns:
        The experiment ID as a string.
    """
    mlflow.set_tracking_uri(f"file:///{TRACKING_URI}")
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        exp_id = mlflow.create_experiment(EXPERIMENT_NAME)
    else:
        exp_id = experiment.experiment_id
    mlflow.set_experiment(EXPERIMENT_NAME)
    return exp_id


def make_run_name(model_type: str) -> str:
    """Generate a run name following the convention: {model_type}_{YYYYMMDD_HHMMSS}."""
    return f"{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------
def log_recommendation_run(
    params: dict,
    metrics: dict,
    model_artifact_path: str | None = None,
    evaluation_report: dict | None = None,
    top_k_sample_path: str | None = None,
):
    """Log a complete recommendation training run to MLflow.

    This is the main entry point that REC-12 training scripts should call.
    It validates that all required fields from the REC-4 contract are present,
    then logs params, metrics, and artifacts in one shot.

    Args:
        params: Dictionary of hyperparameters (must contain all REQUIRED_PARAMS).
        metrics: Dictionary of evaluation metrics (must contain all REQUIRED_METRICS).
        model_artifact_path: Local path to the serialized model file.
        evaluation_report: Dictionary that will be saved as evaluation_report.json.
        top_k_sample_path: Local path to top_k_sample.csv file.

    Raises:
        ValueError: If required params or metrics are missing.
    """
    missing_params = [p for p in REQUIRED_PARAMS if p not in params]
    if missing_params:
        raise ValueError(f"Missing required params: {missing_params}")

    missing_metrics = [m for m in REQUIRED_METRICS if m not in metrics]
    if missing_metrics:
        raise ValueError(f"Missing required metrics: {missing_metrics}")

    run_name = make_run_name(params["model_type"])

    with mlflow.start_run(run_name=run_name):
        # Log parameters
        mlflow.log_params(params)

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log artifacts
        if model_artifact_path:
            mlflow.log_artifact(model_artifact_path, artifact_path=ARTIFACT_SUBDIRS["model"])

        if evaluation_report is not None:
            report_dir = Path(TRACKING_URI).parent / "tmp_artifacts"
            report_dir.mkdir(exist_ok=True)
            report_file = report_dir / "evaluation_report.json"
            report_file.write_text(json.dumps(evaluation_report, indent=2))
            mlflow.log_artifact(str(report_file), artifact_path=ARTIFACT_SUBDIRS["reports"])
            report_file.unlink()

            # Also log training config snapshot
            config_file = report_dir / "training_config.json"
            config_file.write_text(json.dumps(params, indent=2))
            mlflow.log_artifact(str(config_file), artifact_path=ARTIFACT_SUBDIRS["reports"])
            config_file.unlink()

            report_dir.rmdir()

        if top_k_sample_path:
            mlflow.log_artifact(top_k_sample_path, artifact_path=ARTIFACT_SUBDIRS["samples"])
