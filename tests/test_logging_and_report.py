import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from file_manager.write_to_file import close_logger, configure_logger, generate_report


class LoggingAndReportTests(unittest.TestCase):
    def test_generate_report_includes_summary_and_errors(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            host = SimpleNamespace(id="host-123", name="Host-One")
            report_path = generate_report(
                "certificate_update",
                [host],
                errors=[("host-456", "permission denied")],
                out_dir=tmpdir,
            )

            self.assertTrue(Path(report_path).exists())
            content = Path(report_path).read_text(encoding="utf-8")
            self.assertIn("Total successful updates: 1", content)
            self.assertIn("ERROR:", content)
            self.assertIn("host-456", content)

    def test_configure_logger_creates_file_and_console_handlers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "certificate_update.log"
            logger = configure_logger(log_path=str(log_path), console=True)

            logger.info("sample log message")
            self.assertTrue(log_path.exists())
            content = log_path.read_text(encoding="utf-8")
            self.assertIn("sample log message", content)
            close_logger(logger)


if __name__ == "__main__":
    unittest.main()
