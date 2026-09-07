import json

import pytest

from test_report.exceptions import (
    InvalidReportError,
    ReportFileNotFoundError,
)
from test_report.parser import load_report
from test_report.summary import (
    build_summary,
    calculate_pass_rate,
    count_outcomes,
    get_failed_tests,
)


def test_load_report(tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(
        json.dumps({"tests": [], "duration": 1.25}),
        encoding="utf-8",
    )

    report = load_report(report_path)

    assert report["duration"] == 1.25
    assert report["tests"] == []


def test_load_report_raises_for_missing_file(tmp_path):
    report_path = tmp_path / "missing.json"

    with pytest.raises(ReportFileNotFoundError):
        load_report(report_path)


def test_load_report_raises_for_invalid_json(tmp_path):
    report_path = tmp_path / "invalid.json"
    report_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(InvalidReportError, match="Invalid JSON report"):
        load_report(report_path)


def test_count_outcomes():
    test_records = [
        {"outcome": "passed"},
        {"outcome": "passed"},
        {"outcome": "failed"},
        {"outcome": "skipped"},
    ]

    assert count_outcomes(test_records) == {
        "passed": 2,
        "failed": 1,
        "skipped": 1,
    }


def test_calculate_pass_rate():
    counts = {
        "passed": 8,
        "failed": 2,
        "skipped": 5,
    }

    assert calculate_pass_rate(counts) == 80.0


def test_calculate_pass_rate_with_no_executed_tests():
    counts = {
        "passed": 0,
        "failed": 0,
        "skipped": 3,
    }

    assert calculate_pass_rate(counts) == 0.0


def test_get_failed_tests():
    test_records = [
        {"nodeid": "test_add", "outcome": "passed"},
        {"nodeid": "test_divide", "outcome": "failed"},
    ]

    assert get_failed_tests(test_records) == ["test_divide"]


def test_build_summary():
    report = {
        "duration": 2.5,
        "tests": [
            {"nodeid": "test_add", "outcome": "passed"},
            {"nodeid": "test_divide", "outcome": "failed"},
            {"nodeid": "test_skip", "outcome": "skipped"},
        ],
    }

    summary = build_summary(report)

    assert summary == {
        "total": 3,
        "passed": 1,
        "failed": 1,
        "skipped": 1,
        "pass_rate": 50.0,
        "duration_seconds": 2.5,
        "failed_tests": ["test_divide"],
    }
