.PHONY: help install dev-install test lint format clean run

help:
	@echo "AI-Powered SQL Agent - Development Commands"
	@echo "============================================"
	@echo "make install       - Install dependencies"
	@echo "make dev-install   - Install with dev dependencies"
	@echo "make test          - Run tests"
	@echo "make lint          - Run linting checks"
	@echo "make format        - Format code with Black"
	@echo "make clean         - Clean up cache files"
	@echo "make run           - Run the agent"
	@echo "make interactive   - Run interactive mode"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

test:
	pytest tests/ -v --cov=. --cov-report=html

lint:
	flake8 sql_agent.py llm_agent.py tests/

format:
	black sql_agent.py llm_agent.py tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

run:
	python sql_agent.py

interactive:
	python -c "from sql_agent import SQLAgent; agent = SQLAgent(); agent.run_interactive()"

setup-env:
	cp .env.example .env
	@echo "✅ .env file created. Please update with your credentials."

venv:
	python3.11 -m venv venv
	@echo "✅ Virtual environment created. Run: source venv/bin/activate"

