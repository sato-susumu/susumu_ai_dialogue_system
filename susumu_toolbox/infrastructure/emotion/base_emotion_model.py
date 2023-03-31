from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.emotion import Emotion


class BaseEmotionModel:
    def __init__(self, config: Config):
        self._config = config

    def get_max_emotion(self, text: str) -> (Emotion, float, dict):
        return Emotion.HAPPY, 0.0, {Emotion.HAPPY.value: 0.0}
