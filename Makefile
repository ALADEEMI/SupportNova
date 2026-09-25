# SupportNova developer commands (CLAUDE.md section 9).
# Works with GNU make on Linux/macOS and with mingw32-make / GNU make on Windows.
# Override the bootstrap interpreter if needed, e.g.:  make setup PYTHON="py -3.12"

PYTHON ?= python

ifeq ($(OS),Windows_NT)
SHELL := cmd.exe
VENV_PY := .venv\Scripts\python.exe
else
VENV_PY := .venv/bin/python
endif

.PHONY: help setup lint format typecheck test check audit seed run api eval-holdout

help:
	@echo Targets: setup seed run api test check lint format typecheck audit eval-holdout

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements-dev.txt
	$(VENV_PY) -m pre_commit install

lint:
	$(VENV_PY) -m ruff check .
	$(VENV_PY) -m ruff format --check .

format:
	$(VENV_PY) -m ruff format .
	$(VENV_PY) -m ruff check --fix .

typecheck:
	$(VENV_PY) -m mypy .

test:
	$(VENV_PY) -m pytest -m "not live_llm" --cov --cov-report=term

check: lint typecheck test

audit:
	$(VENV_PY) -m pip_audit -r requirements.txt

seed:
	$(VENV_PY) -m alembic upgrade head
	$(VENV_PY) -m database.seeders

run:
	$(VENV_PY) -m streamlit run src/app/Home.py

api:
	$(VENV_PY) -m uvicorn src.api.main:app --reload

eval-holdout:
	$(VENV_PY) scripts/eval/run_holdout_eval.py
