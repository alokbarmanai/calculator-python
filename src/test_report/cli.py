import argparse
from pathlib import Path

from test_report.parser import load_report
from test_report.summary import build_summary


def print_summary(summary: dict) -> None:
    print("Test Report Summary")
    print("===================")

    rows = [
        ("Total tests", str(summary["total"])),
        ("Passed", str(summary["passed"])),
        ("Failed", str(summary["failed"])),
        ("Skipped", str(summary["skipped"])),
        ("Pass rate", f"{summary['pass_rate']:.2f}%"),
        ("Duration", f"{summary['duration_seconds']:.2f} seconds"),
    ]

    for label, value in rows:
        print(f"{label:<14} : {value}")

    if summary["failed_tests"]:
        print("\nFailed tests:")
        for test_name in summary["failed_tests"]:
            print(f"  - {test_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a pytest JSON test report.")
    parser.add_argument(
        "report_path",
        type=Path,
        help="Path to the pytest JSON report",
    )

    arguments = parser.parse_args()
    report = load_report(arguments.report_path)
    summary = build_summary(report)
    print_summary(summary)


if __name__ == "__main__":
    main()
