# backend/app/utils.py
import os
import json
import re
from typing import List, Tuple, Optional


def read_text_file(path: str, encoding: str = "utf-8") -> str:
    """
    Read a text file and return its contents.
    Raises FileNotFoundError if the path doesn't exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def chunk_text(
    text: str, chunk_size: int = 200, overlap: int = 40
) -> List[str]:
    """
    Simple whitespace-based chunker.
    - chunk_size: number of words per chunk
    - overlap: number of overlapping words between consecutive chunks
    Returns list[str] chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    tokens = text.split()
    out = []
    i = 0
    n = len(tokens)
    while i < n:
        chunk = tokens[i : i + chunk_size]
        out.append(" ".join(chunk))
        i += chunk_size - overlap
    return out


def safe_json_parse(text: str) -> Tuple[Optional[dict], Optional[str]]:
    """
    Try to find and parse JSON in model output.
    Returns (parsed_dict, error_message). If parse succeeds, error_message is None.
    This attempts:
      1. Direct JSON parse
      2. Extract first {...} block and parse
    """
    text = text.strip()
    # First attempt: direct parse
    try:
        parsed = json.loads(text)
        return parsed, None
    except Exception:
        pass

    # Second attempt: find the first JSON object {...}
    match = re.search(r"\{(?:[^{}]|(?R))*\}", text, flags=re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            parsed = json.loads(candidate)
            return parsed, None
        except Exception as e:
            return None, f"found JSON-like block but failed to parse: {e}"

    # Third attempt: try to fix common issues (smart but conservative)
    # Replace single quotes with double quotes, remove trailing commas
    transformed = text.replace("'", '"')
    transformed = re.sub(r",\s*}", "}", transformed)
    transformed = re.sub(r",\s*]", "]", transformed)
    try:
        parsed = json.loads(transformed)
        return parsed, None
    except Exception as e:
        return None, f"no JSON found and basic transforms failed: {e}"


def ensure_dir(path: str) -> None:
    """
    Create directory if it doesn't exist (including parents).
    """
    os.makedirs(path, exist_ok=True)
