from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.main_window import MainWindow


def test_main_window():
    config = Config()
    MainWindow(config)
