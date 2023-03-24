from susumu_toolbox.infrastructure.config import Config


class BaseEmotionModel:
    # https://vrm.dev/vrm1/changed.html#vrmc-vrm-expression
    HAPPY = 'happy'
    SAD = 'sad'
    SURPRISED = 'surprised'
    ANGRY = 'angry'
    RELAXED = 'relaxed'

    def __init__(self, config: Config):
        self._config = config

    def get_max_emotion(self, text: str):
        return {self.HAPPY, 0.0}, {self.HAPPY, 0.0}
