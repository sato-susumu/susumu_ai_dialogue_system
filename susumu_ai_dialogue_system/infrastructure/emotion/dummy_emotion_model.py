from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.base_emotion_model import BaseEmotionModel
from susumu_ai_dialogue_system.infrastructure.emotion.emotion import Emotion


class DummyEmotionModel(BaseEmotionModel):
    def __init__(self, config: Config):
        super().__init__(config)

    # noinspection PyMethodMayBeStatic
    def get_max_emotion(self, text: str) -> (Emotion, float, dict):
        return Emotion.HAPPY, 0.0, {Emotion.HAPPY.value: 0.0}
