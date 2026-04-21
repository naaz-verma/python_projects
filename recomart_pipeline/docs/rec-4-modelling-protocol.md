# REC-4: Modelling Protocol, Evaluation Plan, and Inference Contract

**Story Owner:** Naaz
**Story Points:** 2
**Assignment Coverage:** Task 1, Task 9
**Status:** Phase 1 - Contract Lock

---

## 1. Model Strategy

### 1.1 Primary Model: Collaborative Filtering (SVD / Matrix Factorization)

**Algorithm:** Singular Value Decomposition (SVD) via the `surprise` library.

**Rationale:**
- The assignment mandates at least one recommendation model; collaborative filtering is the most established approach for user-item interaction data.
- SVD handles explicit ratings naturally and scales well for the RecoMart dataset size.
- The `surprise` library provides a clean API for training, cross-validation, and prediction, reducing implementation overhead.

**Key hyperparameters (defaults, tunable):**

| Parameter   | Default | Description                          |
|-------------|---------|--------------------------------------|
| n_factors   | 100     | Number of latent factors             |
| n_epochs    | 20      | Number of SGD iterations             |
| lr_all      | 0.005   | Learning rate for all parameters     |
| reg_all     | 0.02    | Regularization term for all parameters |

### 1.2 Optional Stretch: Content-Based Filtering

If time permits after the primary model is complete:
- Use item metadata features (category, brand, price range) to compute item similarity using TF-IDF + cosine similarity.
- Hybrid approach: blend CF scores with content-based scores using a weighted average.

**This is not mandatory for submission.** The team should focus on delivering a solid CF baseline first.

---

## 2. Train / Validation / Test Split Logic

### 2.1 Recommended Approach: Temporal Split

Since recommendation systems operate on time-ordered interactions, a temporal split is the most realistic evaluation strategy.

**Procedure:**
1. Sort all user-item interactions by timestamp (ascending).
2. Split by time cutoff:
   - **Train:** First 70% of interactions (by time)
   - **Validation:** Next 15% of interactions
   - **Test:** Final 15% of interactions

**Advantages:**
- Simulates real-world deployment where the model trains on past data and predicts future interactions.
- Prevents data leakage from future interactions into training.

### 2.2 Fallback Approach: Random Stratified Split

If timestamps are unavailable or unreliable in the dataset:
1. For each user, randomly split their interactions into 70/15/15.
2. Ensures every user with sufficient interactions appears in all three sets.

**Minimum interaction threshold:** Users with fewer than 5 interactions are excluded from evaluation (kept in training only).

### 2.3 Decision

Use **temporal split** as the primary method. Document which method was used in every MLflow run via the `split_method` parameter.

---

## 3. Model Input / Output Contract

### 3.1 Training Input Format

The model expects a user-item interaction dataset with the following schema:

| Column          | Type    | Description                              | Required |
|-----------------|---------|------------------------------------------|----------|
| user_id         | int/str | Unique user identifier                   | Yes      |
| item_id         | int/str | Unique item identifier                   | Yes      |
| rating          | float   | Explicit rating (1.0 - 5.0) or implicit score | Yes |
| timestamp       | int     | Unix timestamp of the interaction        | Yes      |

**Source:** This data comes from the prepared/cleaned dataset produced by REC-10 (Dheeraj).

**Format:** CSV file or pandas DataFrame with the columns above. No nulls allowed in any column.

### 3.2 Inference Contract

```python
def recommend(user_id: int, k: int = 10) -> list[tuple[int, float]]:
    """
    Generate top-K item recommendations for a given user.

    Args:
        user_id: The unique identifier of the user.
        k: Number of recommendations to return (default: 10).

    Returns:
        A list of (item_id, predicted_score) tuples, sorted by
        predicted_score descending. Length is exactly k.

    Raises:
        ValueError: If k < 1.

    Cold-start handling:
        If user_id is not found in the training data, returns the
        top-K most popular items (by interaction count) as fallback.
    """
```

**Output example:**
```python
recommend(user_id=42, k=5)
# Returns:
[
    (1023, 4.82),
    (587,  4.71),
    (2901, 4.65),
    (412,  4.59),
    (1456, 4.51)
]
```

**Contract rules:**
- Items the user has already interacted with in the training set are excluded from recommendations.
- Scores are predicted ratings on the original scale (1.0 - 5.0 for explicit feedback).
- The function must be deterministic for the same model state and inputs.

---

## 4. Evaluation Metrics

All metrics are computed on the **test set** only. The validation set is used for hyperparameter tuning.

### 4.1 Precision@K

**Definition:** Of the top-K recommended items, what fraction are relevant (actually interacted with by the user in the test set)?

