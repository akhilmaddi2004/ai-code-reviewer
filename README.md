## 🛡️ AI Code Reviewer

- An automated Python code quality analysis tool built using Streamlit, Flake8, Black, and Radon.
- This application analyzes Python code, identifies quality issues, improves formatting, measures complexity, and generates professional reports.

- This project demonstrates real-world static code analysis, automated formatting, complexity measurement, and reporting through a clean web interface.

## 📌 Project Objective

- The objective of this project is to automatically evaluate and improve Python code quality by:

- Detecting coding standard violations

- Formatting code using industry-standard tools

- Measuring cyclomatic complexity and maintainability

- Providing before-and-after code comparison

- Generating downloadable professional reports

## 🧠 Tools & Technologies Used
Tool	Purpose
Streamlit	Web-based user interface
Flake8	Code style and lint analysis
Black	Automatic code formatter
Radon	Complexity & maintainability analysis
FPDF	PDF report generation
Python	Core application logic

### 📂 Project Structure

```text
ai-code-reviewer/
│
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # List of dependencies (streamlit, black, flake8, etc.)
├── README.md               # Project documentation
│
├── utils/                  # Utility modules
│   ├── analyzer.py         # Flake8 style analysis logic
│   ├── formatter.py        # Black formatting logic
│   ├── complexity.py       # Radon complexity analysis
│   └── report.py           # PDF / JSON / TXT report generation
│
├── output/
│   └── reports/            # Directory where generated reports are saved
│
└── screenshots/            # UI images for documentation
    ├── 01_home.png
    ├── 02_code_input.png
    ├── 03_flake8.png
    ├── 04_black.png
    ├── 05_radon.png
    └── 06_report.png
 
## ⚠️ Note About Virtual Environment (Important)

The virtual environment (venv) is intentionally not included in this repository.

Reason:

- The virtual environment contains 100+ auto-generated files

- Best practice is to exclude it from version control

Anyone cloning this repository can recreate the environment easily using requirements.txt.

## 🚀 Features Implemented
✅ 1. Code Input

- Upload a Python (.py) file

- OR paste Python code directly into the UI

✅ 2. Style Analysis (Flake8)

Detects:

- Indentation errors

- Unused imports

- Line length violations

- Syntax issues

Displays:

- Line number

- Error code (E, W, F)

- Clear error description

✅ 3. Code Formatting (Black)

- Automatically formats code using Black

- Displays:

  - ❌ Original code

  - ✅ Formatted code

- Allows download of the cleaned Python file

✅ 4. Complexity & Maintainability (Radon)

Measures:

- Cyclomatic complexity per function

- Maintainability Index (0–100)

Grades:

- A – Low complexity (Good)

- B – Moderate complexity

- C – High risk

- D – Very high risk

✅ 5. Before vs After Code Comparison

- Side-by-side display of:

  - Original code

  - Black-formatted code

- Helps visually understand improvements

✅ 6. Dashboard Summary

Displays:

- Total style violations

- Maintainability score

- Code quality grade

- Lines of code

✅ 7. Professional Report Generation

Users can download reports in multiple formats:

Report Type	Purpose
PDF	Internship / project submission
JSON	Structured analysis data
TXT	Human-readable summary
Fixed Code	Cleaned Python file

## ▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-code-reviewer.git
cd ai-code-reviewer

2️⃣ Create Virtual Environment
python -m venv venv

3️⃣ Activate Virtual Environment

Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Run the Application
streamlit run app.py

6️⃣ Open in Browser
http://localhost:8501

🧪 Example Test Case
✅ 5. Before vs After Code Comparison

### ❌ Poor Code Input 
```python
def calc(a,b):
  if a>10:
    if b>10:
      if a>b:
        return a-b
      else:
        return b-a
    else:
      if a==b:return 0
      else:return a+b
  else:
    for i in range(0,10):
      print(i)
    return None

### ✅ Improved Code Output (Auto-Formatted by Black)
Python

def calc(a, b):
    if a > 10:
        if b > 10:
            if a > b:
                return a - b
            else:
                return b - a
        else:
            if a == b:
                return 0
            else:
                return a + b
    else:
        for i in range(0, 10):
            print(i)
        return None

✅ Improved Output

- Flake8 flags style issues

- Black formats the code

- Radon scores complexity

- PDF report generated

## 🖼️ Screenshots Included (Instead of Video)

The repository includes screenshots showing:

1. Streamlit home screen

2. Code input interface

3. Flake8 analysis output

4. Black before/after comparison

5. Complexity & maintainability dashboard

6. Generated PDF report

Screenshots clearly demonstrate the working of the project and are sufficient for evaluation.

## 📦 Deliverables Checklist

- ✅ Streamlit application

- ✅ Code analysis using Flake8

- ✅ Formatting using Black

- ✅ Complexity analysis using Radon

- ✅ Professional PDF report

- ✅ README documentation

- ✅ Screenshots for proof
