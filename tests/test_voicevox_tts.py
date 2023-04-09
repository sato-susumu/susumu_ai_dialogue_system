import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest
import requests

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.tts.voicevox_tts import VoicevoxTTS


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def tts(config):
    return VoicevoxTTS(config)


def test_get_version(tts, requests_mock):
    version = "0.2.2"
    requests_mock.get("http://127.0.0.1:50021/version", text=version)

    assert tts.get_version() == version


# noinspection SpellCheckingInspection
def test_get_raw_speakers(tts, requests_mock):
    json_data = [{"name": "Yukari", "styles": [{"id": 0, "name": "normal"}, {"id": 1, "name": "angry"}]},
                 {"name": "Takumi", "styles": [{"id": 0, "name": "normal"}, {"id": 1, "name": "shout"}]}]

    requests_mock.get("http://127.0.0.1:50021/speakers", json=json_data)

    assert tts.get_raw_speakers() == json_data


# noinspection SpellCheckingInspection
def test_get_speakers(tts):
    tts.get_raw_speakers = MagicMock(return_value=[{"name": "Yukari", "styles": [{"id": 0, "name": "normal"}]}])

    expected = {"Yukari-normal": 0}
    assert tts.get_speakers() == expected


def test_synthesize(tts, requests_mock):
    audio_content = b"audio data"
    requests_mock.post("http://127.0.0.1:50021/audio_query", json={})
    requests_mock.post("http://127.0.0.1:50021/synthesis", content=audio_content)

    result = tts._synthesize("test")

    assert result == audio_content


def test_tts_save_wav(tts, requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.wav")
        audio_content = b"audio data"
        requests_mock.post("http://127.0.0.1:50021/audio_query", json={})
        requests_mock.post("http://127.0.0.1:50021/synthesis", content=audio_content)

        tts.tts_save_wav("test", file_path)

        with open(file_path, "rb") as f:
            assert f.read() == audio_content


@patch("susumu_ai_dialogue_system.infrastructure.tts.base_tts.BaseTTS._wav_play_async")
def test_tts_play_async(mock_wav_play_async, tts, requests_mock):
    audio_content = b"audio data"
    requests_mock.post("http://127.0.0.1:50021/audio_query", json={})
    requests_mock.post("http://127.0.0.1:50021/synthesis", content=audio_content)

    tts.tts_play_async("test")

    mock_wav_play_async.assert_called_once_with(audio_content, tts._on_playback_completed, tts._on_error)


@patch("susumu_ai_dialogue_system.infrastructure.tts.base_tts.BaseTTS._wav_play_async")
def test_tts_play_async_connection_error(mock_wav_play_async, tts, requests_mock):
    requests_mock.post("http://127.0.0.1:50021/audio_query", exc=requests.exceptions.ConnectionError)

    with pytest.raises(requests.exceptions.ConnectionError):
        tts.tts_play_async("test")

    mock_wav_play_async.assert_not_called()


@patch("susumu_ai_dialogue_system.infrastructure.tts.base_tts.BaseTTS._wav_play_sync")
def test_tts_play_sync(mock_wav_play_sync, tts, requests_mock):
    audio_content = b"audio data"
    requests_mock.post("http://127.0.0.1:50021/audio_query", json={})
    requests_mock.post("http://127.0.0.1:50021/synthesis", content=audio_content)

    tts.tts_play_sync("test")

    mock_wav_play_sync.assert_called_once_with(audio_content, tts._on_playback_completed, tts._on_error)
