# kubeai

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

## Notes
- Ensure you are using Python 3.8 or newer.
- The `.venv/` directory is excluded from version control via `.gitignore`. 