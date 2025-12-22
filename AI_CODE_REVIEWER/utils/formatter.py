# utils/formatter.py

import black

def run_black_format(code_text: str, line_length: int = 88) -> str:
    """
    Formats the given code using Black.
    
    Args:
        code_text (str): Raw Python code.
        line_length (int): Maximum allowed line length (default 88).
        
    Returns:
        str: Formatted code if successful, or the original code + error message.
    """
    # 1. Safety check: If input is empty, return empty string
    if not code_text or not code_text.strip():
        return ""

    try:
        # 2. Configure Black settings
        mode = black.FileMode(
            line_length=line_length,
            string_normalization=True,  # Enforce double quotes (standard Python style)
            is_pyi=False,
        )
        
        # 3. Run the formatter
        return black.format_str(code_text, mode=mode)

    except black.NothingChanged:
        # Code was already perfect, return as is
        return code_text

    except black.InvalidInput as e:
        # 4. Handle Syntax Errors (e.g., missing brackets)
        # We return this as a comment so it appears in the UI without crashing the app
        return f"# ERROR: Cannot format code because it has Syntax Errors.\n# Details: {str(e)}"

    except Exception as e:
        # 5. Handle unexpected crashes
        return f"# ERROR: Internal formatting failure: {str(e)}"