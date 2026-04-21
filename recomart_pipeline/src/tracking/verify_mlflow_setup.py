"""
REC-8 Verification: Dummy experiment to confirm MLflow tracking works.

Run this script after installing MLflow to verify the setup:
    cd recomart_pipeline
    python -m src.tracking.verify_mlflow_setup

Expected outcome:
    - A new run appears under the 'recomart-recommendation' experiment
    - Parameters, metrics, and artifacts are logged correctly
    - Console prints the run ID and artifact URI for confirmation

After running, you can view results with:
    mlflow ui --backend-store-uri mlruns
    # Then open http://127.0.0.1:5000
"""

import json
import csv
import tempfile
from pathlib import Path

from src.tracking.mlflow_config import init_tracking, log_recommendation_run


def main():
    print("=" * 60)
    print("REC-8: MLflow Setup Verification")
    print("=" * 60)

    # Step 1: Initialize tracking
    print("\n[1/4] Initializing MLflow tracking...")
    exp_id = init_tracking()
    print(f"  Experiment ID: {exp_id}")
    print(f"  Experiment name: recomart-recommendation")

    # Step 2: Prepare dummy params (matching REC-4 contract)
    dummy_params = {
        "model_type": "svd_dummy",
        "n_factors": 50,
        "n_epochs": 10,
        "lr_all": 0.005,
        "reg_all": 0.02,
        "k_values": "5,10",
        "split_method": "temporal",
        "relevance_threshold": 3.5,
        "min_user_interactions": 5,
        "train_size": 1000,
        "test_size": 200,
    }

    # Step 3: Prepare dummy metrics
    dummy_metrics = {
        "precision_at_5": 0.32,
        "precision_at_10": 0.28,
        "recall_at_5": 0.15,
        "recall_at_10": 0.22,
        "ndcg_at_5": 0.35,
        "ndcg_at_10": 0.31,
        "rmse": 0.92,
        "num_users_evaluated": 150,
    }

    # Step 4: Prepare dummy artifacts
    dummy_eval_report = {
        "model_type": "svd_dummy",
        "metrics": dummy_metrics,
        "note": "This is a dummy verification run for REC-8.",
    }

    # Create a temporary top_k_sample CSV
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "item_id", "predicted_score", "rank"])
        for i in range(5):
            writer.writerow([42, 100 + i, round(4.5 - i * 0.1, 2), i + 1])
        sample_path = f.name

    # Step 5: Log the run
    print("\n[2/4] Logging dummy run...")
    log_recommendation_run(
        params=dummy_params,
        metrics=dummy_metrics,
        evaluation_report=dummy_eval_report,
        top_k_sample_path=sample_path,
    )

    # Clean up temp file
    Path(sample_path).unlink(missing_ok=True)

    print("  Run logged successfully.")

    # Step 6: Verify by reading back
    print("\n[3/4] Verifying logged data...")
    import mlflow

    runs = mlflow.search_runs(experiment_ids=[exp_id])
    if len(runs) == 0:
        print("  ERROR: No runs found!")
        return

    latest = runs.iloc[0]
    run_id = latest["run_id"]
    print(f"  Run ID: {run_id}")
    print(f"  Run name: {latest.get('tags.mlflow.runName', 'N/A')}")
    print(f"  precision_at_5: {latest.get('metrics.precision_at_5', 'MISSING')}")
    print(f"  ndcg_at_10: {latest.get('metrics.ndcg_at_10', 'MISSING')}")
    print(f"  model_type: {latest.get('params.model_type', 'MISSING')}")

    print("\n[4/4] Verification complete.")
    print(f"  Artifact URI: {latest.get('artifact_uri', 'N/A')}")
    print("\nTo view in the MLflow UI, run:")
    print("  mlflow ui --backend-store-uri mlruns")
    print("  Then open http://127.0.0.1:5000")
    print("=" * 60)


if __name__ == "__main__":
    main()
