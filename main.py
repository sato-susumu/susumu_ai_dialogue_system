import os

import PySimpleGUI as Sg

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.main_window import MainWindow


def create_model_data_dir_if_needed():
    model_data_dir = "./model_data"
    if not os.path.exists(model_data_dir):
        os.mkdir(model_data_dir)


def create_log_dir_if_needed():
    model_data_dir = "./log"
    if not os.path.exists(model_data_dir):
        os.mkdir(model_data_dir)


if __name__ == "__main__":
    create_model_data_dir_if_needed()
    create_log_dir_if_needed()

    # TODO:ログ出力対応
    # TODO:GUIに合わせてドキュメントも更新
    _config = Config()
    _config_file_path = _config.get_default_config_path()
    _config.set_current_config_path(_config_file_path)
    if os.path.exists(_config_file_path):
        _config.load(_config_file_path)
    Sg.theme(_config.get_gui_theme_name())
    MainWindow(_config).display()
