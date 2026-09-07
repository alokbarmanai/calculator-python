class TestReportError(Exception):
    """Base exception for test-report errors."""


class ReportFileNotFoundError(TestReportError):
    """Raised when a report file does not exist."""


class InvalidReportError(TestReportError):
    """Raised when a report has an invalid structure."""


class InvalidHistoryError(TestReportError):
    """Raised when historical test data is invalid."""
