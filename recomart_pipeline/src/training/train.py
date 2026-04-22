"""Task 9: SVD model training, evaluation, and MLflow logging.

Implements SVD via scipy for collaborative filtering with pseudo-ratings.

Usage:
    py -3.13 -m src.training.train
"""

import json
import pickle
import logging
import argparse
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

import mlflow

from src.config import (
    SPLITS_DIR, MLRUNS_DIR, REPORTS_DIR, EXPERIMENT_NAME,
    SVD_DEFAULTS, K_VALUES, RELEVANCE_THRESHOLD, RATING_SCALE,
    ensure_dir, LOGS_DIR,
)
from src.training.evaluate import evaluate_model, rmse

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(ensure_dir(LOGS_DIR) / "training.log"),
                              logging.StreamHandler()])
log = logging.getLogger(__name__)


class SVDRecommender:
    """SVD-based collaborative filtering recommender."""

    def __init__(self, n_factors: int = 100):
        self.n_factors = n_factors
        self.user_factors = None
        self.item_factors = None
        self.sigma = None
        self.user_id_map = None  # user_id -> matrix_index
        self.item_id_map = None  # item_id -> matrix_index
        self.reverse_item_map = None  # matrix_index -> item_id
        self.global_mean = 0.0
        self.popular_items = []

    def fit(self, train_df: pd.DataFrame):
        """Train SVD model from interactions DataFrame."""
        log.info("Training SVD with n_factors=%d on %d interactions...", self.n_factors, len(train_df))

        # Build mappings
        users = train_df["user_id"].unique()
        items = train_df["item_id"].unique()
        self.user_id_map = {uid: idx for idx, uid in enumerate(users)}
        self.item_id_map = {iid: idx for idx, iid in enumerate(items)}
        self.reverse_item_map = {idx: iid for iid, idx in self.item_id_map.items()}

        # Build sparse matrix
        rows = train_df["user_id"].map(self.user_id_map).values
        cols = train_df["item_id"].map(self.item_id_map).values
        vals = train_df["rating"].values.astype(float)

        self.global_mean = vals.mean()
        matrix = csr_matrix((vals - self.global_mean, (rows, cols)),
                            shape=(len(users), len(items)))

        # SVD decomposition
        k = min(self.n_factors, min(matrix.shape) - 1)
        U, sigma, Vt = svds(matrix, k=k)
        self.user_factors = U
        self.sigma = sigma
        self.item_factors = Vt.T  # items x factors

        # Popular items fallback
        item_counts = train_df["item_id"].value_counts()
        self.popular_items = item_counts.head(50).index.tolist()

        log.info("SVD training complete. Matrix: %s, factors: %d", matrix.shape, k)

    def predict(self, user_id, item_id) -> float:
        """Predict rating for a user-item pair."""
        if user_id not in self.user_id_map or item_id not in self.item_id_map:
            return self.global_mean
        u_idx = self.user_id_map[user_id]
        i_idx = self.item_id_map[item_id]
        score = self.global_mean + np.dot(
            self.user_factors[u_idx] * self.sigma,
            self.item_factors[i_idx]
        )
        return float(np.clip(score, RATING_SCALE[0], RATING_SCALE[1]))

    def recommend(self, user_id: int, k: int = 10, exclude_known: set | None = None) -> list[int]:
        """Generate top-K item recommendations for a user.

        Returns list of item_ids sorted by predicted score descending.
        Cold-start users get popular items.
        """
        if user_id not in self.user_id_map:
            # Cold start fallback
            items = [i for i in self.popular_items if exclude_known is None or i not in exclude_known]
            return items[:k]

        u_idx = self.user_id_map[user_id]
        scores = self.global_mean + np.dot(
            self.user_factors[u_idx] * self.sigma,
            self.item_factors.T
        )

        # Get top items
        item_scores = []
        for i_idx in range(len(scores)):
            iid = self.reverse_item_map[i_idx]
            if exclude_known and iid in exclude_known:
                continue
            item_scores.append((iid, scores[i_idx]))

        item_scores.sort(key=lambda x: x[1], reverse=True)
        return [iid for iid, _ in item_scores[:k]]

    def save(self, path: str | Path):
        with open(path, "wb") as f:
            pickle.dump(self, f)
        log.info("Model saved to %s", path)

    @staticmethod
    def load(path: str | Path) -> "SVDRecommender":
        with open(path, "rb") as f:
            return pickle.load(f)


