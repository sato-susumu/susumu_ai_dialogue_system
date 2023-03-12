from typing import Optional

# noinspection PyMethodMayBeStatic
from susumu_toolbox.utility.config import Config


class SystemSettings:
    def __init__(self, config: Config):
        self._setting = ""
        self._config = config

    def load_settings(self, file_path: Optional[str] = None) -> None:
        with open(file_path, encoding='utf-8') as file:
            self._setting = file.read()

    def get_config_dir(self) -> str:
        return self._config.get_config_dir()

    def get_system_settings(self) -> str:
        return self._setting
