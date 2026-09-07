import json
import logging
from pathlib import Path
from typing import Any

from test_report.exceptions import (
    InvalidReportError,
    ReportFileNotFoundError,
)

logger = logging.getLogger(__name__)


def load_report(report_path: str | Path) -> dict[str, Any]:
    """Load and validate a JSON test report."""
    path = Path(report_path)

    logger.info("Loading test report: %s", path)

    if not path.exists():
        logger.error("Report file does not exist: %s", path)
        raise ReportFileNotFoundError(f"Report file not found: {path}")

    if not path.is_file():
        logger.error("Report path is not a file: %s", path)
        raise InvalidReportError(f"Report path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as report_file:
            data = json.load(report_file)
    except json.JSONDecodeError as error:
        logger.exception("Report contains invalid JSON: %s", path)
        raise InvalidReportError(f"Invalid JSON report: {path}") from error

    validate_report(data, path)

    logger.info("Successfully loaded test report: %s", path)

    return data


def validate_report(
    report: Any,
    report_path: str | Path = "<memory>",
) -> None:
    """Validate the minimum structure of a pytest JSON report."""
    if not isinstance(report, dict):
        raise InvalidReportError(f"Report must contain a JSON object: {report_path}")

    tests = report.get("tests")

    if tests is None:
        raise InvalidReportError(f"Report is missing the 'tests' field: {report_path}")

    if not isinstance(tests, list):
        raise InvalidReportError(f"The 'tests' field must be a list: {report_path}")

    for index, test in enumerate(tests):
        if not isinstance(test, dict):
            raise InvalidReportError(f"Test at index {index} must be an object")

        if not test.get("nodeid"):
            raise InvalidReportError(f"Test at index {index} is missing 'nodeid'")

        if test.get("outcome") not in {
            "passed",
            "failed",
            "skipped",
        }:
            raise InvalidReportError(f"Test at index {index} has an invalid outcome")
