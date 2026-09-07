from typing import Any


def get_test_records(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Return test records from a pytest JSON report."""
    tests = report.get("tests", [])

    if not isinstance(tests, list):
        raise ValueError("The 'tests' field must be a list")

    return [test for test in tests if isinstance(test, dict)]


def count_outcomes(test_records: list[dict[str, Any]]) -> dict[str, int]:
    """Count passed, failed, and skipped tests."""
    counts = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
    }

    for test in test_records:
        outcome = test.get("outcome")

        if outcome in counts:
            counts[outcome] += 1

    return counts


def calculate_pass_rate(counts: dict[str, int]) -> float:
    """Calculate the pass rate excluding skipped tests."""
    executed_tests = counts["passed"] + counts["failed"]

    if executed_tests == 0:
        return 0.0

    return round((counts["passed"] / executed_tests) * 100, 2)


def get_failed_tests(
    test_records: list[dict[str, Any]],
) -> list[str]:
    """Return node IDs for failed tests."""
    return [
        test.get("nodeid", "Unknown test")
        for test in test_records
        if test.get("outcome") == "failed"
    ]


def build_summary(report: dict[str, Any]) -> dict[str, Any]:
    """Build a compact summary from a pytest JSON report."""
    test_records = get_test_records(report)
    counts = count_outcomes(test_records)

    return {
        "total": len(test_records),
        "passed": counts["passed"],
        "failed": counts["failed"],
        "skipped": counts["skipped"],
        "pass_rate": calculate_pass_rate(counts),
        "duration_seconds": report.get("duration", 0.0),
        "failed_tests": get_failed_tests(test_records),
    }
