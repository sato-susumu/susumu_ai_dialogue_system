import webbrowser

import PySimpleGUI as sg

from susumu_toolbox.infrastructure.config import Config


# noinspection PyMethodMayBeStatic
class BaseWindow:
    WINDOW_SIZE = (800, 600)
    INPUT_SIZE_SHORT = (8, 1)
    INPUT_SIZE_NORMAL = (20, 1)
    INPUT_SIZE_LONG = (70, 1)
    BUTTON_SIZE_NORMAL = (10, 1)

    def __init__(self, config: Config):
        self._config = config

    def is_linked_text_event(self, event) -> bool:
        if event.startswith("URL "):
            return True
        return False

    def open_linked_text_url(self, event):
        url = event.split(' ')[1]
        webbrowser.open(url)

    def create_linked_text(self, text: str, url: str):
        font = ('Arial', 10, "underline")
        return sg.Text(text, tooltip=url, enable_events=True, font=font, key=f'URL {url}',
                       pad=(0, 0), text_color="blue")
