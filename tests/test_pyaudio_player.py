import tempfile
from unittest.mock import Mock

import pytest
from pyaudio import PyAudio

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.pyaudio_player import PyAudioPlayer


@pytest.fixture
def config():
    config_mock = Mock(spec=Config)
    config_mock.get_pyaudio_second_output_enabled.return_value = False
    config_mock.get_pyaudio_second_output_host_api_name.return_value = ''
    config_mock.get_pyaudio_second_output_device_name.return_value = ''
    return config_mock


@pytest.fixture
def pyaudio():
    pyaudio_mock = Mock(spec=PyAudio)
    return pyaudio_mock


@pytest.fixture
def pyaudio_player(config, pyaudio):
    pa = PyAudioPlayer(config)
    return pa


def test_get_second_output_device_id(config, pyaudio):
    # second_output_enabled が False の場合、-1 が返されることを確認する
    pyaudio_player = PyAudioPlayer(config)
    assert pyaudio_player._get_second_output_device_id() == -1


# noinspection SpellCheckingInspection
def test_play_bytes_async(pyaudio_player):
    audio_content = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x80>\x00\x00\x00}\x00\x00\x04\x00\x10' \
                    b'\x00data\x00\x00\x00\x00'
    on_playback_completed = Mock()
    on_error = Mock()

    pyaudio_player.play_bytes_async(audio_content, on_playback_completed, on_error)

    assert pyaudio_player.is_playing()  # 再生中
    pyaudio_player.stop()
    assert not pyaudio_player.is_playing()  # 停止


# noinspection SpellCheckingInspection
def test_play_bytes_sync(pyaudio_player):
    audio_content = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x80>\x00\x00\x00}\x00\x00\x04\x00\x10' \
                    b'\x00data\x00\x00\x00\x00'
    on_playback_completed = Mock()
    on_error = Mock()

    pyaudio_player.play_bytes_sync(audio_content, on_playback_completed, on_error)

    assert not pyaudio_player.is_playing()  # 停止


# noinspection SpellCheckingInspection
def test_play_wav_file(pyaudio_player):
    on_playback_completed = Mock()
    on_error = Mock()

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        f.write(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x80>\x00\x00\x00}\x00\x00\x04\x00\x10'
                b'\x00data\x00\x00\x00\x00')
        pyaudio_player.play_wav_file(f.name, on_playback_completed, on_error)

    assert not pyaudio_player.is_playing()  # 停止
