import pytest

from test_report.summary import (
    build_summary,
    calculate_pass_rate,
    count_outcomes,
    get_failed_tests,
)


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


@pytest.mark.parametrize(
    ("counts", "expected_rate"),
    [
        (
            {"passed": 8, "failed": 2, "skipped": 0},
            80.0,
        ),
        (
            {"passed": 3, "failed": 0, "skipped": 2},
            100.0,
        ),
        (
            {"passed": 0, "failed": 0, "skipped": 3},
            0.0,
        ),
    ],
)
def test_calculate_pass_rate(counts, expected_rate):
    assert calculate_pass_rate(counts) == expected_rate


def test_get_failed_tests():
    test_records = [
        {
            "nodeid": "test_add",
            "outcome": "passed",
        },
        {
            "nodeid": "test_divide",
            "outcome": "failed",
        },
    ]

    assert get_failed_tests(test_records) == ["test_divide"]


def test_build_summary():
    report = {
        "duration": 2.5,
        "tests": [
            {
                "nodeid": "test_add",
                "outcome": "passed",
            },
            {
                "nodeid": "test_divide",
                "outcome": "failed",
            },
            {
                "nodeid": "test_skip",
                "outcome": "skipped",
            },
        ],
    }

    summary = build_summary(report)

    assert summary["total"] == 3
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["skipped"] == 1
    assert summary["pass_rate"] == 50.0
    assert summary["duration_seconds"] == 2.5
    assert summary["failed_tests"] == ["test_divide"]
