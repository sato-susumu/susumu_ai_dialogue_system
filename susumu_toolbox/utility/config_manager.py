import os
from typing import Optional

import yaml


class ConfigManager:
    def __init__(self):
        self._setting = {}

    # noinspection DuplicatedCode
    def load_config(self, *, file_path: Optional[str] = None) -> None:
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), "../../config/config.yaml")

        with open(file_path, encoding='utf-8') as file:
            self._setting = yaml.safe_load(file)

    def get_deepl_auth_key(self):
        return self._setting["DeepL"]["deepl_auth_key"]

    def get_openai_api_key(self):
        return self._setting["OpenAI"]["openai_api_key"]

    def get_obs_host(self):
        return self._setting["OBS"]["obs_host"]

    def get_obs_port_no(self):
        return self._setting["OBS"]["obs_port_no"]

    def get_obs_password(self):
        return self._setting["OBS"]["obs_password"]

    def get_voicevox_host(self):
        return self._setting["VOICEVOX"]["voicevox_host"]

    def get_voicevox_port_no(self):
        return self._setting["VOICEVOX"]["voicevox_prot_no"]

    def get_voicevox_speaker_no(self):
        return self._setting["VOICEVOX"]["voicevox_speaker_no"]

    def get_parlai_host(self):
        return self._setting["ParlAI"]["parlai_host"]

    def get_parlai_port_no(self):
        return self._setting["ParlAI"]["parlai_prot_no"]

