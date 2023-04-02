from __future__ import annotations

from typing import TYPE_CHECKING

import PySimpleGUI as Sg

if TYPE_CHECKING:
    from susumu_toolbox.ui.settings_layout import SettingsLayout
    from susumu_toolbox.ui.main_window import MainWindow

from PySimpleGUI import Window

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_layout import BaseLayout


# noinspection PyMethodMayBeStatic
class SettingsChatTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout):
        super().__init__(config)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_chat_tab_layout"

    def get_layout(self):
        parlai_items = [
            [Sg.Text('・利用には ParlAI Chat Server の起動が必要です。')],
            [Sg.Text('アドレス'),
             Sg.InputText(key=self._config.KEY_PARLAI_HOST,
                          default_text=self._config.get_parlai_host(),
                          size=self.INPUT_SIZE_NORMAL,
                          )
             ],
            [Sg.Text('ポート番号'),
             Sg.InputText(key=self._config.KEY_PARLAI_PORT_NO,
                          default_text=self._config.get_parlai_port_no(),
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          )
             ],
        ]

        chat_gpt_items = [
            [Sg.Text('・利用には API KEYタブ > OpenAI API Key の入力が必要です。')],
        ]

        chat_tab_layout = [
            [Sg.Frame("ChatGPT", chat_gpt_items, expand_x=True)],
            [Sg.Frame("ParlAI", parlai_items, expand_x=True)],
        ]

        return chat_tab_layout

    def update_layout(self, window: Window) -> None:
        pass

    def handle_event(self, event, values, main_window: MainWindow) -> None:
        if event == self._config.KEY_PARLAI_PORT_NO:
            main_window.input_validation_number_only(event, values)
