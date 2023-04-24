from __future__ import annotations

from typing import TYPE_CHECKING

import PySimpleGUI as Sg
import tiktoken
from loguru import logger

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout


# noinspection PyMethodMayBeStatic
class SettingsAiTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout
        self.__current_ai_id = config.get_ai_id_list()[0]
        self._dirty = False

    @classmethod
    def get_key(cls) -> str:
        raise "settings_ai_tab_layout"

    def get_layout(self):
        ai_tab_layout = [
            [Sg.Text('プロンプト')],
            [Sg.Multiline(
                default_text=self._config.get_ai_system_settings_text(self.__current_ai_id),
                key=self._config.KEY_AI_SYSTEM_SETTINGS_TEXT,
                expand_x=True,
                expand_y=True,
                enable_events=True,
            )]
        ]

        return ai_tab_layout

    def get_current_ai_id(self) -> str:
        return self.__current_ai_id

    def _output_token_count(self, text: str) -> None:
        model_name = "gpt-3.5-turbo"
        encoding = tiktoken.encoding_for_model(model_name)
        token_count = len(encoding.encode(text))
        logger.info(f"token_count={token_count} (model_name={model_name})")

    def handle_event(self, event, values) -> None:
        match event:
            case self._config.KEY_AI_SYSTEM_SETTINGS_TEXT:
                new_text = values[self._config.KEY_AI_SYSTEM_SETTINGS_TEXT]
                self._config.set_ai_system_settings_text(self.get_current_ai_id(), new_text)
                self._dirty = True
            case "__TIMEOUT__":
                if self._dirty:
                    new_text = values[self._config.KEY_AI_SYSTEM_SETTINGS_TEXT]
                    self._output_token_count(new_text)
                    self._dirty = False

