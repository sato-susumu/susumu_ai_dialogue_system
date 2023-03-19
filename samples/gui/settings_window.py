import PySimpleGUI as sg

from samples.gui.base_window import BaseWindow
from samples.gui.gui_events import GuiEvents
from samples.gui.obs_test import OBSTest
from samples.gui.stt_test import STTTest
from samples.gui.tts_test import TTSTest
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class SettingsWindow(BaseWindow):

    def __init__(self, config: Config):
        super().__init__(config)

    def _save(self, values: dict) -> None:
        self._config = self._update_config(values, self._config)
        self._config.save()

    _base_function_items_dic = {
        Config.BASE_FUNCTION_VOICE_DIALOGUE: "音声対話",
        Config.BASE_FUNCTION_AI_TUBER: "AITuber",
        Config.BASE_FUNCTION_TEXT_DIALOGUE: "文字対話",
    }
    _input_function_items_dic = {
        Config.INPUT_FUNCTION_SR_GOOGLE: "サンプル音声認識",
        Config.INPUT_FUNCTION_STDIN_PSEUD: "文字入力",
        Config.INPUT_FUNCTION_GOOGLE_STREAMING: "Googleストリーミング音声認識 (追加設定が必要)",
        Config.INPUT_FUNCTION_YOUTUBE_PSEUD: "YouTubeコメント取得 (追加設定が必要)",
    }
    _output_function_items_dic = {
        Config.OUTPUT_FUNCTION_PYTTSX3: "サンプル音声合成 pyttsx3",
        Config.OUTPUT_FUNCTION_VOICEVOX: "VOICEVOX (VOICEVOXアプリ起動が必要)",
        Config.OUTPUT_FUNCTION_GOOGLE_CLOUD: "Google音声合成 (追加設定が必要)",
        Config.OUTPUT_FUNCTION_GTTS: "サンプル音声合成 gTTS",
    }

    def display(self) -> bool:
        base_function_items = [[
            sg.Radio(key=key, text=text, group_id='base', default=self._config.get_common_base_function() == key)
        ] for key, text in self._base_function_items_dic.items()]

        input_function_items = [[
            sg.Radio(key=key, text=text, group_id='input', default=self._config.get_common_input_function() == key)
        ] for key, text in self._input_function_items_dic.items()]

        output_function_items = [[
            sg.Radio(key=key, text=text, group_id='output', default=self._config.get_common_output_function() == key)
        ] for key, text in self._output_function_items_dic.items()]

        other_function_items = [
            [sg.Checkbox(
                text="OBS出力 (追加設定が必要)",
                key=self._config.KEY_COMMON_OBS_ENABLED,
                default=self._config.get_common_obs_enabled(),
            )],
        ]

        common_tab_layout = [
            [sg.Frame("ベース機能", base_function_items)],
            [sg.Frame("入力", input_function_items)],
            [sg.Frame("出力", output_function_items)],
            [sg.Frame("その他", other_function_items)],
        ]

        api_keys_tab_layout = [
            [sg.Text("OpenAI APIキー"),
             sg.InputText(
                 default_text=self._config.get_openai_api_key(),
                 key=self._config.KEY_OPENAI_API_KEY,
                 password_char="*",
                 size=self.INPUT_SIZE_LONG,
             )],
            [sg.Text('DEEPL APIキー',
                     visible=False,
                     ),
             sg.InputText(
                 default_text=self._config.get_deepl_auth_key(),
                 key=self._config.KEY_DEEPL_AUTH_KEY,
                 password_char="*",
                 size=self.INPUT_SIZE_LONG,
                 visible=False,
             )],
        ]

        youtube_pseud_stt_items = [
            [sg.Text('YouTube Data API v3キー'),
             sg.InputText(default_text=self._config.get_youtube_api_key(),
                          key=self._config.KEY_YOUTUBE_API_KEY,
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
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.GOOGLE_STREAMING_STT_TEST)],
        ]

        sr_google_stt_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.SR_GOOGLE_STT_TEST)],
        ]

        stdin_pseud_stt_items = [
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.STDIN_PSEUD_STT_TEST)],
        ]

        stt_tab_layout = [
            [sg.Frame("SpeechRecognition(Google)", sr_google_stt_items)],
            [sg.Frame("YouTube チャット入力取り込み", youtube_pseud_stt_items)],
            [sg.Frame("Googleストリーミング音声認識", google_streaming_stt_items)],
            [sg.Frame("文字入力", stdin_pseud_stt_items)],
        ]

        parlai_items = [
            [sg.Text('アドレス'),
             sg.InputText(key="parlai_host",
                          size=self.INPUT_SIZE_NORMAL,
                          )
             ],
            [sg.Text('ポート番号'),
             sg.InputText(key="parlai_prot_no",
                          size=self.INPUT_SIZE_SHORT,
                          )
             ],
        ]

        chat_tab_layout = [
            [sg.Frame("ParlAI", parlai_items)],
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
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.GOOGLE_CLOUD_TTS_TEST)],
        ]

        tts_tab_layout = [
            [sg.Frame("gTTS (動作確認用)", gtts_items)],
            [sg.Frame("VOICEVOX", voicevox_items)],
            [sg.Frame("Google TTS", google_cloud_tts_items)],
            [sg.Frame("Pyttsx3", pyttsx3_items)],
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
            [sg.Button("テスト", size=(15, 1), key=GuiEvents.OBS_TEST)],
        ]

        other_tab_layout = [
            [sg.Frame("OBS", obs_items)],
        ]

        ai_tab_layout = [
            [sg.Text('タブ5のコンテンツ')]
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
                    [sg.Tab('API KEY', api_keys_tab_layout)],
                    # [sg.Tab('AI設定', ai_tab_layout)],
                    [sg.Tab('入力', stt_tab_layout)],
                    # [sg.Tab('チャットエンジン', chat_tab_layout)],
                    [sg.Tab('音声合成', tts_tab_layout)],
                    [sg.Tab('その他', other_tab_layout, )],
                ],
                # tab_location='left',
            )],
            [sg.Column(buttons_layout, justification='center')],
        ]

        settings_window = sg.Window("設定画面", window_layout,
                                    size=self.WINDOW_SIZE,
                                    # modal=True,
                                    )

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
                         GuiEvents.SR_GOOGLE_STT_TEST, GuiEvents.STDIN_PSEUD_STT_TEST):
                self._stt_test(event, values)
            if event == GuiEvents.OBS_TEST:
                self._obs_test(event, values)
            if event == self._config.KEY_VOICEVOX_PORT_NO:
                self._input_validation_number_only(settings_window, self._config.KEY_VOICEVOX_PORT_NO, values)
            if event == self._config.KEY_VOICEVOX_SPEAKER_NO:
                self._input_validation_number_only(settings_window, self._config.KEY_VOICEVOX_SPEAKER_NO, values)
            if event == self._config.KEY_OBS_PORT_NO:
                self._input_validation_number_only(settings_window, self._config.KEY_OBS_PORT_NO, values)
        settings_window.close()
        return close_button_clicked

    def _tts_test(self, event, values) -> None:
        config = self._config.clone()
        config = self._update_config(values, config)

        if event == GuiEvents.VOICEVOX_TEST:
            config.set_common_output_function(Config.OUTPUT_FUNCTION_VOICEVOX)
        elif event == GuiEvents.GTTS_TEST:
            config.set_common_output_function(Config.OUTPUT_FUNCTION_GTTS)
        elif event == GuiEvents.GOOGLE_CLOUD_TTS_TEST:
            config.set_common_output_function(Config.OUTPUT_FUNCTION_GOOGLE_CLOUD)
        elif event == GuiEvents.PYTTSX3_TEST:
            config.set_common_output_function(Config.OUTPUT_FUNCTION_PYTTSX3)
        else:
            raise Exception("想定外のイベントです")

        try:
            TTSTest(config).run()
        except Exception as e:
            sg.PopupError(e, title="エラー", keep_on_top=True)

    def _update_config(self, values, target_config) -> Config:
        # API KEY
        target_config.set_openai_api_key(values[self._config.KEY_OPENAI_API_KEY])
        target_config.set_deepl_auth_key(values[self._config.KEY_DEEPL_AUTH_KEY])

        # 入力
        target_config.set_youtube_live_url(values[self._config.KEY_YOUTUBE_LIVE_URL])
        target_config.set_youtube_api_key(values[self._config.KEY_YOUTUBE_API_KEY])

        # 出力
        target_config.set_voicevox_host(values[self._config.KEY_VOICEVOX_HOST])
        if values[self._config.KEY_VOICEVOX_PORT_NO] != "":
            target_config.set_voicevox_port_no(int(values[self._config.KEY_VOICEVOX_PORT_NO]))
        if values[self._config.KEY_VOICEVOX_SPEAKER_NO] != "":
            target_config.set_voicevox_speaker_no(int(values[self._config.KEY_VOICEVOX_SPEAKER_NO]))

        # その他
        target_config.set_obs_host(values[self._config.KEY_OBS_HOST])
        if values[self._config.KEY_OBS_PORT_NO] != "":
            target_config.set_obs_port_no(int(values[self._config.KEY_OBS_PORT_NO]))
        target_config.set_obs_password(values[self._config.KEY_OBS_PASSWORD])

        [target_config.set_common_base_function(key) for key in self._base_function_items_dic.keys() if values[key]]
        [target_config.set_common_input_function(key) for key in self._input_function_items_dic.keys() if values[key]]
        [target_config.set_common_output_function(key) for key in self._output_function_items_dic.keys() if values[key]]

        target_config.set_common_obs_enabled(values[self._config.KEY_COMMON_OBS_ENABLED])

        return target_config

    def _stt_test(self, event, values):
        config = self._config.clone()
        config = self._update_config(values, config)

        if event == GuiEvents.YOUTUBE_PSEUD_STT_TEST:
            config.set_common_input_function(config.INPUT_FUNCTION_YOUTUBE_PSEUD)
        elif event == GuiEvents.GOOGLE_STREAMING_STT_TEST:
            config.set_common_input_function(config.INPUT_FUNCTION_GOOGLE_STREAMING)
        elif event == GuiEvents.SR_GOOGLE_STT_TEST:
            config.set_common_input_function(config.INPUT_FUNCTION_SR_GOOGLE)
        elif event == GuiEvents.STDIN_PSEUD_STT_TEST:
            config.set_common_input_function(config.INPUT_FUNCTION_STDIN_PSEUD)
        else:
            raise Exception("想定外のイベントです")

        try:
            STTTest(config).run()
        except Exception as e:
            sg.PopupError(e, title="エラー", keep_on_top=True)

    def _obs_test(self, event, values):
        config = self._config.clone()
        config = self._update_config(values, config)
        try:
            OBSTest(config).run()
        except Exception as e:
            sg.PopupError(e, title="エラー", keep_on_top=True)

    def _input_validation_number_only(self, window, event, values):
        if values[event] and values[event][-1] not in '0123456789':
            window[event].update(values[event][:-1])
