from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic,PyShadowingNames
class BaseOBSClient:
    def __init__(self, config: Config):
        self._config = config

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def set_text(self, scene_name: str, source: str, text: str) -> None:
        pass
