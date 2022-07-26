default: help
.PHONY: help

help: ## Prints the list of all available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install-lint: ## Install test dependencies
	pip install -r requirements-lint.txt

format: install-lint ## Run formatter
	black src tests

lint: install-lint ## Run linter
	flake8
	black --check src tests

sa:  ## Run static analysis
	pip install .
	pip install -r requirements-type-check.txt
	mypy --install-types --config-file mypy.ini src | mypy-baseline filter

sa-baseline:  ## Baseline static analysis
	pip install .
	pip install -r requirements-type-check.txt
	mypy --install-types --config-file mypy.ini src | mypy-baseline sync