def run_training(splits_dir: str | Path | None = None, hyperparams: dict | None = None) -> dict:
    """Full training pipeline: load splits, train, evaluate, log to MLflow."""
    splits_dir = Path(splits_dir or SPLITS_DIR)
    hp = {**SVD_DEFAULTS, **(hyperparams or {})}

    # Load splits
    train_df = pd.read_csv(splits_dir / "train.csv")
    test_df = pd.read_csv(splits_dir / "test.csv")
    log.info("Loaded train=%d, test=%d", len(train_df), len(test_df))

    # Train
    model = SVDRecommender(n_factors=hp["n_factors"])
    model.fit(train_df)

    # Build known items per user (for excluding from recommendations)
    known_items = train_df.groupby("user_id")["item_id"].apply(set).to_dict()

    # Evaluate
    def recommend_fn(user_id, k):
        return model.recommend(user_id, k, exclude_known=known_items.get(user_id, set()))

    metrics = evaluate_model(recommend_fn, test_df, train_df, K_VALUES, RELEVANCE_THRESHOLD)

    # RMSE on test predictions
    predictions = []
    for _, row in test_df.sample(min(10000, len(test_df)), random_state=42).iterrows():
        pred = model.predict(row["user_id"], row["item_id"])
        predictions.append((pred, row["rating"]))
    metrics["rmse"] = round(rmse(predictions), 6)

    log.info("Metrics: %s", metrics)

    # Save model artifact
    model_dir = ensure_dir(REPORTS_DIR.parent / "artifacts")
    model_path = model_dir / "model.pkl"
    model.save(model_path)

    # Generate sample recommendations
    sample_users = test_df["user_id"].drop_duplicates().head(10).tolist()
    sample_rows = []
    for uid in sample_users:
        recs = recommend_fn(uid, 10)
        for rank, iid in enumerate(recs, 1):
            sample_rows.append({"user_id": uid, "item_id": iid, "rank": rank,
                                "predicted_score": round(model.predict(uid, iid), 3)})
    sample_df = pd.DataFrame(sample_rows)
    sample_path = model_dir / "top_k_sample.csv"
    sample_df.to_csv(sample_path, index=False)

    # Log to MLflow
    mlflow.set_tracking_uri(f"file:///{MLRUNS_DIR}")
    mlflow.set_experiment(EXPERIMENT_NAME)

    run_name = f"svd_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params({
            "model_type": "svd_scipy",
            "n_factors": hp["n_factors"],
            "n_epochs": hp.get("n_epochs", "N/A"),
            "lr": hp.get("lr", "N/A"),
            "reg": hp.get("reg", "N/A"),
            "k_values": ",".join(map(str, K_VALUES)),
            "split_method": "temporal",
            "relevance_threshold": RELEVANCE_THRESHOLD,
            "min_user_interactions": 5,
            "train_size": len(train_df),
            "test_size": len(test_df),
        })
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(str(model_path), artifact_path="model")
        mlflow.log_artifact(str(sample_path), artifact_path="samples")

        # Log evaluation report
        report = {"run_name": run_name, "metrics": metrics, "hyperparams": hp}
        report_path = model_dir / "evaluation_report.json"
        report_path.write_text(json.dumps(report, indent=2))
        mlflow.log_artifact(str(report_path), artifact_path="reports")

    log.info("MLflow run '%s' logged successfully", run_name)

    # Generate performance PDF
    _generate_performance_pdf(metrics, hp, run_name)

    return {"metrics": metrics, "model_path": str(model_path), "run_name": run_name}


def _generate_performance_pdf(metrics: dict, hp: dict, run_name: str):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "Model Performance Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Run: {run_name}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Hyperparameters", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for k, v in hp.items():
        pdf.cell(0, 7, f"  {k}: {v}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Evaluation Metrics", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(60, 8, "Metric", border=1)
    pdf.cell(40, 8, "Value", border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    for k, v in metrics.items():
        pdf.cell(60, 7, k, border=1)
        pdf.cell(40, 7, str(v), border=1)
        pdf.ln()

    out = ensure_dir(REPORTS_DIR) / "model_performance.pdf"
    pdf.output(str(out))
    log.info("Performance report saved to %s", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--splits-dir", type=str, default=None)
    parser.add_argument("--n-factors", type=int, default=100)
    args = parser.parse_args()

    result = run_training(args.splits_dir, {"n_factors": args.n_factors})
    print("Training result:", result)
