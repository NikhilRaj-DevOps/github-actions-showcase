import unittest
from pathlib import Path

from src.ops_monitor import CheckResult, ServiceMonitor, format_summary, load_targets


class OpsMonitorTests(unittest.TestCase):
    def test_load_targets_from_config_file(self):
        config_path = Path("tests/sample_monitor_targets.txt")
        targets = load_targets(config_path)
        self.assertEqual(
            targets,
            [
                "https://example.com",
                "https://github.com",
                "https://nikhilraj-devops.github.io",
            ],
        )

    def test_invalid_scheme_is_rejected(self):
        monitor = ServiceMonitor()
        with self.assertRaises(ValueError):
            monitor.check_url("file:///tmp/test.txt")

    def test_check_result_success_status(self):
        result = CheckResult(url="https://example.com", status_code=200, response_time_ms=120, available=True)
        self.assertEqual(result.status_label, "UP")

    def test_check_result_failure_status(self):
        result = CheckResult(url="https://example.com", status_code=503, response_time_ms=300, available=False)
        self.assertEqual(result.status_label, "DOWN")

    def test_format_summary_lists_multiple_results(self):
        results = [
            CheckResult(url="https://example.com", status_code=200, response_time_ms=120, available=True),
            CheckResult(url="https://status.example.org", status_code=503, response_time_ms=400, available=False),
        ]
        summary = format_summary(results)
        self.assertIn("https://example.com", summary)
        self.assertIn("UP", summary)
        self.assertIn("status.example.org", summary)
        self.assertIn("DOWN", summary)

    def test_monitor_can_build_a_result_without_network(self):
        monitor = ServiceMonitor(timeout_seconds=0.1)
        result = monitor.check_url("https://example.com")
        self.assertIn(result.url, "https://example.com")
        self.assertIsInstance(result.status_code, int)
        self.assertIsInstance(result.response_time_ms, int)


if __name__ == "__main__":
    unittest.main()
