# app.py

import os
import streamlit as st

# Import our modularized utility functions
from utils.analyzer import run_flake8_check
from utils.formatter import run_black_format
from utils.complexity import run_complexity_analysis
from utils.report import save_as_json, save_as_text, save_as_pdf

# -------------------------------------------------
# 1. Configuration & Global Styles
# -------------------------------------------------
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a SaaS-like look
# FIXED: Stronger CSS to ensure dashboard visibility
st.markdown("""
    <style>
    /* Force Main Background to be White */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Metric Cards - High Contrast Fix */
    div[data-testid="stMetric"] {
        background-color: #F0F2F6 !important; /* Light Gray Background */
        border: 2px solid #D1D5DB !important; /* Visible Gray Border */
        padding: 15px !important;
        border-radius: 8px !important;
        color: #000000 !important; /* Force Black Text */
    }
    
    /* Metric Label (Small Text) */
    div[data-testid="stMetric"] label {
        color: #333333 !important; /* Dark Gray */
    }

    /* Metric Value (Big Number) */
    div[data-testid="stMetricValue"] {
        color: #000000 !important; /* Pitch Black */
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 3em;
    }
    /* Header Styling */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 2. Sidebar Navigation
# -------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("AI Code Reviewer")
    st.caption("v1.0.0 | Internship Build")
    
    st.markdown("---")
    
    with st.expander("📖 How to use"):
        st.markdown("""
        1. **Upload** or **Paste** your Python code.
        2. Click **Analyze & Optimize**.
        3. View **Style Errors** & **Complexity**.
        4. Download the **Cleaned Code**.
        """)
    
    st.markdown("### ⚙️ Settings")
    st.checkbox("Show Line Numbers", value=True, key="show_lines")
    st.info("Powered by Flake8, Black & Radon")

# -------------------------------------------------
# 3. Main Header & Input Area
# -------------------------------------------------
st.title("🛡️ Automated Code Quality & Security Reviewer")
st.markdown("Optimize your Python code to industry standards in seconds.")

input_tab1, input_tab2 = st.tabs(["📂 Upload File", "📝 Paste Code"])

code_input = ""
filename = "manual_input"

with input_tab1:
    uploaded_file = st.file_uploader("Drop your Python script here...", type=["py"])
    if uploaded_file:
        code_input = uploaded_file.read().decode("utf-8")
        filename = uploaded_file.name.replace(".py", "")

with input_tab2:
    text_area_code = st.text_area("Or paste raw code here...", height=200)
    if not uploaded_file and text_area_code:
        code_input = text_area_code

# -------------------------------------------------
# 4. Analysis Logic
# -------------------------------------------------
if st.button("✨ Analyze & Optimize Code", type="primary"):
    
    if not code_input.strip():
        st.warning("⚠️ Please provide some code to analyze.")
        st.stop()

    # Progress Bar Animation
    progress_text = "Operation in progress. Please wait..."
    my_bar = st.progress(0, text=progress_text)
    
    # 1. Run Style Check
    my_bar.progress(30, text="Checking Style Guidelines (Flake8)...")
    style_issues = run_flake8_check(code_input)
    
    # 2. Run Formatting
    my_bar.progress(60, text="Formatting Code (Black)...")
    formatted_code = run_black_format(code_input)
    
    # 3. Run Complexity
    my_bar.progress(90, text="Calculating Cognitive Complexity (Radon)...")
    complexity_data = run_complexity_analysis(code_input)
    
    my_bar.progress(100, text="Analysis Complete!")
    my_bar.empty()

    # Aggregate results
    full_results = {
        "style_issues": style_issues,
        "complexity": complexity_data,
        "black_preview": formatted_code
    }

    # -------------------------------------------------
    # 5. Dashboard Results (Linear Layout)
    # -------------------------------------------------
    st.divider()
    
    # --- A. Health Summary Cards ---
    st.subheader("📊 Dashboard Overview")
    m1, m2, m3, m4 = st.columns(4)
    
    issue_count = len(style_issues)
    mi_score = complexity_data.get("maintainability_index", 0)
    mi_rank = complexity_data.get("mi_rank", "N/A")
    
    m1.metric("Style Violations", issue_count, delta="Lower is better", delta_color="inverse")
    m2.metric("Maintainability Index", f"{mi_score}", delta="Target: >50")
    m3.metric("Health Grade", mi_rank)
    m4.metric("Lines of Code", len(code_input.splitlines()))

    # --- B. Code Comparison ---
    st.divider()
    st.subheader("🆚 Code Optimization (Before vs After)")
    
    col_orig, col_fix = st.columns(2)
    with col_orig:
        st.caption("❌ Original Input (Messy)")
        st.code(code_input, language="python", line_numbers=st.session_state.show_lines)
    with col_fix:
        st.caption("✅ Optimized Output (Clean)")
        st.code(formatted_code, language="python", line_numbers=st.session_state.show_lines)

    # --- C. Detailed Issues ---
    st.divider()
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("🐞 Style Issues Found")
        if not style_issues:
            st.success("🎉 No issues found! Excellent work.")
        else:
            with st.expander("View all style violations", expanded=True):
                for issue in style_issues:
                    st.markdown(f"**Line {issue['line']}**: `{issue['code']}` - {issue['message']}")
    
    with c2:
        st.subheader("🧠 Complexity Analysis")
        blocks = complexity_data.get("blocks", [])
        if blocks:
            st.dataframe(
                blocks, 
                column_config={
                    "name": "Function Name",
                    "complexity": st.column_config.NumberColumn("Score", format="%d"),
                    "rank": "Grade"
                },
                use_container_width=True
            )
        else:
            st.info("No complex functions detected.")

    # --- D. Export Section ---
    st.divider()
    st.subheader("📥 Download Reports & Code")
    
    # Generate files
    pdf_path = save_as_pdf(code_input, formatted_code, full_results, filename)
    json_path = save_as_json(full_results, filename)
    
    b1, b2, b3 = st.columns(3)
    
    with b1:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name=f"{filename}_Review.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with b2:
        with open(json_path, "rb") as f:
            st.download_button(
                label="📊 Download JSON Data",
                data=f,
                file_name=f"{filename}_metrics.json",
                mime="application/json",
                use_container_width=True
            )
            
    with b3:
        st.download_button(
            label="🐍 Download Fixed Code",
            data=formatted_code,
            file_name=f"fixed_{filename}.py",
            mime="text/x-python",
            use_container_width=True,
            type="primary"
        )

# -------------------------------------------------
# 6. Footer
# -------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>"
    "Built for Python Developers | AI Code Reviewer v1.0"
    "</div>", 
    unsafe_allow_html=True
)