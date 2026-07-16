"""Simple greeting utilities for a GitHub Actions showcase repo."""


def format_greeting(name: str, greeting: str = "Hello") -> str:
    """Return a greeting string for the provided name."""
    normalized_name = name.strip()
    if not normalized_name:
        raise ValueError("name must not be empty")
    return f"{greeting}, {normalized_name}!"


def get_project_name() -> str:
    """Return the project identifier used in the examples."""
    return "github-actions-showcase"
