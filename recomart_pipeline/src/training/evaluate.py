"""Task 9: Evaluation metrics — Precision@K, Recall@K, NDCG@K, RMSE."""

import numpy as np
import pandas as pd


def precision_at_k(recommended: list, relevant: set, k: int) -> float:
    """Precision@K for a single user."""
    top_k = recommended[:k]
    hits = sum(1 for item in top_k if item in relevant)
    return hits / k if k > 0 else 0.0


def recall_at_k(recommended: list, relevant: set, k: int) -> float:
    """Recall@K for a single user."""
    top_k = recommended[:k]
    hits = sum(1 for item in top_k if item in relevant)
    return hits / len(relevant) if len(relevant) > 0 else 0.0


def ndcg_at_k(recommended: list, relevant: set, k: int) -> float:
    """NDCG@K for a single user (binary relevance)."""
    top_k = recommended[:k]
    dcg = sum((1.0 / np.log2(i + 2)) for i, item in enumerate(top_k) if item in relevant)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / np.log2(i + 2) for i in range(ideal_hits))
    return dcg / idcg if idcg > 0 else 0.0


def rmse(predictions: list[tuple[float, float]]) -> float:
    """RMSE over (predicted, actual) pairs."""
    if not predictions:
        return 0.0
    errors = [(p - a) ** 2 for p, a in predictions]
    return np.sqrt(np.mean(errors))


def evaluate_model(recommend_fn, test_df: pd.DataFrame, train_df: pd.DataFrame,
                   k_values: list[int] = None, relevance_threshold: float = 2) -> dict:
    """Full evaluation across all test users.

    Args:
        recommend_fn: Callable(user_id, k) -> list of item_ids
        test_df: Test interactions DataFrame with user_id, item_id, rating columns
        train_df: Train interactions DataFrame
        k_values: List of K values (default [5, 10])
        relevance_threshold: Rating threshold for binary relevance

    Returns:
        Dict of aggregated metrics matching MLflow logging format.
    """
    if k_values is None:
        k_values = [5, 10]

    max_k = max(k_values)

    # Build per-user relevant items from test set
    test_relevant = (
        test_df[test_df["rating"] >= relevance_threshold]
        .groupby("user_id")["item_id"]
        .apply(set)
        .to_dict()
    )

    # Only evaluate users with relevant items in test
    eval_users = [u for u, items in test_relevant.items() if len(items) > 0]

    metrics = {f"precision_at_{k}": [] for k in k_values}
    metrics.update({f"recall_at_{k}": [] for k in k_values})
    metrics.update({f"ndcg_at_{k}": [] for k in k_values})

    for user_id in eval_users:
        recs = recommend_fn(user_id, max_k)
        relevant = test_relevant[user_id]

        for k in k_values:
            metrics[f"precision_at_{k}"].append(precision_at_k(recs, relevant, k))
            metrics[f"recall_at_{k}"].append(recall_at_k(recs, relevant, k))
            metrics[f"ndcg_at_{k}"].append(ndcg_at_k(recs, relevant, k))

    # Aggregate
    result = {}
    for key, values in metrics.items():
        result[key] = round(float(np.mean(values)), 6) if values else 0.0

    result["num_users_evaluated"] = len(eval_users)
    return result
