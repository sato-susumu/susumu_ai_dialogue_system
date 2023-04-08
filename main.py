import os

from susumu_ai_dialogue_system.application.common.log_mannager import LogManager
from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.main_window import MainWindow


if __name__ == "__main__":
    LogManager().setup_logger()

    _config = Config()
    _config_file_path = _config.get_default_config_path()
    _config.set_current_config_path(_config_file_path)
    if os.path.exists(_config_file_path):
        _config.load(_config_file_path)
    MainWindow(_config).display()
