from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.main_window import MainWindow


def test_main_window():
    config = Config()
    MainWindow(config)
