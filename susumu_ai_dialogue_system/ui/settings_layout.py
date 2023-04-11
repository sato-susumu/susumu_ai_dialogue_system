from __future__ import annotations

from typing import TYPE_CHECKING

import PySimpleGUI as Sg

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout
from susumu_ai_dialogue_system.ui.settings_advanced_tab_layout import SettingsAdvancedTabLayout
from susumu_ai_dialogue_system.ui.settings_ai_tab_layout import SettingsAiTabLayout
from susumu_ai_dialogue_system.ui.settings_api_key_tab_layout import SettingsApiKeyTabLayout
from susumu_ai_dialogue_system.ui.settings_chat_tab_layout import SettingsChatTabLayout
from susumu_ai_dialogue_system.ui.settings_common_tab_layout import SettingsCommonTabLayout
from susumu_ai_dialogue_system.ui.settings_stt_tab_layout import SettingsSttTabLayout
from susumu_ai_dialogue_system.ui.settings_tts_tab_layout import SettingsTtsTabLayout

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.main_window import MainWindow


# noinspection PyMethodMayBeStatic
class SettingsLayout(BaseLayout):
    _KEY_SETTINGS_SAVE = "key_settings_save"
    _KEY_SETTINGS_CANCEL = "key_settings_cancel"

    def __init__(self, config: Config, main_window: MainWindow):
        super().__init__(config, main_window)
        self.__common_tab_layout = SettingsCommonTabLayout(config, self, main_window)
        self.__stt_tab_layout = SettingsSttTabLayout(config, self, main_window)
        self.__tts_tab_layout = SettingsTtsTabLayout(config, self, main_window)
        self.__advanced_tab_layout = SettingsAdvancedTabLayout(config, self, main_window)
        self.__api_key_tab_layout = SettingsApiKeyTabLayout(config, self, main_window)
        self.__chat_tab_layout = SettingsChatTabLayout(config, self, main_window)
        self.__ai_tab_layout = SettingsAiTabLayout(config, self, main_window)
        self.__tab_layout_list = [
            self.__common_tab_layout,
            self.__stt_tab_layout,
            self.__tts_tab_layout,
            self.__advanced_tab_layout,
            self.__api_key_tab_layout,
            self.__chat_tab_layout,
            self.__ai_tab_layout,
        ]

    @classmethod
    def get_key(cls) -> str:
        return "settings_layout"

    def __save(self) -> None:
        self._config.save()

    def update_elements(self) -> None:
        if self._config.get_openai_api_key() == "":
            self._main_window.window["api_keys_tab"].select()

    def update_config(self, config: Config) -> None:
        self._config = config
        for layout in self.__tab_layout_list:
            layout.update_config(config)

    def get_layout(self):
        buttons_layout = [
            [
                Sg.Button("保存して閉じる", size=(15, 1), key=self._KEY_SETTINGS_SAVE),
                Sg.Button('キャンセル', size=self.BUTTON_SIZE_NORMAL, key=self._KEY_SETTINGS_CANCEL),
            ],
        ]

        window_layout = [
            [Sg.TabGroup(
                [
                    [Sg.Tab('共通設定', self.__common_tab_layout.get_layout())],
                    [Sg.Tab('API KEY', self.__api_key_tab_layout.get_layout(), key="api_keys_tab")],
                    [Sg.Tab('AI設定', self.__ai_tab_layout.get_layout())],
                    [Sg.Tab('入力', self.__stt_tab_layout.get_layout())],
                    [Sg.Tab('チャットエンジン', self.__chat_tab_layout.get_layout())],
                    [Sg.Tab('出力', self.__tts_tab_layout.get_layout())],
                    [Sg.Tab('実験', self.__advanced_tab_layout.get_layout())],
                ],
                # tab_location='left',
                expand_x=True,
                expand_y=True,
            )],
            [Sg.Column(buttons_layout, justification='center')],
        ]
        return window_layout

    def handle_event(self, event, values) -> None:
        from susumu_ai_dialogue_system.ui.main_layout import MainLayout

        match event:
            case self._KEY_SETTINGS_SAVE:
                self.__save()
                self._main_window.reload_and_update_config()
                self._main_window.create_new_window(MainLayout.get_key())
                return
            case self._KEY_SETTINGS_CANCEL:
                self._main_window.reload_and_update_config()
                self._main_window.create_new_window(MainLayout.get_key())
                return

        if self.is_linked_text_event(event):
            self.open_linked_text_url(event)

        for layout in self.__tab_layout_list:
            layout.handle_event(event, values)
