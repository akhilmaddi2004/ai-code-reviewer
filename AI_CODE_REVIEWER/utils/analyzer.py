# utils/analyzer.py

import subprocess
import tempfile
import os
import re
import logging

# Configure logging for debugging - professional practice
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_flake8_check(code_text: str):
    """
    Runs flake8 on the provided code string to check for style violations.
    
    Args:
        code_text (str): The Python source code to analyze.
        
    Returns:
        list: A list of dictionaries containing error details (line, col, code, message).
    """
    issues = []
    tmp_path = None

    # Regex to safely parse flake8 output: file:line:col: code message
    # Matches format like: /tmp/tmpxyz.py:4:1: E201 Whitespace after '('
    parse_pattern = re.compile(r':(\d+):(\d+):\s([A-Z]\d+)\s(.*)')

    try:
        # Create a temporary file to hold the code
        # delete=False is required for Windows compatibility during subprocess access
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(code_text)
            tmp_path = tmp.name

        # Execute flake8 as a subprocess
        # --isolated prevents user's local config from interfering
        # --format=default ensures standard output we can parse
        result = subprocess.run(
            ["flake8", tmp_path, "--max-line-length=120", "--isolated"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        # Parse the output line by line
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                match = parse_pattern.search(line)
                if match:
                    line_no, col_no, err_code, err_msg = match.groups()
                    issues.append({
                        "line": int(line_no),
                        "column": int(col_no),
                        "code": err_code,
                        "message": err_msg.strip()
                    })

    except Exception as e:
        logger.error(f"Flake8 Analysis Failed: {e}")
        issues.append({
            "line": 0,
            "column": 0,
            "code": "CRITICAL",
            "message": f"Could not run analysis: {str(e)}"
        })

    finally:
        # Strict cleanup to prevent temp file clutter
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                logger.warning(f"Failed to remove temp file: {tmp_path}")

    return issues