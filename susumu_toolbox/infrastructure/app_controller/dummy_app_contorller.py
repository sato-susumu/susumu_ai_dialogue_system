from susumu_toolbox.infrastructure.app_controller.base_app_contorller import BaseAppController
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.infrastructure.emotion.emotion import Emotion


class DummyAppController(BaseAppController):
    def __init__(self, config: Config):
        super().__init__(config)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def set_emotion(self, emotion: Emotion):
        pass
