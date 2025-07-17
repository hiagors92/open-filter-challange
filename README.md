# OpenFilter Practical Challenge – OCR Pipeline Benchmark

This repository presents the solution to the OpenFilter practical challenge, focused on building, testing, and benchmarking a modular OCR pipeline using the OpenFilter framework.

## Context

This project is part of a practical assessment aimed at evaluating technical skills in:

- Integrating and configuring OpenFilter pipelines
- Benchmarking OCR filters
- Identifying architectural and usability improvements
- Designing and validating test strategies

## Initial Observations

During initial setup and exploration, a few challenges and inconsistencies were found:

- **Installation:** Required `pip install openfilter[all]` to install all dependencies. The standard command failed without the `[all]` flag.
- **Python Version:** The project is not compatible with Python 3.13.3; Python 3.12 worked without issues.
- **Conflicts in Dependencies:** The `requirements.txt` in `examples/hello-ocr` led to conflicts that needed manual adjustments.
- **README Gaps:** The root `README.md` lacked clarity. The execution instructions were only functional when explored inside example folders.
- **File Reference Bug:** In `examples/hello-world`, the code looks for `video.mp4`, but the correct file is `example_video.mp4`.

## Code and Documentation Feedback

- Presence of redundant or commented-out code fragments.
- Classes and functions were sometimes overloaded with responsibilities.
- Lack of encapsulation and error handling in key areas.
- Documentation is detailed but lacks consistent architectural standards, DoR (Definition of Ready) and DoD (Definition of Done) artifacts.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/hiagors/open-filter-challenge.git
cd open-filter-challenge
```

2. Create and activate a virtual environment (Python 3.12 recommended):
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install openfilter'[all]'
```

4. (Optional) Install additional tools for benchmarking and testing:
```bash
pip install pytest memory_profiler
```

## Chosen Filter and Pipeline Overview

The selected pipeline is based on the OCR filter available in `examples/hello-ocr`. The structure includes:

- `VideoIn`: loads and loops a sample video
- `FilterOpticalCharacterRecognition`: extracts text using EasyOCR
- `Webvis`: renders output in a local browser interface

## How to Run

### CLI Execution (recommended)
```bash
openfilter run examples/hello-ocr/pipeline.yaml [TODO]
```

### Script Execution
```bash
python script.py --video example_video.mp4 --loop --loop_duration 300
```

### Programmatic Execution
```python
from openfilter import Filter
Filter.run_multi(["examples/hello-ocr/pipeline.yaml"]) [TODO]
```

## Output and Metrics

Upon successful execution:

- Filter results are saved to: `./output/ocr_results.json`
- Benchmark data is saved to: `./benchmark_results.csv`
- You can visualize output in your browser via Webvis at: `http://localhost:8000`

## Tests [TODO]

### Unit Tests [TODO]
Run unit tests to validate filter behavior:
```bash
pytest tests/unit/
```

### Integration Tests [TODO]
Run full pipeline validation:
```bash
pytest tests/integration/
```

Test coverage includes:
- Stream start/stop behavior
- Output file generation and structure
- Filter accuracy against expected results

## Definitions

### Definition of Ready (DoR)
- Filters and dependencies are identified
- Environment is fully operational
- Inputs, outputs, and metrics are defined

### Definition of Done (DoD)
- Pipeline executes end-to-end with expected output
- Metrics are logged and saved correctly
- Results are visualized and exported
- Errors are handled gracefully
- Code follows modular and readable structure

## Current Status Update

Significant progress has been made on the OCR pipeline integration. The **OCR Filter** has been successfully selected and fully integrated, producing expected outputs and persisting results correctly. Recent executions confirm that the pipeline is functional and stable:

* `2025-07-14 02:30:46.542 34620 INFO Saved subject data to ./output/subject_data.json`
* `2025-07-14 02:30:46.542 34620 INFO OCR Filter shutting down. Processed data saved at ./output/ocr_results.json`

To run the current pipeline, navigate to `openfilter/examples/hello-world` and execute:

```bash
python pipeline_runner.py
```

## Current Development Status

### Isolated OCR Environment
- Established a dedicated directory `ocr-filter/` to separate experimental OCR logic and tests.
  - Includes `script.py`, `pipeline_runner.py`, and corresponding test directories.
  - Introduced `poetry` for dependency management via `pyproject.toml`.

### Poetry-Based Project Conversion
- Migrated OpenFilter project structure to use `poetry` for consistent dependency resolution.
- Installed and configured essential tools: `pytest`, `pytest-bdd`, `memory_profiler`, and others.
- Locked dependencies and resolved conflicts previously introduced by `requirements.txt`.

### Test Refactor (In Progress)
- Unified BDD test structure under `ocr-filter/tests/integration/`, consolidating:
  - `.feature` files
  - `steps.py`
  - `test_pipeline.py`
- Refactored path handling using `pathlib` to ensure compatibility across different operating systems.
- Removed duplicate or broken tests and standardized naming conventions.
- [Pending]: Full BDD test integration to improve clarity and usability for new contributors.
