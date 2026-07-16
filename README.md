# GitHub Actions Showcase

![CI](https://github.com/NikhilRaj-DevOps/github-actions-showcase/actions/workflows/ci.yml/badge.svg)

This repository is a compact example project designed to demonstrate practical GitHub Actions usage in a real GitHub repo.

## What it showcases

- CI workflow on push and pull request
- Python test matrix across multiple versions
- Build packaging and archive generation
- Tag-based release automation
- GitHub-hosted runner best practices

## Project structure

```text
.github/workflows/
  ci.yml
  release.yml
src/
  greeter.py
tests/
  test_greeter.py
```

## Local verification

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Workflow highlights

- `ci.yml` runs validation, unit tests, and archive creation.
- `release.yml` publishes a GitHub release when a `v*` tag is pushed.
- The release path demonstrates package distribution without relying on the deprecated artifact upload step.
