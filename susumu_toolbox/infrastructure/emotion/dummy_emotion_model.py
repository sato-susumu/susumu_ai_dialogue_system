from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.base_emotion_model import BaseEmotionModel


class DummyEmotionModel(BaseEmotionModel):
    def __init__(self, config: Config):
        super().__init__(config)

    # noinspection PyMethodMayBeStatic
    def get_max_emotion(self, text: str) -> (dict, dict):
        return {self.HAPPY, 0.0}, {self.HAPPY, 0.0}

