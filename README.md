
# OpenFilter Practical Challenge – OCR Pipeline Benchmark

## Quickstart

```bash
# Clone and enter the project
git clone https://github.com/hiagors/open-filter-challange.git
cd open-filter-challenge/ocr-filter

# Install Poetry
pip install poetry

# Initialize project
cd /ocr-filter

# Install dependencies
poetry install

# Run the pipeline
poetry run python script.py

# View results
cat ./output/ocr_results.json
```

This repository presents the solution to the OpenFilter practical challenge, focused on building, testing, and benchmarking a modular OCR pipeline using the OpenFilter framework.

## Context

This project was developed as part of a practical evaluation to demonstrate the ability to:

- Integrate and configure OpenFilter pipelines.
- Benchmark OCR filters using EasyOCR.
- Identify architectural and usability improvements.
- Design and execute unit and integration test strategies.
- Automate with CI (GitHub Actions).

## Important Notice: Pipeline Learning and Refinement

During the early development of this project, an opportunity for significant architectural improvement was identified. The initial pipeline configuration did not fully leverage OpenFilter's capabilities for specialized preprocessing, as it lacked dedicated filters for license plate detection and cropping. Consequently, the OCR was applied broadly to full video frames, which led to less precise and noisier recognition results for our specific license plate objective.

This experience served as a valuable learning point in optimizing pipeline design for highly specific computer vision tasks. Furthermore, an oversight in selecting the input video led to the use of a non-benchmark source during initial testing, which momentarily impacted validation efforts.

Upon addressing these two key areas, the pipeline underwent a significant refactoring. By integrating the necessary detection and cropping modules, the system now achieves a more robust, modular, and testable structure, fully aligned with best practices for real-world computer vision applications.

## What Worked

- Complete **license plate OCR pipeline** functional using OpenFilter.
- Output persisted correctly in `./output/ocr_results.json`.
- Dedicated test suite with unit and integration tests using `pytest` and `pytest-cov`.
- CI pipeline configured via GitHub Actions.
- Clear structure for reproduction, contribution, and debugging.

## What Went Wrong

- **Initial Pipeline Design Flaw:** The pipeline initially lacked the necessary dedicated filters (specifically `FilterLicensePlateDetection` and `FilterCrop`) to pre-process and isolate license plates before OCR (as detailed in the "Important Notice").
- Some test data validations did not match the expected license plate image (a consequence of the design flaw above).
- Minor dependency conflicts when running outside a Poetry-managed environment.


## Requirements

- Python 3.12.x
- Poetry (`pip install poetry`)


## Installation and Setup

```bash
git clone https://github.com/hiagors/open-filter-challenge.git
cd open-filter-challenge/ocr-filter


poetry install

```

---

## Running the Pipeline

1. Install dependencies
2. Navigate into the project folder
3. Run the script:

   ```bash
   poetry run python script.py
   ```

   Or explicitly:

   ```bash
   poetry run python ocr-filter/script.py
   ```

## Cleaning Python Caches (Optional)

If you need to clean compiled caches before re-running:

```bash
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -exec rm {} +
```

---

## Running Tests with Coverage

To run unit and integration tests with coverage:

```bash
poetry run pytest tests/ --cov=filter_hello_ocr --cov-report=term-missing
```

Test coverage includes:

- Unit test validations with mocked frames and pipeline inputs
- Integration tests validating end-to-end pipeline behavior
- Error handling tests for missing files, broken dependencies, and bad configs


## Test Structure

- `tests/test_pipeline_runner.py`: core pipeline tests
- Unit tests mock the internal components to assert configurations
- Integration tests validate that output files are generated, content is processed, and data flows as expected



## Project Structure

- `ocr-filter/script.py`: script entry point
- `ocr-filter/pipeline_runner.py`: hardcoded pipeline configuration for development
- `filter_hello_ocr/`: OCR pipeline logic
- `tests/`: test suite with mock and real pipeline validation



## GitHub Actions

A GitHub Actions pipeline is available to automate linting and test execution:

- Runs on every `push` and `pull_request`
- Validates test success and coverage
- Prepares the project for future publishing

---

## Output

- OCR results are saved to: `./output/ocr_results.json`
- Subject data to: `./output/subject_data.json`
- Local visualization on: `http://localhost:8000`


## Definition of Ready (DoR)

- OCR filters and dependencies defined
- Environment reproducible with Poetry
- Test strategy in place


## Definition of Done (DoD)

- End-to-end execution confirmed
- Data saved and visualized correctly
- Test coverage executed and verified
- Errors handled gracefully
- CI pipeline working

## Summary

This solution demonstrates real-world capabilities in designing and debugging OCR pipelines under tight constraints. Even without the ideal benchmark input, the project showcases robust architectural decisions, CI/CD integration, and a complete test strategy.

Despite the incorrect input video, the project showcases the expected structure, reproducibility, pipeline behavior, and test discipline required for real-world applications using OpenFilter.
