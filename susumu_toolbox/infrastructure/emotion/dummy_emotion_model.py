from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.base_emotion_model import BaseEmotionModel
from susumu_toolbox.infrastructure.emotion.emotion import Emotion


class DummyEmotionModel(BaseEmotionModel):
    def __init__(self, config: Config):
        super().__init__(config)

    # noinspection PyMethodMayBeStatic
    def get_max_emotion(self, text: str) -> (dict, dict):
        return {Emotion.HAPPY.value, 0.0}, {Emotion.HAPPY.value, 0.0}
