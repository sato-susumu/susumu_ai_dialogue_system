import logging
from threading import Thread, Event

from susumu_toolbox.infrastructure.app_controller.base_app_contorller import BaseAppController
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.emotion import Emotion


class ThreadedAppController(BaseAppController):
    def __init__(self, config: Config, source_controller: BaseAppController):
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
    from susumu_toolbox.infrastructure.app_controller.vmagicmirror_controller import VMagicMirrorController
    import random
    from time import sleep

    logging.basicConfig(level=logging.DEBUG)

    _logger = logging.getLogger(__name__)
    _config = Config()
    _source_controller = VMagicMirrorController(_config)
    _controller = ThreadedAppController(_config, _source_controller)
    _controller.connect()
    try:
        while True:
            _emotion = random.choice(list(Emotion))
            _logger.debug(_emotion)
            _controller.set_emotion(_emotion)
            sleep(5)
    finally:
        _controller.disconnect()
