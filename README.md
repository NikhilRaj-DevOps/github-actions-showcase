# GitHub Actions Showcase

This repository is a compact example project designed to demonstrate practical GitHub Actions usage in a real GitHub repo.

## What it showcases

- CI workflow on push and pull request
- Python test matrix across multiple versions
- Artifact upload from a build job
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

- `ci.yml` runs lint-like validation, unit tests, and archive creation.
- `release.yml` publishes a GitHub release when a `v*` tag is pushed.
- The build artifact keeps the repo’s GitHub Actions story concrete and demonstrable.
