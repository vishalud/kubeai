# kubeai

[![codecov](https://codecov.io/gh/vishalud/kubeai/branch/main/graph/badge.svg)](https://codecov.io/gh/vishalud/kubeai)

A Python project for natural language-driven Kubernetes operations.

## Documentation

- [Architecture & Extensibility Guide](docs/architecture.md) – Learn about kubeai's modular design, data flow, and how to extend the CLI for new resource types, actions, and advanced NLP customization.
- [NLP Customization Guide](docs/nlp_customization.md) – Advanced guide for extending or tuning the natural language/LLM layer, adding new intents/entities, and prompt engineering.

## Setup Instructions

1. **Clone the repository and enter the project directory:**
   ```bash
   git clone git@github.com:vishalud/kubeai.git
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

Watch the latest kubeai demo:

<p align="center">
  <a href="https://youtu.be/4Wh4ZMD0HGc" target="_blank">
    <img src="https://img.youtube.com/vi/4Wh4ZMD0HGc/0.jpg" alt="Watch the demo on YouTube" width="480"/>
  </a>
</p>

<p align="center">
  <a href="https://youtu.be/4Wh4ZMD0HGc" target="_blank">▶️ Click here to watch the demo on YouTube</a>
</p>

<!-- For platforms that support it, embed the video directly: -->
<p align="center">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/4Wh4ZMD0HGc" title="kubeai demo" frameborder="0" allowfullscreen></iframe>
</p>

> Note: If you prefer, the previous MP4 demo is still available at [docs/t-rec_2.mp4](docs/t-rec_2.mp4).

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

Test coverage is also uploaded to [Codecov](https://codecov.io/gh/vishalud/kubeai) via GitHub Actions. The badge above will update automatically after each push to main.

## Notes
- Ensure you are using Python 3.8 or newer.
- The `.venv/` directory is excluded from version control via `.gitignore`. 