```
Precision@K = |{recommended items in top-K} intersection {relevant items}| / K
```

**Computed for:** K = 5, K = 10

### 4.2 Recall@K

**Definition:** Of all relevant items in the test set, what fraction appear in the top-K recommendations?

```
Recall@K = |{recommended items in top-K} intersection {relevant items}| / |{relevant items}|
```

**Computed for:** K = 5, K = 10

### 4.3 NDCG@K (Normalized Discounted Cumulative Gain)

**Definition:** Measures ranking quality, giving higher weight to relevant items appearing at the top of the recommendation list.

```
DCG@K  = sum_{i=1}^{K} rel_i / log2(i + 1)
IDCG@K = DCG@K for the ideal (perfect) ranking
NDCG@K = DCG@K / IDCG@K
```

Where `rel_i` = 1 if the item at position i is relevant, 0 otherwise (binary relevance).

**Computed for:** K = 5, K = 10

### 4.4 RMSE (Root Mean Squared Error)

**Definition:** Measures prediction accuracy on known ratings.

```
RMSE = sqrt(mean((predicted_rating - actual_rating)^2))
```

Used as a secondary metric for model diagnostics, not as the primary ranking metric.

### 4.5 Relevance Threshold

An item is considered **relevant** if the user's actual rating >= 3.5 (on a 1-5 scale). For implicit feedback datasets, any interaction counts as relevant.

### 4.6 Aggregation

All metrics are computed **per user** on the test set, then **averaged across all users** (macro-average). Users with no test interactions are excluded from the average.

---

## 5. MLflow Logging Convention

This section defines the exact fields that training scripts (REC-12) must log in MLflow. The MLflow setup (REC-8) will configure the tracking server and folder structure to support this contract.

### 5.1 Experiment Name

```
recomart-recommendation
```

### 5.2 Run Naming Convention

```
{model_type}_{YYYYMMDD_HHMMSS}
```

Example: `svd_20260421_143022`

### 5.3 Parameters to Log

| Parameter      | Type   | Example          | Description                          |
|----------------|--------|------------------|--------------------------------------|
| model_type     | str    | "svd"            | Algorithm identifier                 |
| n_factors      | int    | 100              | Number of latent factors             |
| n_epochs       | int    | 20               | Training iterations                  |
| lr_all         | float  | 0.005            | Learning rate                        |
| reg_all        | float  | 0.02             | Regularization strength              |
| k_values       | str    | "5,10"           | K values used for evaluation         |
| split_method   | str    | "temporal"       | Train/test split method used         |
| relevance_threshold | float | 3.5          | Rating threshold for binary relevance |
| min_user_interactions | int | 5            | Minimum interactions per user        |
| train_size     | int    | 50000            | Number of training interactions      |
| test_size      | int    | 10000            | Number of test interactions          |

### 5.4 Metrics to Log

| Metric          | Type  | Description                       |
|-----------------|-------|-----------------------------------|
| precision_at_5  | float | Precision@5 averaged across users |
| precision_at_10 | float | Precision@10 averaged across users |
| recall_at_5     | float | Recall@5 averaged across users    |
| recall_at_10    | float | Recall@10 averaged across users   |
| ndcg_at_5       | float | NDCG@5 averaged across users      |
| ndcg_at_10      | float | NDCG@10 averaged across users     |
| rmse            | float | RMSE on test set ratings          |
| num_users_evaluated | int | Users included in metric avg   |

### 5.5 Artifacts to Log

| Artifact                | Format | Description                                      |
|-------------------------|--------|--------------------------------------------------|
| model.pkl               | pickle | Serialized trained model                         |
| evaluation_report.json  | JSON   | Full metric breakdown (per-K and aggregate)      |
| top_k_sample.csv        | CSV    | Sample recommendations for 10 random test users  |
| training_config.json    | JSON   | Full training configuration snapshot             |

### 5.6 Artifact Directory Structure

```
mlruns/
  <experiment_id>/
    <run_id>/
      artifacts/
        model/
          model.pkl
        reports/
          evaluation_report.json
          training_config.json
        samples/
          top_k_sample.csv
```

---

## 6. Interface Dependencies

This contract is consumed by the following downstream stories:

| Story  | What it uses from this contract                                |
|--------|---------------------------------------------------------------|
| REC-8  | MLflow experiment name, run naming, param/metric/artifact specs |
| REC-12 | Model strategy, input format, inference contract, eval metrics, MLflow logging fields |
| REC-16 | Evaluation metrics definitions for final report                |

---

## Revision History

| Date       | Author | Change                          |
|------------|--------|---------------------------------|
| 2026-04-21 | Naaz   | Initial contract - Phase 1 lock |
