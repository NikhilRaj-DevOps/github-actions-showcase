"""Simple SRE/DevOps health-check monitor for a GitHub Actions showcase.

This module provides a lightweight way to probe URLs and generate a simple summary.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys
import time
from typing import Iterable, List
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass
class CheckResult:
    url: str
    status_code: int
    response_time_ms: int
    available: bool

    @property
    def status_label(self) -> str:
        return "UP" if self.available else "DOWN"


class ServiceMonitor:
    """Minimal HTTP health checker used for SRE-style demo workflows."""

    def __init__(self, timeout_seconds: float = 2.0) -> None:
        self.timeout_seconds = timeout_seconds

    def check_url(self, url: str) -> CheckResult:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only HTTP(S) URLs are supported for health checks")

        request = Request(url, headers={"User-Agent": "github-actions-showcase-monitor/1.0"})
        start = time.perf_counter()
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - intentional outbound HTTP(S) health check
                status_code = int(response.getcode())
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                return CheckResult(
                    url=url,
                    status_code=status_code,
                    response_time_ms=elapsed_ms,
                    available=status_code < 400,
                )
        except HTTPError as exc:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return CheckResult(
                url=url,
                status_code=int(exc.code),
                response_time_ms=elapsed_ms,
                available=False,
            )
        except URLError:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return CheckResult(
                url=url,
                status_code=0,
                response_time_ms=elapsed_ms,
                available=False,
            )


def load_targets(config_path: str | Path) -> List[str]:
    target_lines = Path(config_path).read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in target_lines if line.strip() and not line.strip().startswith("#")]


def check_urls(urls: Iterable[str], timeout_seconds: float = 2.0) -> List[CheckResult]:
    monitor = ServiceMonitor(timeout_seconds=timeout_seconds)
    return [monitor.check_url(url) for url in urls]


def format_summary(results: List[CheckResult]) -> str:
    lines = ["Service Health Summary"]
    for result in results:
        lines.append(
            f"- {result.url} | {result.status_label} | HTTP {result.status_code} | {result.response_time_ms} ms"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a simple SRE/DevOps health check against one or more URLs.")
    parser.add_argument("urls", nargs="*", help="One or more URLs to probe.")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a text file containing URLs to check, one per line.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Timeout in seconds for each network request (default: 2.0)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    urls = list(args.urls)
    if args.config:
        urls.extend(load_targets(args.config))

    if not urls:
        parser.error("provide at least one URL or a --config file")

    results = check_urls(urls, timeout_seconds=args.timeout)
    print(format_summary(results))

    if any(not result.available for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
