"""Tooling and hygiene contracts for the repository (SRS Deliverables 12, 13, 14; spec 19)."""

import re
import tomllib
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[1]

README_HEADINGS = [
    # Deliverable 12: installation instructions
    "Python installation",
    "Virtual environment setup",
    "Dependency installation",
    "GenAI API configuration",
    "Secure API-key storage",
    "Database configuration",
    "Knowledge-base setup",
    "Complaint dataset setup",
    "Application startup",
    "Test execution",
    "Troubleshooting",
    # Deliverable 13: execution instructions
    "Login",
    "Upload company documents",
    "Configure complaint rules",
    "Submit complaint",
    "Analyze complaint",
    "Review GenAI output",
    "Run Python validation",
    "Review mismatches",
    "Generate response",
    "Escalate complaint",
    "Review manual queue",
    "Track complaint",
    "View analytics",
    "Generate reports",
    # Deliverable 14 and 15: repository and evaluation information
    "Evaluation",
    "Evaluator credentials",
    "Assumptions",
    "Limitations",
    "Blog",
    "Demonstration video",
]

MAKE_TARGETS = ["setup", "seed", "run", "api", "test", "check", "eval-holdout"]

PYTEST_MARKERS = ["unit", "integration", "e2e", "live_llm", "hidden"]


def _read(name: str) -> str:
    return (REPO_ROOT / name).read_text(encoding="utf-8")


def _markdown_headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{1,6}\s+(.+)$", text, re.MULTILINE)}


@pytest.mark.parametrize("heading", README_HEADINGS)
def test_readme_has_required_section(heading: str) -> None:
    assert heading in _markdown_headings(_read("README.md"))


@pytest.mark.parametrize("target", MAKE_TARGETS)
def test_makefile_defines_documented_target(target: str) -> None:
    assert re.search(rf"^{re.escape(target)}:", _read("Makefile"), re.MULTILINE)


def test_env_example_declares_keys_without_values() -> None:
    assignments = [
        line
        for line in _read(".env.example").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert assignments, ".env.example declares no variables"
    for line in assignments:
        key, _, value = line.partition("=")
        assert value.strip() == "", f"{key} must not carry a value in .env.example"


def test_env_example_declares_required_secrets() -> None:
    text = _read(".env.example")
    for key in ["OPENAI_API_KEY", "OPENAI_BASE_URL", "DATABASE_URL", "APP_SECRET_KEY"]:
        assert re.search(rf"^{key}=", text, re.MULTILINE), f"{key} missing from .env.example"


def test_gitignore_keeps_env_files_out_but_allows_example() -> None:
    lines = _read(".gitignore").splitlines()
    assert ".env" in lines
    assert "!.env.example" in lines


def test_ci_workflow_runs_on_pull_requests_and_executes_checks() -> None:
    workflow = yaml.safe_load(_read(".github/workflows/ci.yml"))
    # PyYAML parses the bare key `on` as boolean True.
    triggers = workflow.get("on", workflow.get(True))
    assert "pull_request" in triggers
    commands = " ".join(
        step.get("run", "") for job in workflow["jobs"].values() for step in job["steps"]
    )
    for tool in ["ruff check", "mypy", "pytest", "pip_audit"]:
        assert tool in commands, f"CI does not run {tool}"


def test_pytest_markers_are_registered() -> None:
    config = tomllib.loads(_read("pyproject.toml"))["tool"]["pytest"]["ini_options"]
    registered = {marker.split(":")[0] for marker in config["markers"]}
    assert set(PYTEST_MARKERS) <= registered
    assert "--strict-markers" in config["addopts"]


def test_requirements_are_pinned() -> None:
    for name in ["requirements.txt", "requirements-dev.txt"]:
        for line in _read(name).splitlines():
            line = line.strip()
            if line and not line.startswith(("#", "-r")):
                assert "==" in line, f"{name}: dependency not pinned: {line}"


def test_license_is_mit() -> None:
    assert _read("LICENSE").startswith("MIT License")
