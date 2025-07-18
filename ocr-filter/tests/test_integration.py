

import subprocess
import os
import pytest

def test_pipeline_runs_successfully():
    result = subprocess.run(
        ["poetry", "run", "python", "filter_hello_ocr/pipeline_runner.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"Pipeline failed unexpectedly.\nSTDERR:\n{result.stderr}"

def test_pipeline_fails_with_missing_video(monkeypatch):
    video_path = "example_video.mp4"
    temp_path = "example_video_backup.mp4"

    if os.path.exists(video_path):
        os.rename(video_path, temp_path)

    try:
        result = subprocess.run(
            ["poetry", "run", "python", "filter_hello_ocr/pipeline_runner.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert result.returncode != 0, "Pipeline should have failed due to missing video."
        assert "No such file or directory" in result.stderr or "error" in result.stderr.lower()
    finally:
        if os.path.exists(temp_path):
            os.rename(temp_path, video_path)