.PHONY: dev api web db-up db-migrate test lint

# Start everything
dev:
	docker compose up -d postgres redis
	@echo "Waiting for postgres..."
	@sleep 2
	cd api && uvicorn leadlocal.main:app --reload --port 8000 &
	cd web && npm run dev &

# Backend only
api:
	cd api && uvicorn leadlocal.main:app --reload --port 8000

# Frontend only
web:
	cd web && npm run dev

# Database
db-up:
	docker compose up -d postgres redis

db-migrate:
	cd api && alembic upgrade head

db-revision:
	cd api && alembic revision --autogenerate -m "$(msg)"

# Testing
test:
	cd api && python -m pytest tests/ -v --cov=leadlocal

# Linting
lint:
	cd api && ruff check src/ && ruff format --check src/

format:
	cd api && ruff check --fix src/ && ruff format src/
