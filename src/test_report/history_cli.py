import argparse
from pathlib import Path

from test_report.history import (
    calculate_flaky_rate,
    calculate_test_statistics,
    collect_test_results,
    find_flaky_candidates,
    load_history,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze historical pytest JSON results."
    )
    parser.add_argument(
        "history_path",
        type=Path,
        help="Path to the historical JSON file",
    )

    arguments = parser.parse_args()
    history = load_history(arguments.history_path)
    results = collect_test_results(history)
    statistics = calculate_test_statistics(results)
    flaky_candidates = find_flaky_candidates(statistics)

    print("Historical Test Analysis")
    print("========================")
    print(f"Number of test runs: {len(history)}")
    print(f"Unique tests:        {len(statistics)}")

    print("\nTest statistics:")

    for nodeid, data in statistics.items():
        failure_rate = calculate_flaky_rate(data)

        print(f"\n{nodeid}")
        print(f"  Outcomes:       {', '.join(data['outcomes'])}")
        print(f"  Passed:         {data['passed']}")
        print(f"  Failed:         {data['failed']}")
        print(f"  Skipped:        {data['skipped']}")
        print(f"  Pass rate:      {data['pass_rate']}%")
        print(f"  Failure rate:   {failure_rate}%")

    print("\nFlaky-test candidates:")

    if not flaky_candidates:
        print("  None found")
    else:
        for nodeid in flaky_candidates:
            print(f"  - {nodeid}")


if __name__ == "__main__":
    main()
