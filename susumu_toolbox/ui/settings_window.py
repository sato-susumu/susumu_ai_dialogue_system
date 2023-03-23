import PySimpleGUI as sg

from susumu_toolbox.application.common.obs_test import OBSTest
from susumu_toolbox.application.common.stt_test import STTTest
from susumu_toolbox.application.common.tts_test import TTSTest
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_window import BaseWindow
from susumu_toolbox.ui.gui_events import GuiEvents


# noinspection PyMethodMayBeStatic
class SettingsWindow(BaseWindow):

    def __init__(self, config: Config):
        super().__init__(config)
        self._current_ai_id = config.get_ai_id_list()[0]

    def _save(self, values: dict) -> None:
        self._config = self._update_config(values, self._config)
        self._config.save()

    def display(self) -> bool:
        base_function_items = [[
            sg.Radio(key=key, text=text, group_id='base', default=self._config.get_common_base_function_key() == key)
        ] for key, text in self._config.base_function_dict.items()]

        input_function_items = [[
            sg.Radio(key=key, text=text, group_id='input', default=self._config.get_common_input_function_key() == key)
        ] for key, text in self._config.input_function_dict.items()]

        chat_function_items = [[
            sg.Radio(key=key, text=text, group_id='chat', default=self._config.get_common_chat_function_key() == key)
        ] for key, text in self._config.chat_function_dict.items()]

        output_function_items = [[
            sg.Radio(key=key, text=text, group_id='output',
                     default=self._config.get_common_output_function_key() == key)
        ] for key, text in self._config.output_function_dict.items()]

        other_function_items = [
            [sg.Checkbox(
                text="OBS出力 (追加設定が必要)",
                key=self._config.KEY_COMMON_OBS_ENABLED,
                default=self._config.get_common_obs_enabled(),
            )],
        ]

        common_tab_layout = [[
            sg.Column([
                [sg.Frame("ベース機能", base_function_items, expand_x=True)],
                [sg.Frame("入力", input_function_items, expand_x=True)],
                [sg.Frame("チャットエンジン", chat_function_items, expand_x=True)],
                [sg.Frame("出力", output_function_items, expand_x=True)],
                [sg.Frame("その他", other_function_items, expand_x=True)],
            ],
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
            ),
        ]]

        openai_items = [
            [sg.Text("OpenAI API Key"),
             sg.InputText(
                 default_text=self._config.get_openai_api_key(),
                 key=self._config.KEY_OPENAI_API_KEY,
                 password_char="*",
                 size=self.INPUT_SIZE_LONG,
             )],
            [sg.Text("API KeyはOpenAIでユーザー登録後、"),
             self.create_linked_text("https://platform.openai.com/account/api-keys",
                                     "https://platform.openai.com/account/api-keys"),
             sg.Text("で作成できます。")],
            [sg.Text("API Keyは他の人に知られないようにご注意ください。")],
        ]
        deepl_items = [
            [sg.Text('DEEPL APIキー',
                     ),
             sg.InputText(
                 default_text=self._config.get_deepl_auth_key(),
                 key=self._config.KEY_DEEPL_AUTH_KEY,
                 password_char="*",
                 size=self.INPUT_SIZE_LONG,
             )],
        ]

        api_keys_tab_layout = [
            [sg.Frame("OpenAI", openai_items, expand_x=True)],
            [sg.Frame("DeepL", deepl_items, expand_x=True, visible=False)],
        ]

        youtube_pseud_stt_items = [
            [sg.Text('GCP YouTube Data API v3のAPIキー'),
             sg.InputText(default_text=self._config.get_gcp_youtube_data_api_key(),
                          key=self._config.KEY_GCP_YOUTUBE_DATA_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [sg.Text('ライブ配信URL'),
             sg.InputText(default_text=self._config.get_youtube_live_url(),
                          key=self._config.KEY_YOUTUBE_LIVE_URL,
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.YOUTUBE_PSEUD_STT_TEST)],
        ]

        google_streaming_stt_items = [
            [sg.Text('Google Speech-to-TextのAPIキー'),
             sg.InputText(default_text=self._config.get_gcp_speech_to_text_api_key(),
                          key=self._config.KEY_GCP_SPEECH_TO_TEXT_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [sg.Text('Google Speech-to-Textを使用するには、GCPの認証もしくは上記APIキーが必要です。')],
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.GOOGLE_STREAMING_STT_TEST)],
        ]

        sr_google_stt_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.SR_GOOGLE_STT_TEST)],
        ]

        stdin_pseud_stt_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.STDIN_PSEUD_STT_TEST)],
        ]

        whisper_api_stt_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.WHISPER_API_STT_TEST)],
        ]

        stt_tab_layout = [
            [sg.Text('テスト実行時の内容はコンソールに表示されます。')],
            [sg.Frame("SpeechRecognition 音声認識(動作確認用)", sr_google_stt_items, expand_x=True)],
            [sg.Frame("Google Speech-to-Text ストリーミング音声認識", google_streaming_stt_items, expand_x=True)],
            [sg.Frame("Whisper API 音声認識", whisper_api_stt_items, expand_x=True)],
            [sg.Frame("YouTube チャット入力取り込み", youtube_pseud_stt_items, expand_x=True)],
            [sg.Frame("文字入力", stdin_pseud_stt_items, expand_x=True)],
        ]

        parlai_items = [
            [sg.Text('アドレス'),
             sg.InputText(key=self._config.KEY_PARLAI_HOST,
                          default_text=self._config.get_parlai_host(),
                          size=self.INPUT_SIZE_NORMAL,
                          )
             ],
            [sg.Text('ポート番号'),
             sg.InputText(key=self._config.KEY_PARLAI_PORT_NO,
                          default_text=self._config.get_parlai_port_no(),
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          )
             ],
        ]

        chat_tab_layout = [
            [sg.Frame("ParlAI", parlai_items, expand_x=True)],
        ]

        voicevox_items = [
            [sg.Text('アドレス'),
             sg.InputText(default_text=self._config.get_voicevox_host(),
                          key=self._config.KEY_VOICEVOX_HOST,
                          size=self.INPUT_SIZE_NORMAL,
                          ),
             ],
            [sg.Text('ポート番号'),
             sg.InputText(default_text=self._config.get_voicevox_port_no(),
                          key=self._config.KEY_VOICEVOX_PORT_NO,
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          ),
             ],
            [sg.Text('スピーカー番号'),
             sg.InputText(default_text=self._config.get_voicevox_speaker_no(),
                          key=self._config.KEY_VOICEVOX_SPEAKER_NO,
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          ),
             ],
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.VOICEVOX_TEST)],
        ]

        gtts_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.GTTS_TEST)],
        ]

        pyttsx3_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.PYTTSX3_TEST)],
        ]

        google_cloud_tts_items = [
            [sg.Text('Google Text-to-SpeechのAPIキー'),
             sg.InputText(default_text=self._config.get_gcp_text_to_speech_api_key(),
                          key=self._config.KEY_GCP_TEXT_TO_SPEECH_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
            [sg.Text('Google Text-to-Speechを使用するには、GCPの認証もしくは上記APIキーが必要です。')],
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.GOOGLE_CLOUD_TTS_TEST)],
        ]

        tts_tab_layout = [
            [sg.Frame("gTTS 音声合成(動作確認用)", gtts_items, expand_x=True)],
            [sg.Frame("VOICEVOX 音声合成", voicevox_items, expand_x=True)],
            [sg.Frame("Google Text-to-Speech 音声合成", google_cloud_tts_items, expand_x=True)],
            [sg.Frame("Pyttsx3 音声合成", pyttsx3_items, expand_x=True)],
        ]

        obs_items = [
            [sg.Text('アドレス'),
             sg.InputText(default_text=self._config.get_obs_host(),
                          key=self._config.KEY_OBS_HOST,
                          size=self.INPUT_SIZE_NORMAL,
                          ),
             ],
            [sg.Text('ポート番号'),
             sg.InputText(default_text=self._config.get_obs_port_no(),
                          key=self._config.KEY_OBS_PORT_NO,
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          ),
             ],
            [sg.Text('パスワード'),
             sg.InputText(default_text=self._config.get_obs_password(),
                          key=self._config.KEY_OBS_PASSWORD,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
            [sg.Text('表示するシーン名'),
             sg.InputText(default_text=self._config.get_obs_scene_name(),
                          key=self._config.KEY_OBS_SCENE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
            [sg.Text('AIの発話を表示するテキスト(GDI+)ソース名'),
             sg.InputText(default_text=self._config.get_obs_ai_utterance_source_name(),
                          key=self._config.KEY_OBS_AI_UTTERANCE_SOURCE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
            [sg.Text('ユーザーの発話を表示するテキスト(GDI+)ソース名'),
             sg.InputText(default_text=self._config.get_obs_user_utterance_source_name(),
                          key=self._config.KEY_OBS_USER_UTTERANCE_SOURCE_NAME,
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.OBS_TEST)],
        ]
        status_items = [
            [sg.Text('OpenAI'), self.create_linked_text("https://status.openai.com/", "https://status.openai.com/")]
        ]

        other_tab_layout = [
            [sg.Frame("OBS", obs_items, expand_x=True)],
            [sg.Frame("APIステータス", status_items, expand_x=True)],
        ]

        # TODO: (低)AI設定の複数対応
        ai_tab_layout = [
            [sg.Text('プロンプト')],
            [sg.Multiline(
                default_text=self._config.get_system_settings_text(self._current_ai_id),
                key=self._config.KEY_AI_SYSTEM_SETTINGS_TEXT,
                expand_x=True,
                expand_y=True
            )]
        ]

        buttons_layout = [
            [
                sg.Button("保存して閉じる", size=(15, 1), key="save"),
                sg.Button('キャンセル', size=self.BUTTON_SIZE_NORMAL, key="cancel"),
            ],
        ]

        window_layout = [
            [sg.TabGroup(
                [
                    [sg.Tab('共通設定', common_tab_layout)],
                    [sg.Tab('API KEY', api_keys_tab_layout, key="api_keys_tab")],
                    [sg.Tab('AI設定', ai_tab_layout)],
                    [sg.Tab('入力', stt_tab_layout)],
                    [sg.Tab('チャットエンジン', chat_tab_layout)],
                    [sg.Tab('出力', tts_tab_layout)],
                    [sg.Tab('その他', other_tab_layout)],
                ],
                # tab_location='left',
                expand_x=True,
                expand_y=True,
            )],
            [sg.Column(buttons_layout, justification='center')],
        ]

        settings_window = sg.Window("設定画面", window_layout,
                                    size=self.WINDOW_SIZE,
                                    finalize=True,
                                    # modal=True,
                                    )
        if self._config.get_openai_api_key() == "":
            settings_window["api_keys_tab"].select()

        while True:
            event, values = settings_window.read()
            if event == sg.WIN_CLOSED:
                close_button_clicked = True
                break
            if event == "save":
                self._save(values)
                close_button_clicked = False
                break
            if event == "cancel":
                # TODO:設定変更後の確認処理実装
                # logout_ret = sg.PopupOKCancel("終了しますか？", title="終了確認", keep_on_top=True)
                # if logout_ret == "OK":
                #     close_button_clicked = False
                #     break
                close_button_clicked = False
                break
            if event in (
                    GuiEvents.VOICEVOX_TEST, GuiEvents.GTTS_TEST, GuiEvents.GOOGLE_CLOUD_TTS_TEST,
                    GuiEvents.PYTTSX3_TEST):
                self._tts_test(event, values)
            if event in (GuiEvents.YOUTUBE_PSEUD_STT_TEST, GuiEvents.GOOGLE_STREAMING_STT_TEST,
                         GuiEvents.SR_GOOGLE_STT_TEST, GuiEvents.STDIN_PSEUD_STT_TEST,
                         GuiEvents.WHISPER_API_STT_TEST):
                self._stt_test(event, values)
            if event == GuiEvents.OBS_TEST:
                self._obs_test(event, values)

            if event in (self._config.KEY_VOICEVOX_PORT_NO, self._config.KEY_VOICEVOX_SPEAKER_NO,
                         self._config.KEY_OBS_PORT_NO, self._config.KEY_PARLAI_PORT_NO):
                self._input_validation_number_only(settings_window, event, values)

            if self.is_linked_text_event(event):
                self.open_linked_text_url(event)

        settings_window.close()
        return close_button_clicked

    def _tts_test(self, event, values) -> None:
        config = self._config.clone()
        config = self._update_config(values, config)

        if event == GuiEvents.VOICEVOX_TEST:
            config.set_common_output_function_key(Config.OUTPUT_FUNCTION_VOICEVOX)
        elif event == GuiEvents.GTTS_TEST:
            config.set_common_output_function_key(Config.OUTPUT_FUNCTION_GTTS)
        elif event == GuiEvents.GOOGLE_CLOUD_TTS_TEST:
            config.set_common_output_function_key(Config.OUTPUT_FUNCTION_GOOGLE_CLOUD)
        elif event == GuiEvents.PYTTSX3_TEST:
            config.set_common_output_function_key(Config.OUTPUT_FUNCTION_PYTTSX3)
        else:
            raise Exception("想定外のイベントです")

        try:
            TTSTest(config).run()
        except Exception as e:
            print(e)
            sg.PopupError(e, title="エラー", keep_on_top=True)

    def _update_config(self, values, target_config) -> Config:
        # API KEY
        target_config.set_openai_api_key(values[self._config.KEY_OPENAI_API_KEY])
        target_config.set_deepl_auth_key(values[self._config.KEY_DEEPL_AUTH_KEY])

        # AI設定
        target_config.set_system_settings_text(self._current_ai_id, values[self._config.KEY_AI_SYSTEM_SETTINGS_TEXT])

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
        if values[self._config.KEY_VOICEVOX_SPEAKER_NO] != "":
            target_config.set_voicevox_speaker_no(int(values[self._config.KEY_VOICEVOX_SPEAKER_NO]))
        target_config.set_gcp_text_to_speech_api_key(values[self._config.KEY_GCP_TEXT_TO_SPEECH_API_KEY])

        # その他
        target_config.set_obs_host(values[self._config.KEY_OBS_HOST])
        if values[self._config.KEY_OBS_PORT_NO] != "":
            target_config.set_obs_port_no(int(values[self._config.KEY_OBS_PORT_NO]))
        target_config.set_obs_password(values[self._config.KEY_OBS_PASSWORD])

        # 共通設定
        [target_config.set_common_base_function_key(key) for key in self._config.base_function_dict.keys() if
         values[key]]
        [target_config.set_common_input_function_key(key) for key in self._config.input_function_dict.keys() if
         values[key]]
        [target_config.set_common_chat_function_key(key) for key in self._config.chat_function_dict.keys() if
         values[key]]
        [target_config.set_common_output_function_key(key)
         for key in self._config.output_function_dict.keys() if values[key]]

        target_config.set_common_obs_enabled(values[self._config.KEY_COMMON_OBS_ENABLED])

        return target_config

    def _stt_test(self, event, values):
        config = self._config.clone()
        config = self._update_config(values, config)

        if event == GuiEvents.YOUTUBE_PSEUD_STT_TEST:
            config.set_common_input_function_key(config.INPUT_FUNCTION_YOUTUBE_PSEUD)
        elif event == GuiEvents.GOOGLE_STREAMING_STT_TEST:
            config.set_common_input_function_key(config.INPUT_FUNCTION_GOOGLE_STREAMING)
        elif event == GuiEvents.SR_GOOGLE_STT_TEST:
            config.set_common_input_function_key(config.INPUT_FUNCTION_SR_GOOGLE)
        elif event == GuiEvents.STDIN_PSEUD_STT_TEST:
            config.set_common_input_function_key(config.INPUT_FUNCTION_STDIN_PSEUD)
        elif event == GuiEvents.WHISPER_API_STT_TEST:
            config.set_common_input_function_key(config.INPUT_FUNCTION_WHISPER_API)
        else:
            raise Exception("想定外のイベントです")

        try:
            STTTest(config).run()
        except Exception as e:
            print(e)
            sg.PopupError(e, title="エラー", keep_on_top=True)

    # noinspection PyUnusedLocal
    def _obs_test(self, event, values):
        config = self._config.clone()
        config = self._update_config(values, config)
        config.set_common_obs_enabled(True)
        try:
            OBSTest(config).run()
        except Exception as e:
            print(e)
            sg.PopupError(e, title="エラー", keep_on_top=True)

    def _input_validation_number_only(self, window, event, values):
        if values[event] and values[event][-1] not in '0123456789':
            window[event].update(values[event][:-1])
