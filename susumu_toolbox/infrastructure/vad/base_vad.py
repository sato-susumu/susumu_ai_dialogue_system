# noinspection PyMethodMayBeStatic
class BaseVad:
    def __init__(self):
        pass

    def get_threshold(self) -> float:
        return 0.0

    def detect(self, audio_chunk) -> float:
        return 0.0
