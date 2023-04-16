from __future__ import annotations

from typing import TYPE_CHECKING

import PySimpleGUI as Sg

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

from susumu_ai_dialogue_system.infrastructure.config import Config, LangChainMemoryType
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout


# noinspection PyMethodMayBeStatic
class SettingsLangchainTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_langchain_tab_layout"

    def get_layout(self):
        memory_items = [[
            Sg.Radio(key=name, text=name, group_id='memory_type',
                     default=self._config.get_langchain_memory_type().name == name,
                     enable_events=True,
                     )
        ] for name in LangChainMemoryType.keys()]

        langchain_group_layout = [
            [Sg.Text('・利用には API KEYタブ > OpenAI API Key の入力が必要です。')],
            [Sg.Checkbox('Conversationの詳細をログに出力する',
                         key=self._config.KEY_LANGCHAIN_CONVERSATION_VERBOSE,
                         default=self._config.get_langchain_conversation_verbose(),
                         enable_events=True,
                         )],
            [Sg.Frame("Memory", memory_items, expand_x=True)],
        ]

        langchain_tab_layout = [
            [Sg.Frame("LangChain", langchain_group_layout, expand_x=True)],
        ]

        return langchain_tab_layout

    def handle_event(self, event, values) -> None:
        match event:
            case self._config.KEY_LANGCHAIN_CONVERSATION_VERBOSE:
                self._config.set_langchain_conversation_verbose(
                    values[self._config.KEY_LANGCHAIN_CONVERSATION_VERBOSE])

        if event in LangChainMemoryType.keys():
            [self._config.set_langchain_memory_type(memory_type)
             for memory_type in LangChainMemoryType if values[memory_type.name]]
