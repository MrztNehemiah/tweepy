from pathlib import Path
import re


def sanitize_filename(filename: str) -> str:
    """Remove dangerous characters and ensure safe filename"""
    # Get just the filename without path components
    safe_name = Path(filename).name
    # Remove or replace dangerous characters
    safe_name = re.sub(r"[^\w\s.-]", "", safe_name)
    # Prevent hidden files and ensure not empty
    safe_name = safe_name.lstrip(".")
    if not safe_name:
        raise ValueError("Invalid filename")
    return safe_name
