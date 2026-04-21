# RecoMart - End-to-End Data Management Pipeline for Recommendation System

DM4ML Assignment I - End-to-end data management pipeline for a recommendation system.

## Team

| Member   | Stories                  |
|----------|--------------------------|
| Pranav   | REC-1, REC-5, REC-7, REC-15 |
| Dheeraj  | REC-2, REC-6, REC-9, REC-10 |
| Aniketh  | REC-3, REC-11, REC-13, REC-14 |
| Naaz     | REC-4, REC-8, REC-12, REC-16 |

## Project Structure

```
recomart_pipeline/
  docs/                  # Contracts, protocols, specifications
  data/                  # Raw, prepared, transformed data (tracked via DVC)
  src/                   # Pipeline source code
  notebooks/             # EDA and experimentation
  mlruns/                # MLflow tracking
  README.md
```

## Contracts (Phase 1)

- [Modelling Protocol & Inference Contract](docs/rec-4-modelling-protocol.md)

## Infrastructure (Phase 2)

- [MLflow Setup & Logging Guide](docs/rec-8-mlflow-setup-guide.md)

### MLflow Quick Start

```bash
pip install mlflow
cd recomart_pipeline
python -m src.tracking.verify_mlflow_setup   # verify setup
mlflow ui --backend-store-uri mlruns          # browse experiments
```
