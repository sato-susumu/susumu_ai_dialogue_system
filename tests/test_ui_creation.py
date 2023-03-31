from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_window import BaseWindow
from susumu_toolbox.ui.main_window import MainWindow
from susumu_toolbox.ui.settings_window import SettingsWindow


def test_base_window():
    config = Config()
    BaseWindow(config)


def test_main_window():
    config = Config()
    MainWindow(config)


def test_settings_window():
    config = Config()
    SettingsWindow(config)
