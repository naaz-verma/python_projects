# RecoMart — End-to-End Data Management Pipeline for ML

A complete data management pipeline for a product recommendation system, built on the **Retailrocket** e-commerce dataset.

**Assignment:** DM4ML (Data Management for Machine Learning) — Assignment I

---

## Project Structure

```
recomart_pipeline/
├── src/
│   ├── config.py                       # Central paths, constants, helpers
│   ├── api/server.py                   # Mock FastAPI for API ingestion
│   ├── ingestion/
│   │   ├── ingest_csv.py               # CSV file ingestion into data lake
│   │   └── ingest_api.py               # REST API ingestion with retry
│   ├── validation/
│   │   ├── validators.py               # Schema, null, range, duplicate checks
│   │   └── quality_report.py           # PDF data quality report
│   ├── preparation/cleaner.py          # Dedup, pseudo-ratings, cold filtering
│   ├── transformation/
│   │   ├── features.py                 # User/item/co-occurrence features
│   │   └── sqlite_loader.py            # SQLite schema + load
│   ├── feature_store/store.py          # Versioned feature registry
│   ├── versioning/dvc_ops.py           # DVC tracking + lineage
│   ├── training/
│   │   ├── splitter.py                 # Temporal train/val/test split
│   │   ├── evaluate.py                 # Precision@K, Recall@K, NDCG@K, RMSE
│   │   └── train.py                    # SVD model + MLflow logging
│   ├── orchestration/pipeline.py       # Prefect DAG (full pipeline)
│   └── reports/problem_formulation.py  # Problem formulation PDF
├── notebooks/01_eda.ipynb              # Exploratory Data Analysis
├── data/                               # Date-partitioned data lake
├── db/features.db                      # SQLite feature database
├── feature_store/                      # JSON registry + versioned CSVs
├── mlruns/                             # MLflow experiment tracking
├── reports/                            # Generated PDF reports
├── logs/                               # Pipeline execution logs
└── requirements.txt
```

---

## Quick Start (Step-by-Step)

Follow these steps in order on a fresh machine.

### Step 1: Install dependencies

```bash
cd recomart_pipeline
pip install -r requirements.txt
```

> **Note (Windows):** If `python` defaults to 3.14+, use `py -3.13` instead of `python` in all commands below.

### Step 2: Download the dataset

**Option A** — Via kagglehub (requires Kaggle API credentials):
```bash
python -c "import kagglehub; print(kagglehub.dataset_download('retailrocket/ecommerce-dataset'))"
```
This prints the download path — use it as `<SOURCE>` in the commands below.

**Option B** — Manual download from [Kaggle](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset).
Extract the zip. The folder should contain: `events.csv`, `item_properties_part1.csv`, `item_properties_part2.csv`, `category_tree.csv`.

> **Corporate network?** kagglehub may fail with SSL errors behind a corporate proxy. Use manual download instead.

### Step 3: Ingest CSV files

```bash
python -m src.ingestion.ingest_csv --source <SOURCE>
```
This copies raw CSVs into `data/raw/csv/{type}/{date}/` with metadata.

### Step 4: Generate problem formulation PDF

```bash
python -m src.reports.problem_formulation
```
Output: `reports/problem_formulation.pdf`

### Step 5: Run the full pipeline (skip API first)

```bash
python -m src.orchestration.pipeline --source <SOURCE> --skip-api
```
This runs: validate → prepare → transform → SQLite + feature store → DVC versioning → split → train.

All logs go to `logs/pipeline.log`.

### Step 6: (Optional) Test API ingestion

Open **two terminals**:

```bash
# Terminal 1 — start mock API server
python -m src.api.server --data-dir <SOURCE>

# Terminal 2 — ingest from API
python -m src.ingestion.ingest_api
```
Then re-run the full pipeline without `--skip-api` if you want both ingestion types in one run.

### Step 7: Run the EDA notebook

```bash
jupyter notebook notebooks/01_eda.ipynb
```
Run all cells. This generates analysis plots saved to `reports/`.

### Step 8: Verify outputs

