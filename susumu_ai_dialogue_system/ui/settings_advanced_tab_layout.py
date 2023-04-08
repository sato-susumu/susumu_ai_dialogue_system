from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from susumu_ai_dialogue_system.application.common.emotion_test import EmotionTest
from susumu_ai_dialogue_system.application.common.obs_test import OBSTest

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout
from susumu_ai_dialogue_system.ui.gui_events import GuiEvents

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
                          ),
             ],
            [Sg.Text('AIの発話を表示するテキスト(GDI+)ソース名'),
             Sg.InputText(default_text=self._config.get_obs_ai_utterance_source_name(),
                          key=self._config.KEY_OBS_AI_UTTERANCE_SOURCE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
            [Sg.Text('ユーザーの発話を表示するテキスト(GDI+)ソース名'),
             Sg.InputText(default_text=self._config.get_obs_user_utterance_source_name(),
                          key=self._config.KEY_OBS_USER_UTTERANCE_SOURCE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
            [Sg.Button("テスト", size=(15, 1), key=GuiEvents.OBS_TEST)],
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
                         )
            ]
        ]

        gui_items = [
            [Sg.Text("アプリタイトル"),
             Sg.InputText(default_text=self._config.get_gui_app_title(),
                          key=self._config.KEY_GUI_APP_TITLE,
                          size=self.INPUT_SIZE_LONG,
                          )],
            [Sg.Text("テーマ"),
             Sg.Combo(values=Sg.theme_list(),
                      default_value=self._config.get_gui_theme_name(),
                      key=self._config.KEY_GUI_THEME_NAME,
                      size=(30, 1),
                      readonly=True,
                      ),
             Sg.Button("全テーマプレビュー",
                       size=self.BUTTON_SIZE_LONG,
                       key=self._KEY_ADVANCED_GUI_ALL_THEME_PREVIEW),
             ],
        ]

        status_items = [
            [Sg.Text('OpenAI'), self.create_linked_text("https://status.openai.com/", "https://status.openai.com/")]
        ]

        advanced_tab_layout = [[
            Sg.Column([
                [Sg.Frame("OBS", obs_items, expand_x=True)],
                [Sg.Frame("感情解析", emotion_items, expand_x=True)],
                [Sg.Frame("VMagicMirror連携", v_magic_mirror_items, expand_x=True)],
                [Sg.Frame("ログ", log_level_items, expand_x=True)],
                [Sg.Frame("GUI", gui_items, expand_x=True)],
                [Sg.Frame("APIステータス", status_items, expand_x=True)],
            ],
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
            ),
        ]]

        return advanced_tab_layout

    def update_elements(self) -> None:
        pass

    # noinspection PyUnusedLocal
    def __obs_test(self, event, values):
        config = self._config.clone()
        config = self._settings_layout.update_local_config_by_values(values, config)
        config.set_common_obs_enabled(True)
        try:
            OBSTest(config).run()
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    def __emotion_test(self, event, values):
        config = self._config.clone()
        config = self._settings_layout.update_local_config_by_values(values, config)

        text = values[self._KEY_ADVANCED_EMOTION_TEST_TEXT]
        try:
            EmotionTest(config).run(text)
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    def handle_event(self, event, values) -> None:
        if event == self._config.KEY_OBS_PORT_NO:
            self._main_window.input_validation_number_only(event, values)

        if event == self._config.KEY_WRIME_EMOTION_SERVER_PORT_NO:
            self._main_window.input_validation_number_only(event, values)

        if event == GuiEvents.OBS_TEST:
            self.__obs_test(event, values)

        if event == self._KEY_ADVANCED_EMOTION_TEST:
            self.__emotion_test(event, values)

        if event == self._KEY_ADVANCED_GUI_ALL_THEME_PREVIEW:
            Sg.theme_previewer()

    def get_selected_console_log_level(self, values):
        selected_log_level_key = values[self._KEY_ADVANCED_CONSOLE_LOG_LEVEL]
        return self._log_level_dic[selected_log_level_key]
