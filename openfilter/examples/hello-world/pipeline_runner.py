import sys
import os

from openfilter.filter_runtime.filter import Filter
from openfilter.filter_runtime.filters.video_in import VideoIn
from openfilter.examples.hello_ocr.filter_hello_ocr.main import FilterOpticalCharacterRecognition
from openfilter.filter_runtime.filters.webvis import Webvis

if __name__ == "__main__":
    try:
        Filter.run_multi([
            (VideoIn, {
                "id": "VideoIn",
                "outputs": ["tcp://*:5550"],
                "sources": [{
                    "source": "file://example_video.mp4",
                    "topic": "main",
                    "options": {"loop": True}
                }]
            }),
            (FilterOpticalCharacterRecognition, {
                "id": "OCRFilter",
                "sources": ["tcp://localhost:5550"],
                "outputs": ["tcp://*:5552"],
                "ocr_engine": "easyocr",
                "forward_ocr_texts": True
            }),
            (Webvis, {
                "id": "Webvis",
                "sources": ["tcp://localhost:5552"]
            })
        ])
    except Exception as e:
        print(f"[ERRO]: {e}")