import os

import PySimpleGUI as sg

from susumu_toolbox.sample.gui.main_window import MainWindow
from susumu_toolbox.utility.config import Config

if __name__ == "__main__":
    # TODO:(低)設定画面のテーマ変更
    sg.theme('Bright Colors')
    # TODO:ログ出力対応
    # TODO:GUIに合わせてドキュメントも更新
    _config = Config()
    _config_file_path = _config.get_default_config_path()
    _config.set_current_config_path(_config_file_path)
    if os.path.exists(_config_file_path):
        _config.load(_config_file_path)
    MainWindow(_config).display()
