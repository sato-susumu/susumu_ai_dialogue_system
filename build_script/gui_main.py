import os

import PySimpleGUI as sg

from susumu_toolbox.sample.gui.main_window import MainWindow
from susumu_toolbox.utility.config import Config

if __name__ == "__main__":
    sg.theme('Bright Colors')
    _config = Config()
    _config_file_path = os.path.join("./", _config.CONFIG_FILE_NAME)
    if os.path.exists(_config_file_path):
        _config.load(_config_file_path)
    MainWindow(_config).display()
