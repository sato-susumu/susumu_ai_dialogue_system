import os

from omegaconf import OmegaConf

from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.system_setting import SystemSettings


# noinspection PyMethodMayBeStatic
class AiConfig:
    def __init__(self, config: Config, ai_id: str):
        self._config = config
        self._system_settings = SystemSettings(config)
        self._ai_id = ai_id
        self._ai_name = "default"

    def get_id(self) -> str:
        return self._ai_id

    def get_name(self) -> str:
        return self._ai_name

    def get_system_settings(self) -> SystemSettings:
        return self._system_settings

    def set_system_settings(self, system_settings: SystemSettings) -> None:
        self._system_settings = system_settings

    def _save_ai_config(self) -> None:
        dict_conf = {
            "ai_id": self._ai_id,
            "ai_name": self._ai_name,
        }
        config = OmegaConf.create(dict_conf)

        self._config.make_ai_config_dir_if_needed()
        config_file_path = self._config.get_ai_config_file_path(self._ai_id)
        OmegaConf.save(config, config_file_path)

    def _save_system_settings(self) -> None:
        system_settings_file_path = self._config.get_ai_system_settings_file_path(self._ai_id)
        self._system_settings.save(system_settings_file_path)

    def save(self) -> None:
        self._save_ai_config()
        self._save_system_settings()

    def _load_ai_config(self) -> None:
        config_file_path = self._config.get_ai_config_file_path(self._ai_id)
        if os.path.exists(config_file_path):
            config = OmegaConf.load(config_file_path)
            self._ai_id = config["ai_id"]
            self._ai_name = config["ai_name"]
        else:
            raise FileNotFoundError(f"AI設定ファイルが存在しません。{config_file_path}")

    def _load_system_settings(self) -> None:
        system_settings_file_path = self._config.get_ai_system_settings_file_path(self._ai_id)
        if os.path.exists(system_settings_file_path):
            self._system_settings.load(system_settings_file_path)

    def load(self) -> None:
        self._load_ai_config()
        self._load_system_settings()

    def exist_ai_config_file(self):
        file_path = self._config.get_ai_config_file_path(self._ai_id)
        return os.path.exists(file_path)
