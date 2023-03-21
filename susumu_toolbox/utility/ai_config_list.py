from susumu_toolbox.utility.ai_config import AiConfig
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class AiConfigList:
    def __init__(self, config: Config):
        self._config = config
        self._ai_config_list = [AiConfig(self._config, "default")]

    def get_ai_id_list(self) -> list:
        return [ai_config.get_id() for ai_config in self._ai_config_list]

    def get_ai_config(self, ai_id: str) -> AiConfig:
        for ai_config in self._ai_config_list:
            if ai_config.get_id() == ai_id:
                return ai_config
        raise ValueError(f"該当するAI IDが存在しません。{ai_id}")

    def exist_ai_config_file(self):
        for ai in self._ai_config_list:
            if ai.exist_ai_config_file():
                return True
        return False

    def load(self):
        for ai in self._ai_config_list:
            ai.load()

    def save(self):
        for ai in self._ai_config_list:
            ai.save()
