"""Task 4: Generate Data Quality Report as PDF.

Uses fpdf2 to create a clean PDF summarizing validation results and data profiles.
"""

from pathlib import Path
from fpdf import FPDF

from src.config import REPORTS_DIR, ensure_dir


def generate_report(validation: dict, output_path: str | None = None):
    """Generate a PDF data quality report.

    Args:
        validation: Dict from validators.validate_all() with 'results', 'profiles', 'summary'.
        output_path: Output PDF path. Defaults to reports/data_quality_report.pdf.
    """
    if output_path is None:
        output_path = str(ensure_dir(REPORTS_DIR) / "data_quality_report.pdf")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Title Page ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 20, "Data Quality Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, "RecoMart Recommendation Pipeline", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 10, "Retailrocket E-commerce Dataset", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    # --- Summary ---
    summary = validation.get("summary", {})
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "1. Validation Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Total checks: {summary.get('total', 0)}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Passed: {summary.get('passed', 0)}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Failed: {summary.get('failed', 0)}", new_x="LMARGIN", new_y="NEXT")

    score = 0
    if summary.get("total", 0) > 0:
        score = round(summary["passed"] / summary["total"] * 100, 1)
    pdf.cell(0, 8, f"Quality Score: {score}%", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # --- Check Results Table ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "2. Validation Check Results", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 9)

    col_widths = [35, 45, 15, 95]
    headers = ["Dataset", "Check", "Status", "Details"]
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 8, h, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    for r in validation.get("results", []):
        status = "PASS" if r["passed"] else "FAIL"
        details = r["details"][:80]
        row = [r["dataset"], r["check_name"], status, details]
        for w, val in zip(col_widths, row):
            pdf.cell(w, 7, val, border=1)
        pdf.ln()
    pdf.ln(5)

    # --- Profiling ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "3. Data Profiles", new_x="LMARGIN", new_y="NEXT")

    for ds_name, profile in validation.get("profiles", {}).items():
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Dataset: {ds_name}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, f"Rows: {profile['rows']:,}  |  Columns: {profile['columns']}  |  "
                        f"Memory: {profile['memory_mb']} MB  |  Duplicates: {profile['duplicate_rows']:,}",
                 new_x="LMARGIN", new_y="NEXT")

        # Column stats table
        pdf.set_font("Helvetica", "B", 8)
        cw = [30, 20, 18, 18, 22, 25, 25, 30]
        ch = ["Column", "Type", "Nulls", "Null%", "Unique", "Min", "Max", "Mean"]
        for w, h in zip(cw, ch):
            pdf.cell(w, 7, h, border=1)
        pdf.ln()

        pdf.set_font("Helvetica", "", 7)
        for col, stats in profile.get("column_stats", {}).items():
            vals = [
                col[:12],
                str(stats["dtype"])[:8],
                str(stats["null_count"]),
                str(stats["null_pct"]),
                str(stats["unique_count"]),
                str(stats.get("min", ""))[:10],
                str(stats.get("max", ""))[:10],
                str(stats.get("mean", ""))[:10],
            ]
            for w, v in zip(cw, vals):
                pdf.cell(w, 6, v, border=1)
            pdf.ln()
        pdf.ln(5)

    pdf.output(output_path)
    print(f"Data quality report saved to: {output_path}")
