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

    def display(self) -> bool:
        common_tab_layout = [
            [sg.Text("common")],
        ]
        api_keys_tab_layout = [
            [sg.Text("OpenAI APIキー"),
             sg.InputText(
                 self._config.get_openai_api_key(),
                 size=self.INPUT_SIZE_LONG,
                 password_char="*",
                 key=self._config.KEY_OPENAI_API_KEY)],
            # [sg.Text('GCP APIキー'),
            #  sg.InputText(key="gcp_api_key",
            #               password_char="*",
            #               size=self.INPUT_SIZE_LONG,
            #               )
            #  ],
            # [sg.Text('DEEPL APIキー'),
            #  sg.InputText(key="deepl_auth_key",
            #               password_char="*",
            #               size=self.INPUT_SIZE_LONG,
            #               )
            #  ],
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
                    # [sg.Tab('共通設定', common_tab_layout)],
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
        try:
            TTSTest(config).run(event)
        except Exception as e:
            sg.PopupError(e, title="エラー", keep_on_top=True)

    def _update_config(self, values, target_config) -> Config:
        # API KEY
        target_config.set_openai_api_key(values[self._config.KEY_OPENAI_API_KEY])

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
        return target_config

    def _stt_test(self, event, values):
        config = self._config.clone()
        config = self._update_config(values, config)
        try:
            STTTest(config).run(event)
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
