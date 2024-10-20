.PHONY: dev run lint format

run:
	uv run fastapi run ./src/main.py

dev:
	uv run fastapi dev ./src/main.py

lint:
	uv run ruff check ./src

format:
	uv run ruff format ./src
