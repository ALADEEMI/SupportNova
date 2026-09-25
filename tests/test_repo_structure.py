"""Repository layout required by SRS Deliverable 2 (Source Code) and CLAUDE.md section 4."""

from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[1]

MANDATORY_FILES = ["README.md", "AI_USAGE.md", "requirements.txt", "LICENSE"]

MANDATORY_DIRS = [
    "src",
    "templates",
    "static",
    "complaint_processing",
    "document_processing",
    "knowledge_base",
    "genai_pipeline",
    "python_validation",
    "complaint_rules",
    "routing_rules",
    "escalation_rules",
    "prompt_templates",
    "schemas",
    "comparison_engine",
    "hallucination_checks",
    "security",
    "database",
    "tests",
    "sample_complaints",
    "sample_documents",
    "hidden_test_ready",
    "documentation",
    "screenshots",
    "reports",
    "config",
]

PYTHON_PACKAGES = [
    "src",
    "src/app",
    "src/core",
    "src/services",
    "src/api",
    "complaint_processing",
    "document_processing",
    "knowledge_base",
    "genai_pipeline",
    "python_validation",
    "comparison_engine",
    "hallucination_checks",
    "security",
    "database",
]


def test_srs_deliverable_2_lists_exactly_29_mandatory_paths() -> None:
    assert len(MANDATORY_FILES) + len(MANDATORY_DIRS) == 29


@pytest.mark.parametrize("name", MANDATORY_FILES)
def test_mandatory_file_exists(name: str) -> None:
    path = REPO_ROOT / name
    assert path.is_file(), f"Missing mandatory file: {name}"
    assert path.stat().st_size > 0, f"Mandatory file is empty: {name}"


@pytest.mark.parametrize("name", MANDATORY_DIRS)
def test_mandatory_directory_exists_and_is_tracked(name: str) -> None:
    path = REPO_ROOT / name
    assert path.is_dir(), f"Missing mandatory directory: {name}/"
    assert any(p.is_file() for p in path.rglob("*")), f"{name}/ has no files, so git would drop it"


@pytest.mark.parametrize("name", PYTHON_PACKAGES)
def test_code_directory_is_an_importable_package(name: str) -> None:
    assert (REPO_ROOT / name / "__init__.py").is_file(), f"{name}/ is missing __init__.py"
