import json

import pytest

from test_report.exceptions import (
    InvalidHistoryError,
    InvalidReportError,
    ReportFileNotFoundError,
)
from test_report.history import load_history
from test_report.parser import load_report


def test_missing_report_raises_custom_exception(tmp_path):
    report_path = tmp_path / "missing.json"

    with pytest.raises(ReportFileNotFoundError):
        load_report(report_path)


def test_invalid_report_root_raises_exception(tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(
        json.dumps(["not", "an", "object"]),
        encoding="utf-8",
    )

    with pytest.raises(InvalidReportError):
        load_report(report_path)


def test_report_without_tests_raises_exception(tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(
        json.dumps({"duration": 1.5}),
        encoding="utf-8",
    )

    with pytest.raises(InvalidReportError):
        load_report(report_path)


def test_report_with_invalid_outcome_raises_exception(tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text(
        json.dumps(
            {
                "tests": [
                    {
                        "nodeid": "test_example",
                        "outcome": "unknown",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(InvalidReportError):
        load_report(report_path)


def test_invalid_history_root_raises_exception(tmp_path):
    history_path = tmp_path / "history.json"
    history_path.write_text(
        json.dumps({"tests": []}),
        encoding="utf-8",
    )

    with pytest.raises(InvalidHistoryError):
        load_history(history_path)
