# utils/complexity.py

from radon.complexity import cc_visit
from radon.metrics import mi_visit
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_rank(score: int) -> str:
    """
    Converts a complexity score into a letter grade.
    1-5: A (Low risk - Good)
    6-10: B (Moderate risk)
    11-20: C (High risk)
    21+: D (Very high risk)
    """
    if score <= 5: return 'A'
    if score <= 10: return 'B'
    if score <= 20: return 'C'
    return 'D'

def run_complexity_analysis(code_text: str) -> dict:
    """
    Analyzes both Cyclomatic Complexity and Maintainability Index.

    Args:
        code_text (str): The Python source code.

    Returns:
        dict: Contains a list of blocks and the overall maintainability score.
    """
    results = {
        "blocks": [],
        "maintainability_index": 0,
        "mi_rank": "F", # Default to fail if analysis breaks
        "error": None
    }

    # Safety check for empty input
    if not code_text or not code_text.strip():
        return results

    try:
        # 1. Calculate Cyclomatic Complexity (Function/Class level)
        blocks = cc_visit(code_text)
        
        for block in blocks:
            # Determine if it's a Function (F) or Class (C) for clarity
            block_type = "Function" if hasattr(block, 'is_method') else "Class"
            
            results["blocks"].append({
                "name": block.name,
                "type": block_type,
                "complexity": block.complexity,
                "rank": get_rank(block.complexity),
                "line_start": block.lineno,
                "line_end": block.endline,
            })

        # 2. Calculate Maintainability Index (Overall file health: 0-100)
        # 100 is best, 0 is worst
        mi_score = mi_visit(code_text, multi=False)
        
        # Rank the MI score: >75 is A, >50 is B, else C
        mi_rank = 'A' if mi_score >= 75 else 'B' if mi_score >= 50 else 'C'
        
        results["maintainability_index"] = round(mi_score, 2)
        results["mi_rank"] = mi_rank

    except SyntaxError:
        results["error"] = "Syntax Error: Fix your code before analyzing complexity."
    except Exception as e:
        logger.error(f"Complexity Analysis Failed: {e}")
        results["error"] = str(e)

    return results