from pytest_bdd import given, when, then, scenarios, parsers
import os
import subprocess
import json
import yaml
import tempfile
from contextlib import contextmanager

# Load scenarios from the features directory
scenarios('../features')

# --- Fixtures and Helper Functions ---

@contextmanager
def create_temp_config(config_data):
    """Creates a temporary YAML configuration file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".yaml") as f:
        yaml.dump(config_data, f)
    try:
        yield f.name
    finally:
        os.unlink(f.name)

# --- Given Steps ---

@given("a sample video input file exists")
def video_exists():
    assert os.path.isfile("example_video.mp4"), "example_video.mp4 must exist for tests to run."

@given(parsers.parse("a pipeline YAML path that does not exist"))
def fake_yaml_path():
    invalid_path = "invalid_path.yaml"
    assert not os.path.exists(invalid_path)
    return invalid_path

@given(parsers.parse("a configuration with a non-existent video file path"))
def config_with_missing_video():
    config_data = {
        "filters": [
            {
                "id": "video_in_filter",
                "filter_type": "VideoIn",
                "inputs": [
                    "file://nonexistent_video.mp4" 
                ],
                "outputs": ["video_stream"]
            }
        ]
    }
    return config_data

@given(parsers.parse("an OCR filter configuration with an invalid engine"))
def invalid_engine_config():
    config_data = {
        "id": "test_ocr_filter",
        "filter_type": "FilterOpticalCharacterRecognition",
        "ocr_engine": "INVALID_ENGINE_NAME", 
        "inputs": ["video_stream"],
        "outputs": ["ocr_results"]
    }
    return config_data

@given(parsers.parse("a configuration missing required fields"))
def missing_config_fields():
    config_data = {
        "id": "test_missing_fields_filter",
        "filter_type": "FilterOpticalCharacterRecognition",
        "ocr_engine": "tesseract",
        "inputs": ["video_stream"],
        # 'outputs' field is intentionally missing
    }
    return config_data

@given(parsers.parse("a pipeline configuration without defined outputs"))
def config_without_pipeline_outputs():
    config_data = {
        "filters": [
            {
                "id": "video_in_filter",
                "filter_type": "VideoIn",
                "inputs": ["file://example_video.mp4"],
                "outputs": ["video_stream"]
            },
            {
                "id": "ocr_filter",
                "filter_type": "FilterOpticalCharacterRecognition",
                "ocr_engine": "tesseract",
                "inputs": ["video_stream"],
                "outputs": [] # No outputs specified for the filter or pipeline
            }
        ]
    }
    return config_data


# --- When Steps ---

@when(parsers.parse("the pipeline is executed with config {config_type}"))
@when("the pipeline is executed")
def run_pipeline(config_type=None, config_with_missing_video=None, fake_yaml_path=None):
    """
    Executes the pipeline, potentially with a specific configuration.
    It can now receive context from given steps.
    """
    cmd = ["python", "pipeline_runner.py"]
    temp_config_path = None

    if config_type == "missing video":
        with create_temp_config(config_with_missing_video) as path:
            temp_config_path = path
            cmd.extend(["--config", temp_config_path])
    elif config_type == "non-existent YAML path":
        cmd.extend(["--config", fake_yaml_path])
    elif config_type == "without defined outputs":
        with create_temp_config(config_without_pipeline_outputs) as path:
            temp_config_path = path
            cmd.extend(["--config", temp_config_path])


    print(f"\nRunning command: {' '.join(cmd)}")
    process = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if not hasattr(run_pipeline, 'last_process_result'):
        run_pipeline.last_process_result = {}
    run_pipeline.last_process_result['stdout'] = process.stdout
    run_pipeline.last_process_result['stderr'] = process.stderr
    run_pipeline.last_process_result['returncode'] = process.returncode
    print(f"STDOUT:\n{process.stdout}")
    print(f"STDERR:\n{process.stderr}")

@when("the OCR filter is initialized")
def init_ocr_filter(invalid_engine_config=None, missing_config_fields=None):
    """
    Initializes the OCR filter with a given configuration.
    This step now receives the problematic configuration from 'given' steps.
    """
    from openfilter.filter_optical_character_recognition.filter import FilterOpticalCharacterRecognition
    from openfilter.filter_optical_character_recognition.filter import OCREngine

    filter_config = None
    if invalid_engine_config:
        filter_config = invalid_engine_config
    elif missing_config_fields:
        filter_config = missing_config_fields
    else:
        filter_config = {
            "id": "default_ocr_filter",
            "filter_type": "FilterOpticalCharacterRecognition",
            "ocr_engine": "tesseract", # or 'easyocr'
            "inputs": ["video_stream"],
            "outputs": ["ocr_results"]
        }
    
    try:
        init_ocr_filter.filter_instance = FilterOpticalCharacterRecognition(filter_config)
        init_ocr_filter.exception = None
    except (ValueError, TypeError) as e:
        init_ocr_filter.filter_instance = None
        init_ocr_filter.exception = e

# --- Then Steps ---

@then("an OCR output file should be created")
def check_output_file():
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    assert os.path.exists(os.path.join(output_dir, "ocr_results.json"))

@then("the OCR output file should not be empty")
def check_output_not_empty():
    with open("output/ocr_results.json", 'r') as f:
        content = f.read()
        assert len(content) > 0, "OCR results file is empty"
        try:
            json_content = json.loads(content)
            assert isinstance(json_content, list) or isinstance(json_content, dict), "OCR results not valid JSON structure"
        except json.JSONDecodeError:
            assert False, "OCR results file is not valid JSON"

@then("a file named \"benchmark_results.csv\" should exist")
def check_benchmark_csv():
    assert os.path.exists("benchmark_results.csv")

@then("the file should contain performance metrics")
def benchmark_file_not_empty():
    with open("benchmark_results.csv", 'r') as f:
        lines = f.readlines()
        assert len(lines) > 1, "Benchmark results file is empty or only contains header"
        assert "timestamp" in lines[0] and "cpu_percent" in lines[0] and "memory_percent" in lines[0], \
            "Benchmark CSV header missing expected columns"

@then("it should raise a ValueError")
def should_raise_valueerror():
    assert init_ocr_filter.exception is not None, "Expected ValueError was not raised"
    assert isinstance(init_ocr_filter.exception, ValueError), f"Expected ValueError, but got {type(init_ocr_filter.exception)}"
    assert "Invalid OCR engine specified" in str(init_ocr_filter.exception) or \
           "is not a valid OCREngine" in str(init_ocr_filter.exception), \
           f"ValueError message not as expected: {init_ocr_filter.exception}"

@then("it should raise a TypeError") 
def should_raise_typeerror():
    assert init_ocr_filter.exception is not None, "Expected TypeError was not raised"
    assert isinstance(init_ocr_filter.exception, TypeError), f"Expected TypeError, but got {type(init_ocr_filter.exception)}"

@then("it should log an error and abort")
def check_error_log_and_abort():
    process_result = run_pipeline.last_process_result
    assert process_result['returncode'] != 0, "Pipeline did not abort (return code was 0)"
    assert "Error" in process_result['stderr'] or "Failed" in process_result['stderr'], \
           f"Error message not found in stderr: {process_result['stderr']}"
    if "nonexistent_video.mp4" in process_result['stderr'] or "No such file or directory" in process_result['stderr']:
        assert True
    elif "No such file or directory: 'invalid_path.yaml'" in process_result['stderr']:
        assert True
    else:
        assert False, f"Unexpected error content in stderr: {process_result['stderr']}"

@then("it should log a configuration error and not crash the pipeline")
def config_error_no_crash():
    process_result = run_pipeline.last_process_result
    assert process_result['returncode'] == 0, "Pipeline crashed when it should not have"
    assert "Configuration error" in process_result['stderr'] or "Warning" in process_result['stderr'], \
           f"Expected configuration error/warning not found in stderr: {process_result['stderr']}"
    assert not os.path.exists("output/ocr_results.json") 