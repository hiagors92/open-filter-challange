from pytest_bdd import scenario, given, when, then, parsers
import os
import subprocess
import json

@scenario('../../../features/integration_success.feature', 'Successful OCR pipeline execution')
def test_successful_pipeline():
    pass

@given("a sample video input file exists")
def video_exists():
    assert os.path.isfile("example_video.mp4")

@when("the pipeline is executed")
def run_pipeline():
    subprocess.run(["python", "pipeline_runner.py"], check=True)

@then("an OCR output file should be created")
def check_output_file():
    assert os.path.exists("output/ocr_results.json")

@then("the OCR output file should not be empty")
def check_output_not_empty():
    with open("output/ocr_results.json") as f:
        content = f.read()
        assert len(content) > 0