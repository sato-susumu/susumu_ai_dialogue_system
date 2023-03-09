import configparser
import os.path


class GuiConfig:
    _DEFAULT_SECTION = "default"
    _CONFIG_FILE_PATH = "./gui_config.ini"
    _OPEN_AI_API_KEY = "open_ai_api_key"
    _DEFAULT_CONFIG = {
        _DEFAULT_SECTION: {
            _OPEN_AI_API_KEY: ""
        }
    }

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._default_config = None

    def save(self):
        with open(self._CONFIG_FILE_PATH, 'w', encoding="UTF-8") as f:
            self._config.write(f)

    def load(self):
        self._config.read_dict(self._DEFAULT_CONFIG)
        if os.path.exists(self._CONFIG_FILE_PATH):
            self._config.read(self._CONFIG_FILE_PATH, "UTF-8")
        self._default_config = self._config[self._DEFAULT_SECTION]

    @property
    def open_ai_api_key(self):
        return self._config.get(self._DEFAULT_SECTION, self._OPEN_AI_API_KEY)

    @open_ai_api_key.setter
    def open_ai_api_key(self, value):
        self._config.set(self._DEFAULT_SECTION, self._OPEN_AI_API_KEY, value)
