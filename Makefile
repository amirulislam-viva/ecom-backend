-include ../.env
BACKEND_PORT ?= 8000

.PHONY: setup up migrations migrate

setup:
	@echo "Setting up backend..."
	uv sync
	uv run alembic upgrade head
	uv run python furnish.py
	@echo "Setup complete."

up:
	@echo "Starting server on port $(BACKEND_PORT)..."
	uv run uvicorn main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

migrations:
	uv run alembic revision --autogenerate -m "$(m)"

migrate:
	uv run alembic upgrade head
