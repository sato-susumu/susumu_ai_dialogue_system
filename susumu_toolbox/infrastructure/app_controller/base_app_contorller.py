import logging

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.emotion import Emotion


class BaseAppController:
    def __init__(self, config: Config):
        self._config = config
        self._logger = logging.getLogger(__name__)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def set_emotion(self, emotion: Emotion):
        pass
