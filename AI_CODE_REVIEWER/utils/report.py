# utils/report.py

import os
import json
from datetime import datetime
from fpdf import FPDF

# Set up paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _timestamp():
    """Returns a clean timestamp string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# --------------------------------------------------
# 1. JSON REPORT (Raw Data)
# --------------------------------------------------
def save_as_json(data, filename="report"):
    path = os.path.join(OUTPUT_DIR, f"{filename}_{_timestamp()}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return path
    except Exception as e:
        return f"Error saving JSON: {e}"


# --------------------------------------------------
# 2. CLEAN TEXT REPORT (Human Readable)
# --------------------------------------------------
def save_as_text(data, filename="report"):
    path = os.path.join(OUTPUT_DIR, f"{filename}_{_timestamp()}.txt")
    
    # Extract complexity data safely
    comp_data = data.get("complexity", {})
    blocks = comp_data.get("blocks", [])
    mi_score = comp_data.get("maintainability_index", "N/A")
    mi_rank = comp_data.get("mi_rank", "N/A")

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("AI CODE REVIEW REPORT\n")
            f.write("=" * 40 + "\n\n")

            # --- STYLE SECTION ---
            f.write(f"STYLE ISSUES ({len(data.get('style_issues', []))} found)\n")
            f.write("-" * 20 + "\n")
            for issue in data.get("style_issues", []):
                if "error" in issue:
                    f.write(f"CRITICAL ERROR: {issue['error']}\n")
                else:
                    f.write(f"[Line {issue['line']}] {issue['code']}: {issue['message']}\n")
            f.write("\n")

            # --- COMPLEXITY SECTION ---
            f.write("COMPLEXITY ANALYSIS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Overall Maintainability: {mi_score}/100 (Grade: {mi_rank})\n\n")
            
            f.write(f"{'Name':<30} {'Type':<10} {'Complexity':<10} {'Rank':<5}\n")
            f.write("-" * 60 + "\n")
            
            for block in blocks:
                f.write(f"{block['name']:<30} {block['type']:<10} {block['complexity']:<10} {block['rank']:<5}\n")

        return path
    except Exception as e:
        return f"Error saving Text Report: {e}"


# --------------------------------------------------
# 3. PDF REPORT (Professional & Internship Ready)
# --------------------------------------------------
def save_as_pdf(original_code, formatted_code, analysis_results, filename="report"):
    path = os.path.join(OUTPUT_DIR, f"{filename}_{_timestamp()}.pdf")
    
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # --- Helper for Titles ---
        def add_section_title(title):
            pdf.ln(8)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, title, ln=True)
            pdf.set_font("Arial", size=10) # Reset to normal

        # --- Helper for Code Blocks ---
        def add_code_block(code_text):
            pdf.set_font("Courier", size=9) # Monospace is key for code
            pdf.set_fill_color(240, 240, 240) # Light gray background
            # Encode to latin-1 to prevent FPDF crashes with special chars
            safe_text = code_text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 5, safe_text, fill=True)
            pdf.set_font("Arial", size=10) # Reset

        # Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Automated Code Review Report", ln=True, align='C')
        pdf.ln(5)

        # 1. Complexity
        comp_data = analysis_results.get("complexity", {})
        add_section_title("1. Complexity & Maintainability")
        pdf.cell(0, 6, f"Maintainability Index: {comp_data.get('maintainability_index', 'N/A')} (Grade: {comp_data.get('mi_rank', 'N/A')})", ln=True)
        
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(60, 6, "Function/Class", border=1)
        pdf.cell(30, 6, "Complexity", border=1)
        pdf.cell(30, 6, "Rank", border=1)
        pdf.ln()
        pdf.set_font("Arial", size=10)

        for block in comp_data.get("blocks", []):
            pdf.cell(60, 6, block['name'], border=1)
            pdf.cell(30, 6, str(block['complexity']), border=1)
            pdf.cell(30, 6, block['rank'], border=1)
            pdf.ln()

        # 2. Style Issues
        add_section_title("2. Style Issues (Flake8)")
        issues = analysis_results.get("style_issues", [])
        if not issues:
            pdf.cell(0, 6, "No style issues found. Good job!", ln=True)
        else:
            for issue in issues:
                text = f"[Line {issue['line']}] {issue['code']}: {issue['message']}"
                pdf.multi_cell(0, 6, text)

        # 3. Code Previews
        add_section_title("3. Original Code")
        add_code_block(original_code)

        add_section_title("4. Formatted Code (Black)")
        add_code_block(formatted_code)

        pdf.output(path)
        return path

    except Exception as e:
        return f"Error generating PDF: {e}"