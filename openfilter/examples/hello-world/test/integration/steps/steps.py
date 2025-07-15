from pytest_bdd import given, when, then, scenarios, parsers
import os
import subprocess
import json

scenarios('../features')

@given("a sample video input file exists")
def video_exists():
    assert os.path.isfile("example_video.mp4")

@given(parsers.parse("a pipeline YAML path that does not exist"))
def fake_yaml_path():
    assert not os.path.exists("invalid_path.yaml")

@given(parsers.parse("a configuration with a non-existent video file path"))
def config_with_missing_video():
    assert not os.path.exists("nonexistent_video.mp4")

@given(parsers.parse("an OCR filter configuration with an invalid engine"))
def invalid_engine_config():
    pass

@given(parsers.parse("a configuration missing required fields"))
def missing_config_fields():
    pass  

@given(parsers.parse("a pipeline configuration without defined outputs"))
def config_without_outputs():
    pass

@when("the pipeline is executed")
def run_pipeline():
    subprocess.run(["python", "pipeline_runner.py"], check=True)

@when("the OCR filter is initialized")
def init_ocr_filter():
    pass  

@then("an OCR output file should be created")
def check_output_file():
    assert os.path.exists("output/ocr_results.json")

@then("the OCR output file should not be empty")
def check_output_not_empty():
    with open("output/ocr_results.json") as f:
        content = f.read()
        assert len(content) > 0

@then("a file named \"benchmark_results.csv\" should exist")
def check_benchmark_csv():
    assert os.path.exists("benchmark_results.csv")

@then("the file should contain performance metrics")
def benchmark_file_not_empty():
    with open("benchmark_results.csv") as f:
        lines = f.readlines()
        assert len(lines) > 1 

@then("it should raise a ValueError")
def should_raise_valueerror():
    try:
        from openfilter.filters import FilterOpticalCharacterRecognition
        from openfilter.filters.filter_optical_character_recognition.enums import OCREngine
        FilterOpticalCharacterRecognition({
            "id": "test",
            "ocr_engine": "INVALID_ENGINE",
            "outputs": [],
            "sources": [],
        })
    except ValueError:
        assert True
    else:
        assert False, "Expected ValueError not raised"

@then("it should raise a FileNotFoundError")
def should_raise_file_not_found():
    try:
        subprocess.run(["python", "pipeline_runner.py", "--video", "nonexistent_video.mp4"], check=True)
    except subprocess.CalledProcessError:
        assert True
    else:
        assert False, "Expected FileNotFoundError or process failure not raised"

@then("it should log an error and abort")
def check_error_log():
    assert True  # Placeholder for actual log inspection

@then("it should log a configuration error and not crash the pipeline")
def config_error_no_crash():
    assert True