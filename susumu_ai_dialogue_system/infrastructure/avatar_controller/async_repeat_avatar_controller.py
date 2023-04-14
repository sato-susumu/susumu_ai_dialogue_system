from threading import Thread, Event

import loguru

from susumu_ai_dialogue_system.infrastructure.avatar_controller.base_avatar_controller import BaseAvatarController
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.emotion import Emotion


class AsyncRepeatAvatarController(BaseAvatarController):
    def __init__(self, config: Config, source_controller: BaseAvatarController):
        super().__init__(config)

        self._source_controller = source_controller
        self._thread = None
        self._current_emotion = Emotion.NEUTRAL
        self._stop_requested_event = Event()

    def _run(self):
        self._source_controller.connect()
        while not self._stop_requested_event.wait(timeout=1):
            self._source_controller.set_emotion(self._current_emotion)
        self._source_controller.disconnect()

    def connect(self):
        if self._thread is None:
            self._thread = Thread(target=self._run, daemon=True)
            self._thread.start()

    def disconnect(self):
        if self._thread:
            self._stop_requested_event.set()
            self._thread.join()
            self._thread = None

    def set_emotion(self, emotion: Emotion):
        self._current_emotion = emotion


if __name__ == '__main__':
    from susumu_ai_dialogue_system.infrastructure.avatar_controller.vmagicmirror_avatar_controller import VMagicMirrorController
    import random
    from time import sleep

    _config = Config()
    _source_controller = VMagicMirrorController(_config)
    _controller = AsyncRepeatAvatarController(_config, _source_controller)
    _controller.connect()
    try:
        while True:
            _emotion = random.choice(list(Emotion))
            loguru.logger.debug(_emotion)
            _controller.set_emotion(_emotion)
            sleep(5)
    finally:
        _controller.disconnect()
