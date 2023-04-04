from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from susumu_toolbox.application.common.obs_test import OBSTest

if TYPE_CHECKING:
    from susumu_toolbox.ui.settings_layout import SettingsLayout
    from susumu_toolbox.ui.main_window import MainWindow

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_layout import BaseLayout
from susumu_toolbox.ui.gui_events import GuiEvents

import PySimpleGUI as Sg


# noinspection PyMethodMayBeStatic
class SettingsOtherTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_other_tab_layout"

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
            [Sg.Text('・感情解析のモデル入手と配置が必要です。')],
        ]

        v_magic_mirror_items = [
            [Sg.Text('・VMagicMirrorの起動と事前の設定が必要です。')],
        ]

        status_items = [
            [Sg.Text('OpenAI'), self.create_linked_text("https://status.openai.com/", "https://status.openai.com/")]
        ]

        other_tab_layout = [
            [Sg.Frame("OBS", obs_items, expand_x=True)],
            [Sg.Frame("感情解析", emotion_items, expand_x=True)],
            [Sg.Frame("VMagicMirror連携", v_magic_mirror_items, expand_x=True)],
            [Sg.Frame("APIステータス", status_items, expand_x=True)],
        ]

        return other_tab_layout

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

    def handle_event(self, event, values) -> None:
        if event == self._config.KEY_OBS_PORT_NO:
            self._main_window.window.input_validation_number_only(event, values)

        if event == GuiEvents.OBS_TEST:
            self.__obs_test(event, values)
