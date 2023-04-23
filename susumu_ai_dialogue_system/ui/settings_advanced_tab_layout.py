from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

from loguru import logger

from susumu_ai_dialogue_system.application.common.emotion_test import EmotionTest
from susumu_ai_dialogue_system.application.common.obs_test import OBSTest
from susumu_ai_dialogue_system.ui.secondary_audio_select_window import SecondaryAudioSelectWindow

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout

import PySimpleGUI as Sg


# noinspection PyMethodMayBeStatic
class SettingsAdvancedTabLayout(BaseLayout):
    _log_level_dic = {
        "すべて": "DEBUG",
        "INFO以上": "INFO",
        "WARNING以上": "WARNING",
        "ERROR以上": "ERROR",
    }
    _KEY_ADVANCED_CONSOLE_LOG_LEVEL = "key_advanced_console_log_level"
    _KEY_ADVANCED_GUI_ALL_THEME_PREVIEW = "key_advanced_gui_all_theme_preview"
    _KEY_ADVANCED_EMOTION_TEST_TEXT = "key_advanced_emotion_test_text"
    _KEY_ADVANCED_EMOTION_TEST = "key_advanced_emotion_test"
    _KEY_ADVANCED_OBS_TEST = "key_advanced_obs_test"
    _KEY_ADVANCED_SECONDARY_OUTPUT_API_NAME = "key_advanced_secondary_output_api_name"
    _KEY_ADVANCED_SECONDARY_OUTPUT_DEVICE_NAME = "key_advanced_secondary_output_device_name"
    _KEY_ADVANCED_SECONDARY_OUTPUT_DEVICE_CHANGE = "key_advanced_secondary_output_device_change"

    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_advanced_tab_layout"

    def get_layout(self):
        obs_items = [
            [Sg.Text('・利用には OBS Studio の起動、設定が必要です。')],
            [Sg.Text('・OBS Studioの ツール > obs-websocket設定 で「ウェブサーバーを有効にする」を有効にしてください。')],
            [Sg.Text('アドレス'),
             Sg.InputText(default_text=self._config.get_obs_host(),
                          key=self._config.KEY_OBS_HOST,
                          size=self.INPUT_SIZE_NORMAL,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('ポート番号'),
             Sg.InputText(default_text=self._config.get_obs_port_no(),
                          key=self._config.KEY_OBS_PORT_NO,
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('パスワード'),
             Sg.InputText(default_text=self._config.get_obs_password(),
                          key=self._config.KEY_OBS_PASSWORD,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('AIの発話を表示するテキスト(GDI+)ソース名'),
             Sg.InputText(default_text=self._config.get_obs_ai_utterance_source_name(),
                          key=self._config.KEY_OBS_AI_UTTERANCE_SOURCE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('ユーザーの発話を表示するテキスト(GDI+)ソース名'),
             Sg.InputText(default_text=self._config.get_obs_user_utterance_source_name(),
                          key=self._config.KEY_OBS_USER_UTTERANCE_SOURCE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          ),
             ],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_ADVANCED_OBS_TEST)],
        ]

        emotion_items = [
            [Sg.Text("・感情解析サーバー"),
             self.create_linked_text("https://github.com/sato-susumu/susumu_emotional_analysis",
                                     "https://github.com/sato-susumu/susumu_emotional_analysis"),
             Sg.Text("の起動が必要です。")],
            [Sg.Text("・起動にはdockerなどの知識が必要です。")],
            [Sg.Text('アドレス'),
             Sg.InputText(default_text=self._config.get_wrime_emotion_server_host(),
                          key=self._config.KEY_WRIME_EMOTION_SERVER_HOST,
                          size=self.INPUT_SIZE_NORMAL,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('ポート番号'),
             Sg.InputText(default_text=self._config.get_wrime_emotion_server_port_no(),
                          key=self._config.KEY_WRIME_EMOTION_SERVER_PORT_NO,
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('感情解析テスト用文字列'),
             Sg.InputText(default_text="なお、このメッセージは5秒後に自動的に消滅する。",
                          key=self._KEY_ADVANCED_EMOTION_TEST_TEXT,
                          expand_x=True,
                          enable_events=True,
                          ),
             ],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_ADVANCED_EMOTION_TEST)],
        ]

        v_magic_mirror_items = [
            [Sg.Text('・VMagicMirrorの起動と事前の設定が必要です。')],
        ]

        log_level_value = self._config.get_advanced_console_log_level()
        log_level_key = [k for k, v in self._log_level_dic.items() if v == log_level_value][0]

        log_level_items = [
            [
                Sg.Text('コンソールログ出力'),
                Sg.Combo(values=list(self._log_level_dic.keys()),
                         default_value=log_level_key,
                         key=self._KEY_ADVANCED_CONSOLE_LOG_LEVEL,
                         size=(30, 1),
                         readonly=True,
                         enable_events=True,
                         )
            ]
        ]

        secondary_audio_items = [
            [Sg.Text("・一部の音声合成、一部のデバイスのみ対応しています。")],
            [Sg.Text("・Windowsでは、MMEおよびWASAPIの一部デバイスのみ動作確認しています。")],
            [Sg.Checkbox("音声を出力する",
                         default=self._config.get_pyaudio_secondary_output_enabled(),
                         key=self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_ENABLED,
                         enable_events=True,
                         )],
            [Sg.Text("API名:"),
             Sg.Text(text=self._config.get_pyaudio_secondary_output_api_name(),
                     key=self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_API_NAME),
             ],
            [Sg.Text("デバイス名:"),
             Sg.Text(text=self._config.get_pyaudio_secondary_output_device_name(),
                     key=self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_DEVICE_NAME),
             ],
            [Sg.Button("デバイスの変更",
                       size=self.BUTTON_SIZE_LONG,
                       key=self._KEY_ADVANCED_SECONDARY_OUTPUT_DEVICE_CHANGE)],
        ]

        chat_gpt_items = [
            [Sg.Checkbox("履歴をログに出力する",
                         default=self._config.get_advanced_chat_gpt_history_log_enabled(),
                         key=self._config.KEY_ADVANCED_CHAT_GPT_HISTORY_LOG_ENABLED,
                         enable_events=True,
                         )],
        ]

        gui_items = [
            [Sg.Text("アプリタイトル"),
             Sg.InputText(default_text=self._config.get_gui_app_title(),
                          key=self._config.KEY_GUI_APP_TITLE,
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          )],
            [Sg.Text("テーマ"),
             Sg.Combo(values=Sg.theme_list(),
                      default_value=self._config.get_gui_theme_name(),
                      key=self._config.KEY_GUI_THEME_NAME,
                      size=(30, 1),
                      readonly=True,
                      enable_events=True,
                      ),
             Sg.Button("全テーマプレビュー",
                       size=self.BUTTON_SIZE_LONG,
                       key=self._KEY_ADVANCED_GUI_ALL_THEME_PREVIEW),
             ],
        ]

        langchain_items = [
            [Sg.Checkbox("LangChainを使用する",
                         default=self._config.get_advanced_langchain_enabled(),
                         key=self._config.KEY_ADVANCED_LANGCHAIN_ENABLED,
                         enable_events=True,
                         )]
        ]

        link_items = [
            [Sg.Text('OpenAI'),
             self.create_linked_text("Status", "https://status.openai.com/"),
             self.create_linked_text("Usage", "https://platform.openai.com/account/usage")],
        ]

        advanced_tab_layout = [[
            Sg.Column([
                [Sg.Frame("OBS", obs_items, expand_x=True)],
                [Sg.Frame("感情解析", emotion_items, expand_x=True)],
                [Sg.Frame("VMagicMirror連携", v_magic_mirror_items, expand_x=True)],
                [Sg.Frame("ログ", log_level_items, expand_x=True)],
                [Sg.Frame("口パク用第二音声デバイス", secondary_audio_items, expand_x=True)],
                [Sg.Frame("ChatGPT", chat_gpt_items, expand_x=True)],
                [Sg.Frame("LangChain", langchain_items, expand_x=True)],
                [Sg.Frame("GUI", gui_items, expand_x=True)],
                [Sg.Frame("リンク", link_items, expand_x=True)],
            ],
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
            ),
        ]]

        return advanced_tab_layout

    # noinspection PyUnusedLocal
    def __obs_test(self, event, values):
        config = self._config.clone()
        config.set_common_obs_enabled(True)
        try:
            OBSTest(config).run()
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    # noinspection PyUnusedLocal
    def __emotion_test(self, event, values):
        config = self._config.clone()
        text = values[self._KEY_ADVANCED_EMOTION_TEST_TEXT]
        try:
            EmotionTest(config).run(text)
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    def handle_event(self, event, values) -> None:
        match event:
            case self._config.KEY_OBS_HOST:
                self._config.set_obs_host(values[self._config.KEY_OBS_HOST])
            case self._config.KEY_OBS_PORT_NO:
                new_value = self._main_window.input_validation_number_only(event, values)
                self._config.set_obs_port_no(int(new_value))
            case self._config.KEY_OBS_PASSWORD:
                self._config.set_obs_password(values[self._config.KEY_OBS_PASSWORD])
            case self._config.KEY_OBS_AI_UTTERANCE_SOURCE_NAME:
                self._config.set_obs_ai_utterance_source_name(
                    values[self._config.KEY_OBS_AI_UTTERANCE_SOURCE_NAME])
            case self._config.KEY_OBS_USER_UTTERANCE_SOURCE_NAME:
                self._config.set_obs_user_utterance_source_name(
                    values[self._config.KEY_OBS_USER_UTTERANCE_SOURCE_NAME])
            case self._KEY_ADVANCED_OBS_TEST:
                self.__obs_test(event, values)

            case self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_ENABLED:
                self._config.set_pyaudio_secondary_output_enabled(
                    values[self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_ENABLED])
            case self._KEY_ADVANCED_SECONDARY_OUTPUT_DEVICE_CHANGE:
                api_name, device_name = self._change_pyaudio_secondary_output_device()
                if api_name is not None and device_name is not None:
                    self._config.set_pyaudio_secondary_output_api_name(api_name)
                    self._config.set_pyaudio_secondary_output_device_name(device_name)
                    self._main_window.window[self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_API_NAME].update(api_name)
                    self._main_window.window[self._config.KEY_PYAUDIO_SECONDARY_OUTPUT_DEVICE_NAME].update(device_name)

            case self._KEY_ADVANCED_CONSOLE_LOG_LEVEL:
                self._config.set_advanced_console_log_level(self.__get_selected_console_log_level(values))

            case self._config.KEY_GUI_APP_TITLE:
                self._config.set_gui_app_title(values[self._config.KEY_GUI_APP_TITLE])
            case self._config.KEY_GUI_THEME_NAME:
                self._config.set_gui_theme_name(values[self._config.KEY_GUI_THEME_NAME])

            case self._KEY_ADVANCED_GUI_ALL_THEME_PREVIEW:
                Sg.theme_previewer()

            case self._config.KEY_WRIME_EMOTION_SERVER_HOST:
                self._config.set_wrime_emotion_server_host(values[self._config.KEY_WRIME_EMOTION_SERVER_HOST])
            case self._config.KEY_WRIME_EMOTION_SERVER_PORT_NO:
                new_value = self._main_window.input_validation_number_only(event, values)
                self._config.set_wrime_emotion_server_port_no(int(new_value))
            case self._KEY_ADVANCED_EMOTION_TEST:
                self.__emotion_test(event, values)
            case self._config.KEY_ADVANCED_CHAT_GPT_HISTORY_LOG_ENABLED:
                self._config.set_advanced_chat_gpt_history_log_enabled(
                    values[self._config.KEY_ADVANCED_CHAT_GPT_HISTORY_LOG_ENABLED])
            case self._config.KEY_ADVANCED_LANGCHAIN_ENABLED:
                self._config.set_advanced_langchain_enabled(
                    values[self._config.KEY_ADVANCED_LANGCHAIN_ENABLED])
                from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
                self._main_window.update_all_elements_in_window(SettingsLayout.get_key())

    def __get_selected_console_log_level(self, values):
        selected_log_level_key = values[self._KEY_ADVANCED_CONSOLE_LOG_LEVEL]
        return self._log_level_dic[selected_log_level_key]

    def _change_pyaudio_secondary_output_device(self) -> Tuple[Optional[str], Optional[str]]:
        api_name, device_name = None, None
        try:
            window = SecondaryAudioSelectWindow(self._config, self._main_window)
            api_name, device_name = window.display()
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)
        return api_name, device_name
