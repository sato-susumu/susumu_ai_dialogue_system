import os
from typing import Optional


# noinspection PyMethodMayBeStatic
class SystemSettings:
    def __init__(self):
        self._setting = ""

    def load_settings(self, file_path: Optional[str] = None) -> None:
        with open(file_path, encoding='utf-8') as file:
            self._setting = file.read()

    def get_config_dir(self) -> str:
        return os.path.join(os.path.dirname(__file__), "../../config/")

    def get_system_settings(self) -> str:
        return self._setting
