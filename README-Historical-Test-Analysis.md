## Historical Test Analysis

The project can analyze multiple pytest JSON results and identify
potential flaky-test candidates.

Run the analyzer:

```bash
python src/test_report/history_cli.py sample_data/history.json
```

A test is considered a flaky candidate when it has both passed and failed
across multiple runs with the same code.

The analysis reports:

- Per-test execution count
- Passed count
- Failed count
- Skipped count
- Pass rate
- Failure rate
- Potential flaky tests
