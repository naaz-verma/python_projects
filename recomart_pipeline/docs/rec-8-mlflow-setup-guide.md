# REC-8: MLflow Tracking Setup and Experiment Metadata Conventions

**Story Owner:** Naaz
**Story Points:** 2
**Assignment Coverage:** Task 9
**Status:** Complete (pending MLflow install & verification run)

---

## 1. Overview

This document describes how MLflow is set up for the RecoMart project and how all training scripts must log their runs. The conventions here implement the contract defined in [REC-4 Section 5](rec-4-modelling-protocol.md#5-mlflow-logging-convention).

---

## 2. Installation

```bash
pip install mlflow
```

After installing, verify the setup by running the dummy experiment:

```bash
cd recomart_pipeline
python -m src.tracking.verify_mlflow_setup
```

To open the MLflow UI and browse experiments:

```bash
mlflow ui --backend-store-uri mlruns
# Open http://127.0.0.1:5000
```

---

## 3. Project Configuration

| Setting          | Value                            |
|------------------|----------------------------------|
| Tracking URI     | `mlruns/` (local filesystem)     |
| Experiment name  | `recomart-recommendation`        |
| Run naming       | `{model_type}_{YYYYMMDD_HHMMSS}` |

All tracking data lives inside `recomart_pipeline/mlruns/`. No remote server is needed for this assignment.

---

## 4. Artifact Directory Structure

Each MLflow run stores artifacts in three subdirectories:

```
mlruns/
  <experiment_id>/
    <run_id>/
      artifacts/
        model/
          model.pkl            # Serialized trained model
        reports/
          evaluation_report.json   # Full metric breakdown
          training_config.json     # Snapshot of all hyperparameters
        samples/
          top_k_sample.csv     # Top-K recommendations for 10 sample users
```

---

## 5. How Training Scripts Should Log Runs

### 5.1 Quick Start (Recommended)

Use the helper function in `src/tracking/mlflow_config.py`. This handles initialization, validation, and artifact logging in one call:

```python
from src.tracking.mlflow_config import init_tracking, log_recommendation_run

# Initialize once at the start of your script
init_tracking()

# After training and evaluation, log everything
log_recommendation_run(
    params={
        "model_type": "svd",
        "n_factors": 100,
        "n_epochs": 20,
        "lr_all": 0.005,
        "reg_all": 0.02,
        "k_values": "5,10",
        "split_method": "temporal",
        "relevance_threshold": 3.5,
        "min_user_interactions": 5,
        "train_size": 50000,
        "test_size": 10000,
    },
    metrics={
        "precision_at_5": 0.35,
        "precision_at_10": 0.29,
        "recall_at_5": 0.18,
        "recall_at_10": 0.25,
        "ndcg_at_5": 0.38,
        "ndcg_at_10": 0.33,
        "rmse": 0.88,
        "num_users_evaluated": 500,
    },
    model_artifact_path="path/to/model.pkl",
    evaluation_report={"metrics": {...}, "per_user": [...]},
    top_k_sample_path="path/to/top_k_sample.csv",
)
```

The helper will:
- Validate that all required params and metrics are present (raises `ValueError` if not)
- Generate a run name automatically
- Log params, metrics, and artifacts into the correct subdirectories
- Save a `training_config.json` snapshot alongside the evaluation report

### 5.2 Manual Logging (Alternative)

If you need more control, use MLflow directly:

```python
import mlflow
from src.tracking.mlflow_config import init_tracking, make_run_name

init_tracking()

with mlflow.start_run(run_name=make_run_name("svd")):
    mlflow.log_params({...})
    mlflow.log_metrics({...})
    mlflow.log_artifact("model.pkl", artifact_path="model")
    mlflow.log_artifact("report.json", artifact_path="reports")
    mlflow.log_artifact("sample.csv", artifact_path="samples")
```

---

## 6. Required Parameters

All training runs **must** log these parameters (enforced by `log_recommendation_run`):

| Parameter              | Type  | Example          |
|------------------------|-------|------------------|
| model_type             | str   | "svd"            |
| n_factors              | int   | 100              |
| n_epochs               | int   | 20               |
| lr_all                 | float | 0.005            |
| reg_all                | float | 0.02             |
| k_values               | str   | "5,10"           |
| split_method           | str   | "temporal"       |
| relevance_threshold    | float | 3.5              |
| min_user_interactions  | int   | 5                |
| train_size             | int   | 50000            |
| test_size              | int   | 10000            |

---

## 7. Required Metrics

All training runs **must** log these metrics:

| Metric              | Type  | Description                        |
|---------------------|-------|------------------------------------|
| precision_at_5      | float | Precision@5 averaged across users  |
| precision_at_10     | float | Precision@10 averaged across users |
| recall_at_5         | float | Recall@5 averaged across users     |
| recall_at_10        | float | Recall@10 averaged across users    |
| ndcg_at_5           | float | NDCG@5 averaged across users       |
| ndcg_at_10          | float | NDCG@10 averaged across users      |
| rmse                | float | RMSE on test set ratings           |
| num_users_evaluated | int   | Users included in metric average   |

---

## 8. Verification Checklist

After installing MLflow, confirm the setup by running:

```bash
python -m src.tracking.verify_mlflow_setup
```

You should see:
- [x] Experiment `recomart-recommendation` created
- [x] A dummy run logged with all params and metrics
- [x] Artifacts stored in `model/`, `reports/`, `samples/` subdirectories
- [x] Run visible in `mlflow ui`

Take a screenshot of the MLflow UI showing the dummy run for submission evidence.

---

## Revision History

| Date       | Author | Change                              |
|------------|--------|-------------------------------------|
| 2026-04-21 | Naaz   | Initial setup - pending MLflow install |
