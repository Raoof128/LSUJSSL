.PHONY: help install install-dev test test-cov clean run-legit run-attack run-demo telemetry report format lint type-check quality-check all

help:
	@echo "LEO Satellite Simulation Lab - Makefile Commands"
	@echo "======================================================="
	@echo "Setup & Installation:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run test suite"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Run flake8 linting"
	@echo "  make type-check    - Run mypy type checking"
	@echo "  make quality-check - Run all quality checks (format + lint + type)"
	@echo ""
	@echo "Simulation:"
	@echo "  make run-demo      - Run full demo script"
	@echo "  make run-legit     - Send legitimate command"
	@echo "  make run-attack    - Simulate rogue attack"
	@echo "  make telemetry     - View telemetry logs"
	@echo "  make report        - Export security report"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         - Remove generated files"
	@echo "  make all           - Run quality checks + tests"

install:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

install-dev: install
	. venv/bin/activate && pip install -r requirements-dev.txt

test:
	. venv/bin/activate && python -m pytest tests/ -v

test-cov:
	. venv/bin/activate && python -m pytest tests/ -v --cov=satellite_sim --cov-report=html --cov-report=term

run-demo:
	. venv/bin/activate && python demo.py

run-legit:
	. venv/bin/activate && python -m satellite_sim.cli.sat_cli send --station legit --cmd "ADJUST_THRUST"

run-attack:
	. venv/bin/activate && python -m satellite_sim.cli.sat_cli send --station rogue --cmd "SHUTDOWN_REACTOR" --attack-type BAD_SIGNATURE

telemetry:
	. venv/bin/activate && python -m satellite_sim.cli.sat_cli watch-telemetry

report:
	. venv/bin/activate && python -m satellite_sim.cli.sat_cli export-report

clean:
	rm -rf __pycache__ .pytest_cache *.log *.json venv htmlcov .coverage
	rm -rf satellite_sim.egg-info dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

format:
	. venv/bin/activate && black satellite_sim/ tests/ demo.py

lint:
	. venv/bin/activate && flake8 satellite_sim/ tests/

type-check:
	. venv/bin/activate && mypy satellite_sim/

quality-check: format lint type-check
	@echo "✅ All quality checks passed!"

all: quality-check test
	@echo "✅ All checks and tests passed!"
