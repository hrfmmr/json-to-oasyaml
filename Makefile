VENV := .venv
poetry-run := poetry run

.PHONY: default
default: bootstrap

.PHONY: bootstrap
bootstrap:
	poetry install

.PHONY: run
run:
	@$(poetry-run) python main.py