After the pipeline completes, you should have:

| Output | Location | Task |
|--------|----------|------|
| Problem formulation PDF | `reports/problem_formulation.pdf` | Task 1 |
| Data quality report PDF | `reports/data_quality_report.pdf` | Task 4 |
| Model performance PDF | `reports/model_performance.pdf` | Task 9 |
| SQLite feature database | `db/features.db` | Task 6 |
| Feature store registry | `feature_store/registry.json` | Task 7 |
| MLflow experiment data | `mlruns/` | Task 9 |
| Train/val/test splits | `data/splits/` | Task 9 |
| Pipeline logs | `logs/` | Task 10 |
| EDA plots | `reports/eda_*.png` | Task 5 |

### Step 9: Record demo video (5-10 min)

Walk through the pipeline execution and outputs for submission.

---

## Running Stages Individually

If you prefer to run each stage manually instead of the full pipeline:

```bash
# 1. Ingest CSV files
python -m src.ingestion.ingest_csv --source <SOURCE>

# 2. Start API server + ingest from API (two terminals)
python -m src.api.server --data-dir <SOURCE>
python -m src.ingestion.ingest_api

# 3. Validate raw data
python -m src.validation.validators --raw-dir data/raw/csv

# 4. Prepare data (clean, pseudo-ratings, cold filtering)
python -m src.preparation.cleaner --raw-dir data/raw/csv

# 5. Feature engineering
python -m src.transformation.features --prepared-dir data/prepared/<date>
python -m src.transformation.sqlite_loader --transformed-dir data/transformed/<date>

# 6. Feature store registration
python -m src.feature_store.store --transformed-dir data/transformed/<date>

# 7. DVC versioning
python -m src.versioning.dvc_ops --init
python -m src.versioning.dvc_ops --track-all

# 8. Split + Train
python -m src.training.splitter --interactions data/prepared/<date>/interactions.csv
python -m src.training.train
```

Replace `<date>` with today's date in `YYYY-MM-DD` format (e.g., `2026-04-22`).

---

## Dataset

**Retailrocket Recommender System Dataset** — real-world anonymised e-commerce data.

| File | Description | Rows |
|------|-------------|------|
| events.csv | User interactions (view, addtocart, transaction) | ~2.7M |
| item_properties_part1/2.csv | Item attribute snapshots | ~20M |
| category_tree.csv | Category hierarchy | ~1.7K |

### Pseudo-Rating Scheme

| Event | Rating | Meaning |
|-------|--------|---------|
| view | 1 | Weak interest |
| addtocart | 2 | Moderate interest |
| transaction | 3 | Strong interest |

---

## Pipeline Stages

| Stage | Task | Module |
|-------|------|--------|
| Ingestion | CSV + REST API ingestion | `src.ingestion` |
| Validation | Schema, null, range, duplicate checks | `src.validation` |
| Preparation | Dedup, pseudo-ratings, cold filtering | `src.preparation` |
| Feature Engineering | User/item/co-occurrence features + SQLite | `src.transformation` |
| Feature Store | Versioned CSV snapshots + JSON registry | `src.feature_store` |
| Data Versioning | DVC tracking + lineage metadata | `src.versioning` |
| Model Training | SVD (scipy) + MLflow logging | `src.training` |
| Orchestration | Prefect DAG | `src.orchestration` |

---

## Model

- **Algorithm:** SVD via `scipy.sparse.linalg.svds`
- **Latent factors:** 100
- **Evaluation:** Precision@K, Recall@K, NDCG@K (K=5,10), RMSE
- **Relevance threshold:** rating >= 2 (addtocart + transaction)
- **Cold-start:** Popular-item fallback for unseen users

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.13 |
| Data Processing | Pandas, NumPy, SciPy |
| Model | SVD (scipy.sparse.linalg.svds) |
| Experiment Tracking | MLflow |
| Orchestration | Prefect |
| Data Versioning | DVC |
| API Framework | FastAPI + Uvicorn |
| Database | SQLite |
| Reporting | fpdf2, Matplotlib, Seaborn |
