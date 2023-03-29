# noinspection PyMethodMayBeStatic
import logging


class BaseVad:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_threshold(self) -> float:
        return 0.0

    def detect(self, audio_chunk) -> float:
        return 0.0
