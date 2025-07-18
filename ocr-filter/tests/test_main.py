import pytest
from unittest.mock import patch, MagicMock
import importlib

import filter_hello_ocr.main as main_module


def test_run_multi_called_with_correct_filters(monkeypatch):
    mock_run_multi = MagicMock()
    monkeypatch.setattr(main_module.Filter, 'run_multi', mock_run_multi)

    monkeypatch.setattr(main_module, '__name__', '__main__')
    importlib.reload(main_module)

    assert mock_run_multi.called
    args, _ = mock_run_multi.call_args
    filters = args[0]
    assert isinstance(filters, list)
    assert len(filters) == 3

    video_in_cls, video_in_kwargs = filters[0]
    assert video_in_cls == main_module.VideoIn
    assert isinstance(video_in_kwargs, dict)
    assert video_in_kwargs["id"] == "VideoIn"
    assert video_in_kwargs["outputs"] == ["tcp://*:5550"]
    assert video_in_kwargs["sources"][0]["source"] == "file://example_video.mp4"
    assert video_in_kwargs["sources"][0]["options"]["loop"] is True

    ocr_cls, ocr_kwargs = filters[1]
    assert ocr_cls == main_module.FilterOpticalCharacterRecognition
    assert ocr_kwargs["id"] == "OCRFilter"
    assert ocr_kwargs["sources"] == ["tcp://localhost:5550"]
    assert ocr_kwargs["outputs"] == ["tcp://*:5552"]
    assert ocr_kwargs["ocr_engine"] == "easyocr"
    assert ocr_kwargs["forward_ocr_texts"] is True

    webvis_cls, webvis_kwargs = filters[2]
    assert webvis_cls == main_module.Webvis
    assert webvis_kwargs["id"] == "Webvis"
    assert webvis_kwargs["sources"] == ["tcp://localhost:5552"]