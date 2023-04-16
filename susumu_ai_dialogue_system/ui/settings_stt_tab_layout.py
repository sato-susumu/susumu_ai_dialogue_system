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


# noinspection PyMethodMayBeStatic
class SettingsSttTabLayout(BaseLayout):
    _KEY_STT_YOUTUBE_PSEUD_STT_TEST = "key_stt_youtube_pseud_stt_test"
    _KEY_STT_GOOGLE_STREAMING_STT_TEST = "key_stt_google_streaming_stt_test"
    _KEY_STT_SR_GOOGLE_STT_TEST = "key_stt_sr_google_stt_test"
    _KEY_STT_STDIN_PSEUD_STT_TEST = "key_stt_stdin_pseud_stt_test"
    _KEY_STT_WHISPER_API_STT_TEST = "key_stt_whisper_api_stt_test"

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
                          enable_events=True,
                          )
             ],
            [Sg.Text('ライブ配信URL'),
             Sg.InputText(default_text=self._config.get_youtube_live_url(),
                          key=self._config.KEY_YOUTUBE_LIVE_URL,
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          )
             ],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_STT_YOUTUBE_PSEUD_STT_TEST)],
        ]

        google_streaming_stt_items = [
            [Sg.Text('・利用には別途GCP認証もしくは下記APIキーの設定が必要です。')],
            [Sg.Text('Google Speech-to-TextのAPIキー'),
             Sg.InputText(default_text=self._config.get_gcp_speech_to_text_api_key(),
                          key=self._config.KEY_GCP_SPEECH_TO_TEXT_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          )
             ],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_STT_GOOGLE_STREAMING_STT_TEST)],
        ]

        sr_google_stt_items = [
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_STT_SR_GOOGLE_STT_TEST)],
        ]

        stdin_pseud_stt_items = [
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_STT_STDIN_PSEUD_STT_TEST)],
        ]

        whisper_api_stt_items = [
            [Sg.Text('・利用には API KEYタブ > OpenAI API Key の入力が必要です。')],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_STT_WHISPER_API_STT_TEST)],
        ]

        stt_tab_layout = [
            [Sg.Text('・テスト実行時の内容はコンソールに表示されます。')],
            [Sg.Frame("サンプル音声認識 SpeechRecognition", sr_google_stt_items, expand_x=True)],
            [Sg.Frame("文字入力", stdin_pseud_stt_items, expand_x=True)],
            [Sg.Frame("Google Speech-to-Text ストリーミング音声認識", google_streaming_stt_items, expand_x=True)],
            [Sg.Frame("Whisper API音声認識", whisper_api_stt_items, expand_x=True)],
            [Sg.Frame("YouTube ライブチャット入力取り込み", youtube_pseud_stt_items, expand_x=True)],
        ]

        return stt_tab_layout

    # noinspection PyUnusedLocal
    def __stt_test(self, event, values):
        config = self._config.clone()
        match event:
            case self._KEY_STT_YOUTUBE_PSEUD_STT_TEST:
                config.set_common_input_function(InputFunction.YOUTUBE_PSEUD)
            case self._KEY_STT_GOOGLE_STREAMING_STT_TEST:
                config.set_common_input_function(InputFunction.GOOGLE_STREAMING)
            case self._KEY_STT_SR_GOOGLE_STT_TEST:
                config.set_common_input_function(InputFunction.SR_GOOGLE)
            case self._KEY_STT_STDIN_PSEUD_STT_TEST:
                config.set_common_input_function(InputFunction.STDIN_PSEUD)
            case self._KEY_STT_WHISPER_API_STT_TEST:
                config.set_common_input_function(InputFunction.WHISPER_API)
            case _:
                raise Exception("想定外のイベントです")

        try:
            STTTest(config).run()
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    def handle_event(self, event, values) -> None:
        match event:
            case self._config.KEY_GCP_YOUTUBE_DATA_API_KEY:
                self._config.set_gcp_youtube_data_api_key(values[self._config.KEY_GCP_YOUTUBE_DATA_API_KEY])
            case self._config.KEY_YOUTUBE_LIVE_URL:
                self._config.set_youtube_live_url(values[self._config.KEY_YOUTUBE_LIVE_URL])
            case self._config.KEY_GCP_SPEECH_TO_TEXT_API_KEY:
                self._config.set_gcp_speech_to_text_api_key(values[self._config.KEY_GCP_SPEECH_TO_TEXT_API_KEY])

        if event in (self._KEY_STT_YOUTUBE_PSEUD_STT_TEST, self._KEY_STT_GOOGLE_STREAMING_STT_TEST,
                     self._KEY_STT_SR_GOOGLE_STT_TEST, self._KEY_STT_STDIN_PSEUD_STT_TEST,
                     self._KEY_STT_WHISPER_API_STT_TEST):
            self.__stt_test(event, values)
