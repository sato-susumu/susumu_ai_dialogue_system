from susumu_toolbox.infrastructure.config import Config


# noinspection PyMethodMayBeStatic,PyShadowingNames
class BaseOBSClient:
    def __init__(self, config: Config):
        self._config = config

    def update_config(self, config: Config):
        self._config = config

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def set_text(self, source: str, text: str) -> None:
        pass

    def set_user_utterance_text(self, text: str) -> None:
        source_name = self._config.get_obs_user_utterance_source_name()
        self.set_text(source_name, text)

    def set_ai_utterance_text(self, text: str) -> None:
        source_name = self._config.get_obs_ai_utterance_source_name()
        self.set_text(source_name, text)
