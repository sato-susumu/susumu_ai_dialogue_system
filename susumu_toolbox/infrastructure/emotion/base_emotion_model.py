from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.emotion import Emotion


class BaseEmotionModel:
    HAPPY = 'happy'
    SAD = 'sad'
    SURPRISED = 'surprised'
    ANGRY = 'angry'
    RELAXED = 'relaxed'

    def __init__(self, config: Config):
        self._config = config

    def get_max_emotion(self, text: str) -> (dict, dict):
        return {Emotion.HAPPY.value, 0.0}, {Emotion.HAPPY.value.HAPPY, 0.0}
