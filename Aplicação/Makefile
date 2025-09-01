.PHONY: help dev test lint format clean build up down logs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment
	docker compose up --build

test: ## Run tests with coverage
	cd backend && python -m pytest

cov: ## Run tests with coverage and generate HTML report
	cd backend && python -m pytest -v -s --cov=app --cov-report=term-missing --cov-report=html

cov-open: ## Open HTML coverage report in default browser
	cd backend && python -c "import webbrowser; webbrowser.open('htmlcov/index.html')"

test-watch: ## Run tests in watch mode
	cd backend && python -m pytest --watch

lint: ## Run linting checks
	cd backend && python -m ruff check app/
	cd backend && python -m ruff format --check app/

format: ## Format code with ruff
	cd backend && python -m ruff format app/
	cd backend && python -m ruff check --fix app/

clean: ## Clean up containers and volumes
	docker compose down -v
	docker system prune -f

build: ## Build Docker images
	docker compose build

up: ## Start services
	docker compose up -d

down: ## Stop services
	docker compose down

logs: ## Show service logs
	docker compose logs -f

logs-backend: ## Show backend logs
	docker compose logs -f backend

logs-frontend: ## Show frontend logs
	docker compose logs -f frontend

logs-db: ## Show database logs
	docker compose logs -f db

shell-backend: ## Open shell in backend container
	docker compose exec backend /bin/bash

shell-db: ## Open shell in database container
	docker compose exec db psql -U pmapp -d pmdb

migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

migrate-create: ## Create new migration
	docker compose exec backend alembic revision --autogenerate -m "$(message)"

health: ## Check API health
	curl -f http://localhost:8000/health || echo "API not healthy"
	curl -f http://localhost:5173 || echo "Frontend not healthy"
