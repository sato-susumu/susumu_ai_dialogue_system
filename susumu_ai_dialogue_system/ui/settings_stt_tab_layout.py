from __future__ import annotations

from typing import TYPE_CHECKING

import PySimpleGUI as Sg
from loguru import logger

from susumu_ai_dialogue_system.application.common.stt_test import STTTest

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

from susumu_ai_dialogue_system.infrastructure.config import Config, InputFunction
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout
from susumu_ai_dialogue_system.ui.gui_events import GuiEvents


# noinspection PyMethodMayBeStatic
class SettingsSttTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_stt_tab_layout"

    def get_layout(self):
        youtube_pseud_stt_items = [
            [Sg.Text('GCP YouTube Data API v3のAPIキー'),
             Sg.InputText(default_text=self._config.get_gcp_youtube_data_api_key(),
                          key=self._config.KEY_GCP_YOUTUBE_DATA_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [Sg.Text('ライブ配信URL'),
             Sg.InputText(default_text=self._config.get_youtube_live_url(),
                          key=self._config.KEY_YOUTUBE_LIVE_URL,
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [Sg.Button("テスト", size=(15, 1), key=GuiEvents.YOUTUBE_PSEUD_STT_TEST)],
        ]

        google_streaming_stt_items = [
            [Sg.Text('・利用には別途GCP認証もしくは下記APIキーの設定が必要です。')],
            [Sg.Text('Google Speech-to-TextのAPIキー'),
             Sg.InputText(default_text=self._config.get_gcp_speech_to_text_api_key(),
                          key=self._config.KEY_GCP_SPEECH_TO_TEXT_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [Sg.Button("テスト", size=(15, 1), key=GuiEvents.GOOGLE_STREAMING_STT_TEST)],
        ]

        sr_google_stt_items = [
            [Sg.Button("テスト", size=(15, 1), key=GuiEvents.SR_GOOGLE_STT_TEST)],
        ]

        stdin_pseud_stt_items = [
            [Sg.Button("テスト", size=(15, 1), key=GuiEvents.STDIN_PSEUD_STT_TEST)],
        ]

        whisper_api_stt_items = [
            [Sg.Text('・利用には API KEYタブ > OpenAI API Key の入力が必要です。')],
            [Sg.Button("テスト", size=(15, 1), key=GuiEvents.WHISPER_API_STT_TEST)],
        ]

        stt_tab_layout = [
            [Sg.Text('・テスト実行時の内容はコンソールに表示されます。')],
            [Sg.Frame("SpeechRecognition 音声認識(動作確認用)", sr_google_stt_items, expand_x=True)],
            [Sg.Frame("Google Speech-to-Text ストリーミング音声認識", google_streaming_stt_items, expand_x=True)],
            [Sg.Frame("Whisper API 音声認識", whisper_api_stt_items, expand_x=True)],
            [Sg.Frame("YouTube チャット入力取り込み", youtube_pseud_stt_items, expand_x=True)],
            [Sg.Frame("文字入力", stdin_pseud_stt_items, expand_x=True)],
        ]

        return stt_tab_layout

    def update_elements(self) -> None:
        pass

    def __stt_test(self, event, values):
        config = self._config.clone()
        config = self._settings_layout.update_local_config_by_values(values, config)

        if event == GuiEvents.YOUTUBE_PSEUD_STT_TEST:
            config.set_common_input_function(InputFunction.YOUTUBE_PSEUD)
        elif event == GuiEvents.GOOGLE_STREAMING_STT_TEST:
            config.set_common_input_function(InputFunction.GOOGLE_STREAMING)
        elif event == GuiEvents.SR_GOOGLE_STT_TEST:
            config.set_common_input_function(InputFunction.SR_GOOGLE)
        elif event == GuiEvents.STDIN_PSEUD_STT_TEST:
            config.set_common_input_function(InputFunction.STDIN_PSEUD)
        elif event == GuiEvents.WHISPER_API_STT_TEST:
            config.set_common_input_function(InputFunction.WHISPER_API)
        else:
            raise Exception("想定外のイベントです")

        try:
            STTTest(config).run()
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    def handle_event(self, event, values) -> None:
        if event in (GuiEvents.YOUTUBE_PSEUD_STT_TEST, GuiEvents.GOOGLE_STREAMING_STT_TEST,
                     GuiEvents.SR_GOOGLE_STT_TEST, GuiEvents.STDIN_PSEUD_STT_TEST,
                     GuiEvents.WHISPER_API_STT_TEST):
            self.__stt_test(event, values)
