# GitHub Actions Showcase

![CI](https://github.com/NikhilRaj-DevOps/github-actions-showcase/actions/workflows/ci.yml/badge.svg)

This repository is a compact example project designed to demonstrate practical GitHub Actions usage in a real GitHub repo.

## What it showcases

- CI workflow on push and pull request
- Python test matrix across multiple versions
- Security scanning in the pipeline
- Mid-level Python application for SRE/DevOps-style health checks
- Build packaging and archive generation- Scheduled monitoring workflow for live health-check execution- Tag-based release automation
- GitHub-hosted runner best practices

## Project structure

```text
.github/
  workflows/
    ci.yml
    release.yml
src/
  greeter.py
  ops_monitor.py
tests/
  test_greeter.py
  test_ops_monitor.py
```

## Local verification

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

### Run the SRE/DevOps monitor CLI

```bash
python3 -m src.ops_monitor https://example.com https://status.example.org
```

Or use the included config file:

```bash
python3 -m src.ops_monitor --config tests/sample_monitor_targets.txt
```

This prints a simple health summary for each URL and exits with a non-zero status if any monitored endpoint is down.

## Workflow highlights

- `ci.yml` runs validation, security scanning, unit tests, and archive creation.
- `release.yml` publishes a GitHub release when a `v*` tag is pushed and includes generated changelog notes.
- The release path demonstrates package distribution without relying on the deprecated artifact upload step.
