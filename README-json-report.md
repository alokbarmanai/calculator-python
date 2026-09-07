## JSON Test Report Parser

This project includes utilities for parsing pytest JSON test reports.

Generate a JSON report:

```bash
pytest --json-report \
  --json-report-file=sample_data/pytest-report.json \
  --json-report-indent=2
```

Parse the report:

```bash
parse-test-report sample_data/pytest-report.json
```

The parser reports:

- Total tests
- Passed tests
- Failed tests
- Skipped tests
- Pass percentage
- Test execution duration
- Names of failed tests
