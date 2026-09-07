import argparse
import logging
from pathlib import Path

from test_report.exceptions import TestReportError
from test_report.history import (
    calculate_duration_statistics,
    calculate_flaky_rate,
    calculate_test_statistics,
    collect_test_results,
    find_flaky_candidates,
    load_history,
)
from test_report.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> int:
    configure_logging()

    parser = argparse.ArgumentParser(
        description="Analyze historical pytest JSON results."
    )
    parser.add_argument(
        "history_path",
        type=Path,
        help="Path to the historical JSON file",
    )

    arguments = parser.parse_args()

    try:
        history = load_history(arguments.history_path)
        results = collect_test_results(history)
        statistics = calculate_test_statistics(results)
        duration_statistics = calculate_duration_statistics(history)
        flaky_candidates = find_flaky_candidates(statistics)

    except TestReportError as error:
        logger.error("Analysis failed: %s", error)
        return 1

    print("Historical Test Analysis")
    print("========================")
    print(f"Number of test runs: {len(history)}")
    print(f"Unique tests:        {len(statistics)}")

    print("\nTest statistics:")

    for nodeid, data in statistics.items():
        failure_rate = calculate_flaky_rate(data)
        duration_data = duration_statistics.get(
            nodeid,
            {
                "average_seconds": 0.0,
                "maximum_seconds": 0.0,
            },
        )

        print(f"\n{nodeid}")
        print(f"  Outcomes:          {', '.join(data['outcomes'])}")
        print(f"  Passed:            {data['passed']}")
        print(f"  Failed:            {data['failed']}")
        print(f"  Skipped:           {data['skipped']}")
        print(f"  Pass rate:         {data['pass_rate']}%")
        print(f"  Failure rate:      {failure_rate}%")
        print(f"  Average duration:  {duration_data['average_seconds']} seconds")
        print(f"  Maximum duration:  {duration_data['maximum_seconds']} seconds")

    print("\nFlaky-test candidates:")

    if not flaky_candidates:
        print("  None found")
    else:
        for nodeid in flaky_candidates:
            print(f"  - {nodeid}")

    logger.info(
        "Analysis completed: runs=%d tests=%d flaky_candidates=%d",
        len(history),
        len(statistics),
        len(flaky_candidates),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
