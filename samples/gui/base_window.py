from susumu_toolbox.utility.config import Config


class BaseWindow:
    WINDOW_SIZE = (600, 400)
    INPUT_SIZE_SHORT = (8, 1)
    INPUT_SIZE_NORMAL = (20, 1)
    INPUT_SIZE_LONG = (70, 1)
    BUTTON_SIZE_NORMAL = (10, 1)

    def __init__(self, config: Config):
        self._config = config
