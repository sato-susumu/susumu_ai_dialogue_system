from susumu_ai_dialogue_system.infrastructure.avatar_controller.base_avatar_controller import BaseAvatarController
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.emotion.emotion import Emotion


class DummyAvatarController(BaseAvatarController):
    def __init__(self, config: Config):
        super().__init__(config)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def set_emotion(self, emotion: Emotion):
        pass
