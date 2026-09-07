import json
from pathlib import Path
from typing import Any


def load_report(report_path: str | Path) -> dict[str, Any]:
    """Load a JSON test report from disk."""
    path = Path(report_path)

    if not path.exists():
        raise FileNotFoundError(f"Report file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Report path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as report_file:
            data = json.load(report_file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON report: {path}") from error

    if not isinstance(data, dict):
        raise ValueError("The JSON report must contain an object at the root")

    return data
