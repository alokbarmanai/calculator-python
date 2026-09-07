import json
import logging

from test_report.logging_config import JsonFormatter


def test_json_formatter_creates_structured_log():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test_report",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Report loaded",
        args=(),
        exc_info=None,
    )

    formatted_message = formatter.format(record)
    log_entry = json.loads(formatted_message)

    assert log_entry["level"] == "INFO"
    assert log_entry["logger"] == "test_report"
    assert log_entry["message"] == "Report loaded"
    assert "timestamp" in log_entry
