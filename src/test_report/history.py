import json
import logging
from pathlib import Path
from typing import Any

from test_report.exceptions import InvalidHistoryError

logger = logging.getLogger(__name__)


def load_history(history_path: str | Path) -> list[dict[str, Any]]:
    """Load and validate multiple test runs from a JSON file."""
    path = Path(history_path)

    logger.info("Loading test history: %s", path)

    if not path.exists():
        logger.error("History file does not exist: %s", path)
        raise InvalidHistoryError(f"History file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as history_file:
            history = json.load(history_file)
    except json.JSONDecodeError as error:
        logger.exception("History contains invalid JSON: %s", path)
        raise InvalidHistoryError(f"Invalid JSON history file: {path}") from error

    validate_history(history, path)

    logger.info(
        "Loaded test history: %s runs=%d",
        path,
        len(history),
    )

    return history


def validate_history(
    history: Any,
    history_path: str | Path = "<memory>",
) -> None:
    """Validate the structure of historical test results."""
    if not isinstance(history, list):
        raise InvalidHistoryError(f"History must contain a list: {history_path}")

    for run_index, run in enumerate(history):
        if not isinstance(run, dict):
            raise InvalidHistoryError(f"Run at index {run_index} must be an object")

        tests = run.get("tests")

        if not isinstance(tests, list):
            raise InvalidHistoryError(
                f"Run at index {run_index} must contain a tests list"
            )

        for test_index, test in enumerate(tests):
            if not isinstance(test, dict):
                raise InvalidHistoryError(
                    f"Test at index {test_index} must be an object"
                )

            if not test.get("nodeid"):
                raise InvalidHistoryError(
                    f"Test at index {test_index} is missing nodeid"
                )

            if test.get("outcome") not in {
                "passed",
                "failed",
                "skipped",
            }:
                raise InvalidHistoryError(
                    f"Test at index {test_index} has invalid outcome"
                )


def collect_test_results(
    history: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """Group outcomes by test node ID."""
    results: dict[str, list[str]] = {}

    for run in history:
        for test in run.get("tests", []):
            nodeid = test.get("nodeid")
            outcome = test.get("outcome")

            if nodeid and outcome:
                results.setdefault(nodeid, []).append(outcome)

    return results


def calculate_test_statistics(
    outcomes_by_test: dict[str, list[str]],
) -> dict[str, dict[str, Any]]:
    """Calculate historical statistics for every test."""
    statistics = {}

    for nodeid, outcomes in outcomes_by_test.items():
        passed = outcomes.count("passed")
        failed = outcomes.count("failed")
        skipped = outcomes.count("skipped")
        total = len(outcomes)

        executed = passed + failed
        pass_rate = round((passed / executed) * 100, 2) if executed else 0.0

        statistics[nodeid] = {
            "total_runs": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": pass_rate,
            "outcomes": outcomes,
        }

    return statistics


def find_flaky_candidates(
    statistics: dict[str, dict[str, Any]],
) -> list[str]:
    """Find tests with both passed and failed outcomes."""
    return [
        nodeid
        for nodeid, data in statistics.items()
        if data["passed"] > 0 and data["failed"] > 0
    ]


def calculate_flaky_rate(test_data: dict[str, Any]) -> float:
    """Calculate the percentage of executed runs that failed."""
    executed_runs = test_data["passed"] + test_data["failed"]

    if executed_runs == 0:
        return 0.0

    return round((test_data["failed"] / executed_runs) * 100, 2)


def calculate_duration_statistics(
    history: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    """Calculate average and maximum duration for each test."""
    durations: dict[str, list[float]] = {}

    for run in history:
        for test in run.get("tests", []):
            nodeid = test.get("nodeid")
            duration = test.get("duration")

            if nodeid and isinstance(duration, int | float):
                durations.setdefault(nodeid, []).append(float(duration))

    statistics = {}

    for nodeid, values in durations.items():
        statistics[nodeid] = {
            "average_seconds": round(sum(values) / len(values), 4),
            "maximum_seconds": round(max(values), 4),
        }

    return statistics
