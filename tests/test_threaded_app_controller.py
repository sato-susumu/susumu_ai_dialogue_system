import pytest
from unittest.mock import MagicMock

from susumu_ai_dialogue_system.infrastructure.avatar_controller.async_repeat_avatar_controller import AsyncRepeatAvatarController
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.emotion import Emotion


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def source_controller():
    return MagicMock()


def test_connect(config, source_controller):
    threaded_controller = AsyncRepeatAvatarController(config, source_controller)
    threaded_controller.connect()
    assert threaded_controller._thread is not None


def test_disconnect(config, source_controller):
    threaded_controller = AsyncRepeatAvatarController(config, source_controller)
    threaded_controller.connect()
    threaded_controller.disconnect()
    assert threaded_controller._thread is None


def test_set_emotion(config, source_controller):
    threaded_controller = AsyncRepeatAvatarController(config, source_controller)
    emotion = Emotion.SAD
    threaded_controller.set_emotion(emotion)
    assert threaded_controller._current_emotion == emotion


def test_run(config, source_controller):
    threaded_controller = AsyncRepeatAvatarController(config, source_controller)
    threaded_controller._stop_requested_event.set()
    threaded_controller._run()
    source_controller.connect.assert_called_once()
    source_controller.disconnect.assert_called_once()
