import os
import sys

import PySimpleGUI as Sg
from loguru import logger

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

    logger.remove()
    logger.add(
        sys.stdout,
        level='DEBUG',
        # format="<green>{time:YYYY-MM-DD HH:mm:ss.SSSSSS}</green> | <level>{level:<7}</level> | {message}"
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | {message}"
    )

    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | {message}"
    logger.add("log/{time:YYYY-MM-DD}_app.log",
               format=log_format)
    logger.add("log/{time:YYYY-MM-DD}_error.log",
               level="ERROR",
               format=log_format)

    _config = Config()
    _config_file_path = _config.get_default_config_path()
    _config.set_current_config_path(_config_file_path)
    if os.path.exists(_config_file_path):
        _config.load(_config_file_path)
    Sg.theme(_config.get_gui_theme_name())
    MainWindow(_config).display()
