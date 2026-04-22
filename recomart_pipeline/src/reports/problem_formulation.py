"""Task 1: Generate Problem Formulation PDF report.

Usage:
    py -3.13 -m src.reports.problem_formulation
"""

from pathlib import Path
from fpdf import FPDF

from src.config import REPORTS_DIR, ensure_dir


def generate_problem_formulation(output_path: str | Path | None = None):
    """Generate the Problem Formulation & Data Requirements PDF."""
    output_path = Path(output_path or ensure_dir(REPORTS_DIR) / "problem_formulation.pdf")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- Title page ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.ln(40)
    pdf.cell(0, 15, "RecoMart", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 12, "Problem Formulation & Data Requirements", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "DM4ML Assignment I", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Data Management for Machine Learning", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 8, "Prepared by: Naaz Verma", align="C", new_x="LMARGIN", new_y="NEXT")

    # --- Section helper ---
    def section(title: str):
        pdf.ln(6)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)

    def para(text: str):
        pdf.multi_cell(0, 6, text)
        pdf.ln(2)

    def bullet(text: str):
        pdf.cell(8)
        pdf.multi_cell(0, 6, f"- {text}")

    # --- Page 2: Business Problem ---
    pdf.add_page()
    section("1. Business Problem")
    para(
        "RecoMart is a hypothetical e-commerce platform that aims to increase "
        "customer engagement and sales by providing personalised product "
        "recommendations. The core challenge is to build a recommendation "
        "system that can predict which products a user is most likely to "
        "interact with next, given their historical browsing and purchasing "
        "behaviour."
    )
    para(
        "The system must handle implicit feedback (clicks, add-to-cart, "
        "purchases) rather than explicit ratings, which introduces unique "
        "data management challenges including sparse interaction matrices, "
        "cold-start problems, and the need for pseudo-rating construction."
    )

    section("2. Data Sources")
    para("The pipeline ingests data from two source types to satisfy the "
         "multi-source ingestion requirement:")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Source 1: CSV Files (Batch Ingestion)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    bullet("events.csv: ~2.7M user-item interaction events (view, addtocart, transaction)")
    bullet("item_properties_part1.csv + part2.csv: ~20M item attribute snapshots")
    bullet("category_tree.csv: ~1.7K category hierarchy entries")
    para("")
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Source 2: REST API (Streaming Ingestion)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    bullet("Mock FastAPI server exposing item properties and category data")
    bullet("Paginated endpoints with JSON response format")
    bullet("Retry logic and error handling for API failures")

    section("3. Dataset Description")
    para(
        "Dataset: Retailrocket Recommender System Dataset (Kaggle). "
        "Contains real-world anonymised interaction data from a major "
        "e-commerce website over a 4.5-month period."
    )
    bullet("Events: timestamp, visitorid, event (view/addtocart/transaction), itemid, transactionid")
    bullet("Item Properties: timestamp, itemid, property, value (key-value pairs per snapshot)")
    bullet("Category Tree: categoryid, parentid (hierarchical category structure)")

    # --- Page 3: Methodology ---
    pdf.add_page()
    section("4. Data Pipeline Architecture")
    para("The end-to-end pipeline consists of the following stages:")
    bullet("Ingestion: CSV files + REST API with date-partitioned storage and metadata")
    bullet("Validation: Schema checks, null detection, value range validation, duplicate detection")
    bullet("Preparation: Event deduplication, pseudo-rating assignment, cold-start filtering")
    bullet("Feature Engineering: User features, item features, co-occurrence matrix")
    bullet("Feature Store: Versioned snapshots with JSON registry and SHA-256 hashing")
    bullet("Data Versioning: DVC tracking with lineage metadata")
    bullet("Model Training: SVD collaborative filtering with MLflow experiment tracking")
    bullet("Orchestration: Prefect DAG for end-to-end execution")

    section("5. Pseudo-Rating Scheme")
    para("Since the dataset contains implicit feedback, we construct pseudo-ratings "
         "to approximate user preference strength:")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 7, "Event Type", border=1)
    pdf.cell(30, 7, "Rating", border=1)
    pdf.cell(60, 7, "Interpretation", border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    for event, rating, interp in [
        ("view", "1", "Weak interest"),
        ("addtocart", "2", "Moderate interest"),
        ("transaction", "3", "Strong interest / purchase"),
    ]:
        pdf.cell(50, 7, event, border=1)
        pdf.cell(30, 7, rating, border=1)
        pdf.cell(60, 7, interp, border=1)
        pdf.ln()

    section("6. Model Approach")
    para(
        "The recommendation model uses Singular Value Decomposition (SVD) "
        "for collaborative filtering. SVD decomposes the user-item interaction "
        "matrix into latent factor matrices, enabling prediction of unobserved "
        "interactions."
    )
    bullet("Implementation: scipy.sparse.linalg.svds")
    bullet("Default factors: 100 latent dimensions")
    bullet("Mean-centred matrix to handle rating bias")
    bullet("Cold-start fallback: popular items for unseen users")

    section("7. Evaluation Metrics")
    para("Model quality is measured using ranking and rating metrics:")
    bullet("Precision@K (K=5,10): Fraction of recommended items that are relevant")
    bullet("Recall@K (K=5,10): Fraction of relevant items that are recommended")
    bullet("NDCG@K (K=5,10): Normalised Discounted Cumulative Gain (binary relevance)")
    bullet("RMSE: Root Mean Squared Error on predicted vs actual ratings")
    para("Relevance threshold: rating >= 2 (addtocart and transaction events).")

    # --- Page 4: Expected Outputs ---
    pdf.add_page()
    section("8. Expected Outputs")
    bullet("Cleaned, validated datasets in date-partitioned directory structure")
    bullet("Feature store with versioned user/item/co-occurrence features")
    bullet("SQLite database with queryable feature tables")
    bullet("DVC-tracked data artifacts with lineage metadata")
    bullet("Trained SVD model logged to MLflow with all metrics and artifacts")
    bullet("Top-K recommendations for each user")
    bullet("Data quality report (PDF)")
    bullet("Model performance report (PDF)")

    section("9. Data Quality Requirements")
    para("The pipeline enforces the following quality checks:")
    bullet("Schema validation: correct column names and count per dataset")
    bullet("Null checks: required fields must not be null")
    bullet("Value set: event types must be in {view, addtocart, transaction}")
    bullet("Positive IDs: visitor, item, and category IDs must be positive integers")
    bullet("Duplicate detection: identifies and quantifies duplicate rows")
    bullet("Self-reference: category parentid must not equal categoryid")

    section("10. Technology Stack")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 7, "Component", border=1)
    pdf.cell(80, 7, "Technology", border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    for comp, tech in [
        ("Language", "Python 3.13"),
        ("Data Processing", "Pandas, NumPy"),
        ("Model", "SVD (scipy.sparse.linalg.svds)"),
        ("Experiment Tracking", "MLflow"),
        ("Orchestration", "Prefect"),
        ("Data Versioning", "DVC"),
        ("API Framework", "FastAPI + Uvicorn"),
        ("Database", "SQLite"),
        ("Reporting", "fpdf2, Matplotlib, Seaborn"),
    ]:
        pdf.cell(50, 7, comp, border=1)
        pdf.cell(80, 7, tech, border=1)
        pdf.ln()

    # Save
    pdf.output(str(output_path))
    print(f"Problem formulation report saved to {output_path}")


if __name__ == "__main__":
    generate_problem_formulation()
