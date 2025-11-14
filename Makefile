# DevOps Project Makefile
# Quick commands for development and testing

.PHONY: help install test lint format security docker-up docker-down docker-logs clean

# Default target
help:
	@echo "DevOps Project - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install          Install all dependencies"
	@echo "  make test            Run unit tests"
	@echo "  make test-integration Run integration tests"
	@echo "  make test-all        Run all tests with coverage"
	@echo "  make lint            Run linting checks"
	@echo "  make format          Format code with black"
	@echo "  make security        Run security scans"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up       Start all Docker services"
	@echo "  make docker-down     Stop all Docker services"
	@echo "  make docker-logs     View Docker logs"
	@echo "  make docker-ps       Show running containers"
	@echo "  make docker-clean    Remove all containers and volumes"
	@echo ""
	@echo "CI/CD:"
	@echo "  make ci              Run all CI checks locally"
	@echo "  make pre-commit      Install pre-commit hooks"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Clean temporary files"

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r scripts/python/requirements.txt
	pip install pytest pytest-cov flake8 black pylint safety bandit pre-commit requests

# Run unit tests
test:
	cd scripts/python && pytest tests/test_health_checker.py -v

# Run integration tests
test-integration:
	cd scripts/python && pytest tests/test_integration.py -v -m integration

# Run all tests with coverage
test-all:
	cd scripts/python && pytest tests/ -v --cov=. --cov-report=term --cov-report=html

# Run linting
lint:
	flake8 scripts/python --max-line-length=100
	pylint scripts/python/*.py --exit-zero

# Format code
format:
	black scripts/python --line-length=100
	isort scripts/python

# Security scans
security:
	safety check
	bandit -r scripts/python -f screen

# Start Docker stack
docker-up:
	cd docker && docker-compose -f docker-compose-monitoring.yml up -d
	@echo "Waiting for services to start..."
	@sleep 10
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Stop Docker stack
docker-down:
	cd docker && docker-compose -f docker-compose-monitoring.yml down

# View Docker logs
docker-logs:
	cd docker && docker-compose -f docker-compose-monitoring.yml logs -f

# Show running containers
docker-ps:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Clean Docker (remove volumes)
docker-clean:
	cd docker && docker-compose -f docker-compose-monitoring.yml down -v
	docker system prune -f

# Run all CI checks locally
ci: lint test security
	@echo "All CI checks passed!"

# Install pre-commit hooks
pre-commit:
	pre-commit install
	@echo "Pre-commit hooks installed!"

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage coverage.xml
	@echo "Cleaned temporary files!"
