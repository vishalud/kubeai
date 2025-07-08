# kubeai

[![codecov](https://app.codecov.io/gh/vishalud/kubeai/branch/main/graph/badge.svg)](https://codecov.io/gh/vishalud/kubeai)

A Python project for natural language-driven Kubernetes operations.

## Setup Instructions

1. **Clone the repository and enter the project directory:**
   ```bash
   git clone <repo-url>
   cd kubeai
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Directory Structure:**
   - `src/` – Main application code
   - `tests/` – Unit tests
   - `docs/` – Documentation

5. **Verify installation:**
   ```bash
   python -c "import pydantic; import kubernetes; import google.generativeai"
   ```

## Demo

See kubeai in action:

![kubeai demo](docs/t-rec_1.gif)

This demo shows the CLI responding to natural language Kubernetes queries, including listing pods and summarizing their status using Gemini-powered NLP.

## Running Tests

You can run the test suite using the provided Makefile.

- **Run all tests (quiet):**
  ```bash
  make test
  ```

- **Run all tests (verbose):**
  ```bash
  make test-verbose
  ```

- **Run a specific test file:**
  ```bash
  make test-file FILE=tests/test_k8s_client.py
  ```

- **Show all available Makefile targets:**
  ```bash
  make help
  ```

- **Run coverage and see a local report:**
  ```bash
  make coverage
  ```

Test coverage is also uploaded to [Codecov](https://codecov.io/gh/<your-username>/<your-repo>) via GitHub Actions. The badge above will update automatically after each push to main.

## Notes
- Ensure you are using Python 3.8 or newer.
- The `.venv/` directory is excluded from version control via `.gitignore`. 