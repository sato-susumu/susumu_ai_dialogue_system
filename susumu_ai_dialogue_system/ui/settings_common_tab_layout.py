from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

import PySimpleGUI as Sg

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout


# noinspection PyMethodMayBeStatic
class SettingsCommonTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_common_tab_layout"

    def get_layout(self):
        base_function_items = [[
            Sg.Radio(key=key, text=text, group_id='base', default=self._config.get_common_base_function().value == key)
        ] for key, text in self._config.base_function_dict.items()]

        input_function_items = [[
            Sg.Radio(key=key, text=text, group_id='input',
                     default=self._config.get_common_input_function().value == key)
        ] for key, text in self._config.input_function_dict.items()]

        chat_function_items = [[
            Sg.Radio(key=key, text=text, group_id='chat', default=self._config.get_common_chat_function().value == key)
        ] for key, text in self._config.chat_function_dict.items()]

        output_function_items = [[
            Sg.Radio(key=key, text=text, group_id='output',
                     default=self._config.get_common_output_function().value == key)
        ] for key, text in self._config.output_function_dict.items()]

        other_function_items = [
            [Sg.Checkbox(
                text="OBS出力 (追加設定が必要)",
                key=self._config.KEY_COMMON_OBS_ENABLED,
                default=self._config.get_common_obs_enabled(),
            )],
            [Sg.Checkbox(
                text="感情解析とVMagicMirror連携 (追加設定が必要)",
                key=self._config.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED,
                default=self._config.get_common_v_magic_mirror_connection_enabled(),
            )],
        ]

        common_tab_layout = [[
            Sg.Column([
                [Sg.Frame("ベース機能", base_function_items, expand_x=True)],
                [Sg.Frame("入力", input_function_items, expand_x=True)],
                [Sg.Frame("チャットエンジン", chat_function_items, expand_x=True)],
                [Sg.Frame("出力", output_function_items, expand_x=True)],
                [Sg.Frame("実験", other_function_items, expand_x=True)],
            ],
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
            ),
        ]]
        return common_tab_layout

    def update_elements(self) -> None:
        pass

    def handle_event(self, event, values) -> None:
        pass
