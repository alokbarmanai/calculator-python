from test_report.history import (
    calculate_flaky_rate,
    calculate_test_statistics,
    collect_test_results,
    find_flaky_candidates,
)


def test_collect_test_results():
    history = [
        {
            "run_id": "run-1",
            "tests": [
                {"nodeid": "test_add", "outcome": "passed"},
                {"nodeid": "test_divide", "outcome": "failed"},
            ],
        },
        {
            "run_id": "run-2",
            "tests": [
                {"nodeid": "test_add", "outcome": "passed"},
                {"nodeid": "test_divide", "outcome": "passed"},
            ],
        },
    ]

    results = collect_test_results(history)

    assert results == {
        "test_add": ["passed", "passed"],
        "test_divide": ["failed", "passed"],
    }


def test_calculate_test_statistics():
    outcomes = {
        "test_divide": ["passed", "failed", "passed"],
    }

    statistics = calculate_test_statistics(outcomes)

    assert statistics["test_divide"]["passed"] == 2
    assert statistics["test_divide"]["failed"] == 1
    assert statistics["test_divide"]["pass_rate"] == 66.67


def test_find_flaky_candidates():
    statistics = {
        "stable_test": {
            "passed": 3,
            "failed": 0,
            "skipped": 0,
        },
        "flaky_test": {
            "passed": 2,
            "failed": 1,
            "skipped": 0,
        },
        "failing_test": {
            "passed": 0,
            "failed": 3,
            "skipped": 0,
        },
    }

    assert find_flaky_candidates(statistics) == ["flaky_test"]


def test_calculate_flaky_rate():
    test_data = {
        "passed": 2,
        "failed": 1,
        "skipped": 0,
    }

    assert calculate_flaky_rate(test_data) == 33.33
