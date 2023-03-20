import os

import PySimpleGUI as sg

from susumu_toolbox.sample.gui.main_window import MainWindow
from susumu_toolbox.utility.config import Config

if __name__ == "__main__":
    sg.theme('Bright Colors')
    # TODO:ログ出力対応
    # TODO:EXEを作成
    # TODO:GUIに合わせてドキュメントも更新
    _config = Config()
    _config_file_path = os.path.join(_config.get_user_data_dir_path(), _config.CONFIG_FILE_NAME)
    _config.set_config_path(_config_file_path)
    if os.path.exists(_config_file_path):
        _config.load(_config_file_path)
    MainWindow(_config).display()
    # SettingsWindow(_config).display()
    # WelcomeWindow(_config).display()
