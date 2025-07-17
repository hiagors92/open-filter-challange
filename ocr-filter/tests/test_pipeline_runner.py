import sys
import pytest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[0]))

@pytest.fixture(autouse=True)
def patch_imports(monkeypatch):
    video_in = mock.Mock()
    webvis = mock.Mock()
    ocr_filter = mock.Mock()
    filter_cls = mock.Mock() 

    filter_cls.run_multi = mock.Mock() 

    monkeypatch.setitem(sys.modules, "openfilter.filter_runtime.filters.video_in", mock.Mock(VideoIn=video_in))
    monkeypatch.setitem(sys.modules, "openfilter.filter_runtime.filters.webvis", mock.Mock(Webvis=webvis))
    monkeypatch.setitem(sys.modules, "filter_optical_character_recognition.filter", mock.Mock(FilterOpticalCharacterRecognition=ocr_filter))
    monkeypatch.setitem(sys.modules, "openfilter.filter_runtime.filter", mock.Mock(Filter=filter_cls))
    return video_in, webvis, ocr_filter, filter_cls

def test_pipeline_runner_handles_exception(monkeypatch, patch_imports, capsys):
    _, _, _, filter_cls = patch_imports

    filter_cls.run_multi.side_effect = Exception("test error")

    import filter_hello_ocr.pipeline_runner as pipeline_runner

    monkeypatch.setattr(pipeline_runner, "__name__", "__main__")
    
    with pytest.raises(Exception):
        exec(open(pipeline_runner.__file__).read(), pipeline_runner.__dict__)

    captured = capsys.readouterr()
    assert "[ERRO]: test error" in captured.err or "[ERRO]: test error" in captured.out


def test_pipeline_runner_configures_and_runs_correctly(monkeypatch, patch_imports):
    video_in, webvis, ocr_filter, filter_cls = patch_imports

    import filter_hello_ocr.pipeline_runner as pipeline_runner

    filter_cls.run_multi.reset_mock()

    monkeypatch.setattr(pipeline_runner, "__name__", "__main__")
    exec(open(pipeline_runner.__file__).read(), pipeline_runner.__dict__)

    assert filter_cls.run_multi.called

    args, kwargs = filter_cls.run_multi.call_args

    assert isinstance(args[0], list)
    assert len(args[0]) == 3 

    expected_config = [
        (video_in, {
            "id": "VideoIn",
            "outputs": ["tcp://*:5550"],
            "sources": [{
                "source": "file://example_video.mp4",
                "topic": "main",
                "options": {"loop": True}
            }]
        }),
        (ocr_filter, {
            "id": "OCRFilter",
            "sources": ["tcp://localhost:5550"],
            "outputs": ["tcp://*:5552"],
            "ocr_engine": "easyocr",
            "forward_ocr_texts": True
        }),
        (webvis, {
            "id": "Webvis",
            "sources": ["tcp://localhost:5552"]
        })
    ]

    for i, (mock_cls, config) in enumerate(expected_config):
        assert args[0][i][0] is mock_cls 
        assert args[0][i][1] == config 
