.PHONY: help test test-verbose test-file coverage

help:
	@echo "Available targets:"
	@echo "  test         - Run all tests (quiet)"
	@echo "  test-verbose - Run all tests with verbose output"
	@echo "  test-file    - Run a specific test file: make test-file FILE=tests/test_k8s_client.py"
	@echo "  coverage     - Run tests with coverage reporting"

# Run all tests (quiet)
test:
	PYTHONPATH=. pytest tests --disable-warnings

# Run all tests (verbose)
test-verbose:
	PYTHONPATH=. pytest tests --disable-warnings -v

# Run a specific test file: make test-file FILE=tests/test_k8s_client.py
test-file:
	PYTHONPATH=. pytest $(FILE) --disable-warnings -v

# Run coverage
coverage:
	PYTHONPATH=. pytest --cov=src tests 