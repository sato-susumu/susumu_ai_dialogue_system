from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

import PySimpleGUI as Sg

from susumu_ai_dialogue_system.ui.base_layout import BaseLayout
from susumu_ai_dialogue_system.infrastructure.config import Config, InputFunction, BaseFunction,\
    OutputFunction


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
            Sg.Radio(key=key, text=text, group_id='base',
                     default=self._config.get_common_base_function().value == key,
                     enable_events=True,
                     )
        ] for key, text in self._config.base_function_dict.items()]

        input_function_items = [[
            Sg.Radio(key=key, text=text, group_id='input',
                     default=self._config.get_common_input_function().value == key,
                     enable_events=True,
                     )
        ] for key, text in self._config.input_function_dict.items()]

        output_function_items = [[
            Sg.Radio(key=key, text=text, group_id='output',
                     default=self._config.get_common_output_function().value == key,
                     enable_events=True,
                     )
        ] for key, text in self._config.output_function_dict.items()]

        other_function_items = [
            [Sg.Checkbox(
                text="OBS出力 (追加設定が必要)",
                key=self._config.KEY_COMMON_OBS_ENABLED,
                default=self._config.get_common_obs_enabled(),
                enable_events=True,
            )],
            [Sg.Checkbox(
                text="感情解析とVMagicMirror連携 (追加設定が必要)",
                key=self._config.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED,
                default=self._config.get_common_v_magic_mirror_connection_enabled(),
                enable_events=True,
            )],
        ]

        common_tab_layout = [[
            Sg.Column([
                [Sg.Frame("ベース機能", base_function_items, expand_x=True)],
                [Sg.Frame("入力", input_function_items, expand_x=True)],
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

    def handle_event(self, event, values) -> None:
        if event in self._config.base_function_dict.keys():
            [self._config.set_common_base_function(BaseFunction.str2function(key)) for key in
             self._config.base_function_dict.keys() if values[key]]

        if event in self._config.input_function_dict.keys():
            [self._config.set_common_input_function(InputFunction.str2function(key)) for key in
             self._config.input_function_dict.keys() if values[key]]

        if event in self._config.output_function_dict.keys():
            [self._config.set_common_output_function(OutputFunction.str2function(key))
             for key in self._config.output_function_dict.keys() if values[key]]

        match event:
            case self._config.KEY_COMMON_OBS_ENABLED:
                self._config.set_common_obs_enabled(values[self._config.KEY_COMMON_OBS_ENABLED])
            case self._config.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED:
                self._config.set_common_v_magic_mirror_connection_enabled(
                    values[self._config.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED])
