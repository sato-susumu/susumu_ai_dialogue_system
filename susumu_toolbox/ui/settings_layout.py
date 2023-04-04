from __future__ import annotations

from typing import TYPE_CHECKING

import PySimpleGUI as Sg

from susumu_toolbox.infrastructure.config import Config, InputFunction, ChatFunction, BaseFunction, OutputFunction
from susumu_toolbox.ui.base_layout import BaseLayout
from susumu_toolbox.ui.settings_ai_tab_layout import SettingsAiTabLayout
from susumu_toolbox.ui.settings_api_key_tab_layout import SettingsApiKeyTabLayout
from susumu_toolbox.ui.settings_chat_tab_layout import SettingsChatTabLayout
from susumu_toolbox.ui.settings_common_tab_layout import SettingsCommonTabLayout
from susumu_toolbox.ui.settings_other_tab_layout import SettingsOtherTabLayout
from susumu_toolbox.ui.settings_stt_tab_layout import SettingsSttTabLayout
from susumu_toolbox.ui.settings_tts_tab_layout import SettingsTtsTabLayout

if TYPE_CHECKING:
    from susumu_toolbox.ui.main_window import MainWindow


# noinspection PyMethodMayBeStatic
class SettingsLayout(BaseLayout):

    def __init__(self, config: Config, main_window: MainWindow):
        super().__init__(config, main_window)
        self.__common_tab_layout = SettingsCommonTabLayout(config, self, main_window)
        self.__stt_tab_layout = SettingsSttTabLayout(config, self, main_window)
        self.__tts_tab_layout = SettingsTtsTabLayout(config, self, main_window)
        self.__other_tab_layout = SettingsOtherTabLayout(config, self, main_window)
        self.__api_key_tab_layout = SettingsApiKeyTabLayout(config, self, main_window)
        self.__chat_tab_layout = SettingsChatTabLayout(config, self, main_window)
        self.__ai_tab_layout = SettingsAiTabLayout(config, self, main_window)
        self.__tab_layout_list = [
            self.__common_tab_layout,
            self.__stt_tab_layout,
            self.__tts_tab_layout,
            self.__other_tab_layout,
            self.__api_key_tab_layout,
            self.__chat_tab_layout,
            self.__ai_tab_layout,
        ]

    @classmethod
    def get_key(cls) -> str:
        return "settings_layout"

    def __save(self, values: dict) -> None:
        self._config = self.update_local_config_by_values(values, self._config)
        self._config.save()

    def update_elements(self) -> None:
        if self._config.get_openai_api_key() == "":
            self._main_window.window["api_keys_tab"].select()

    def get_layout(self):
        buttons_layout = [
            [
                Sg.Button("保存して閉じる", size=(15, 1), key="save"),
                Sg.Button('キャンセル', size=self.BUTTON_SIZE_NORMAL, key="cancel"),
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
                    [Sg.Tab('その他', self.__other_tab_layout.get_layout())],
                ],
                # tab_location='left',
                expand_x=True,
                expand_y=True,
            )],
            [Sg.Column(buttons_layout, justification='center')],
        ]
        return window_layout

    def update_local_config_by_values(self, values, target_config) -> Config:
        # API KEY
        target_config.set_openai_api_key(values[self._config.KEY_OPENAI_API_KEY])
        target_config.set_deepl_auth_key(values[self._config.KEY_DEEPL_AUTH_KEY])

        # AI設定
        target_config.set_ai_system_settings_text(self.__ai_tab_layout.get_current_ai_id(),
                                                  values[self._config.KEY_AI_SYSTEM_SETTINGS_TEXT])

        # 入力
        target_config.set_youtube_live_url(values[self._config.KEY_YOUTUBE_LIVE_URL])
        target_config.set_gcp_youtube_data_api_key(values[self._config.KEY_GCP_YOUTUBE_DATA_API_KEY])
        target_config.set_gcp_speech_to_text_api_key(values[self._config.KEY_GCP_SPEECH_TO_TEXT_API_KEY])

        # チャットエンジン
        target_config.set_parlai_host(values[self._config.KEY_PARLAI_HOST])
        if values[self._config.KEY_PARLAI_PORT_NO] != "":
            target_config.set_parlai_port_no(int(values[self._config.KEY_PARLAI_PORT_NO]))

        # 出力
        target_config.set_voicevox_host(values[self._config.KEY_VOICEVOX_HOST])
        if values[self._config.KEY_VOICEVOX_PORT_NO] != "":
            target_config.set_voicevox_port_no(int(values[self._config.KEY_VOICEVOX_PORT_NO]))
        target_config.set_voicevox_speaker_no(self.__tts_tab_layout.get_selected_speaker_no(values))
        target_config.set_gcp_text_to_speech_api_key(values[self._config.KEY_GCP_TEXT_TO_SPEECH_API_KEY])

        # その他
        target_config.set_obs_host(values[self._config.KEY_OBS_HOST])
        if values[self._config.KEY_OBS_PORT_NO] != "":
            target_config.set_obs_port_no(int(values[self._config.KEY_OBS_PORT_NO]))
        target_config.set_obs_password(values[self._config.KEY_OBS_PASSWORD])
        target_config.set_advanced_console_log_level(self.__other_tab_layout.get_selected_console_log_level(values))

        # 共通設定
        [target_config.set_common_base_function(BaseFunction.str2function(key)) for key in
         self._config.base_function_dict.keys() if
         values[key]]
        [target_config.set_common_input_function(InputFunction.str2function(key)) for key in
         self._config.input_function_dict.keys() if
         values[key]]
        [target_config.set_common_chat_function(ChatFunction.str2function(key)) for key in
         self._config.chat_function_dict.keys() if
         values[key]]
        [target_config.set_common_output_function(OutputFunction.str2function(key))
         for key in self._config.output_function_dict.keys() if values[key]]

        target_config.set_common_obs_enabled(values[self._config.KEY_COMMON_OBS_ENABLED])
        target_config.set_common_v_magic_mirror_connection_enabled(
            values[self._config.KEY_COMMON_V_MAGIC_MIRROR_CONNECTION_ENABLED])

        return target_config

    def handle_event(self, event, values) -> None:
        from susumu_toolbox.ui.main_layout import MainLayout

        if event == "save":
            self.__save(values)
            self._main_window.update_config()
            self._main_window.create_new_window(MainLayout.get_key())
            return
        if event == "cancel":
            self._main_window.update_config()
            self._main_window.create_new_window(MainLayout.get_key())
            return

        if self.is_linked_text_event(event):
            self.open_linked_text_url(event)

        for layout in self.__tab_layout_list:
            layout.handle_event(event, values)
