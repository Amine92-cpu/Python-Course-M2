.PHONY: install test lint build integration-test up down logs dev help

PYTHON  = python
PYTEST  = pytest
PIP     = pip

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all Python dependencies
	$(PIP) install --no-cache-dir -r requirements.txt

lint:  ## Run flake8 linter on api/, dashboard/, tests/
	flake8 api/ dashboard/ tests/ --max-line-length=100

test:  ## Run unit tests with coverage (must be >= 75%)
	$(PYTEST) tests/test_metrics.py tests/test_routes.py \
		-v --cov=api --cov-report=term-missing --cov-fail-under=75

build:  ## Build Docker images locally (no push)
	docker compose build

integration-test:  ## Start the API container and run integration tests
	@echo "Starting API container for integration tests..."
	API_KEY=test-secret-key docker compose up -d api
	@echo "Waiting for API to be healthy..."
	@sleep 5
	INT_BASE_URL=http://localhost:8000 API_KEY=test-secret-key \
		$(PYTEST) tests/test_integration.py -v
	@echo "Tearing down..."
	docker compose down -v

up:  ## Start the full stack (API + Dashboard) in background
	docker compose up --build -d

down:  ## Stop and remove containers and volumes
	docker compose down -v

logs:  ## Follow logs of all services
	docker compose logs -f

dev:  ## Run API locally without Docker (for development)
	API_KEY=dev-secret-key uvicorn api.main:app --reload --port 8000
