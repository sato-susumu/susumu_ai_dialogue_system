import PySimpleGUI as sg

from samples.gui.base_window import BaseWindow
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class SettingsWindow(BaseWindow):
    # TODO: 最終的にはConfigで定義して参照する
    _OPEN_AI_API_KEY = "openai_api_key"

    def __init__(self, config: Config):
        super().__init__(config)

    def _save(self, values: dict) -> None:
        self._config.set_openai_api_key(values[self._config.KEY_OPENAI_API_KEY])
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

        youtube_items = [
            [sg.Text('ライブ配信URL'),
             sg.InputText(key="youtube_live_url",
                          size=self.INPUT_SIZE_LONG,
                          )
             ],
        ]

        stt_tab_layout = [
            [sg.Frame("YouTube チャット入力取り込み", youtube_items)],
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
             sg.InputText(key="voicevox_host",
                          size=self.INPUT_SIZE_NORMAL,
                          ),
             ],
            [sg.Text('ポート番号'),
             sg.InputText(key="voicevox_prot_no",
                          size=self.INPUT_SIZE_SHORT,
                          ),
             ],
            [sg.Text('スピーカー番号'),
             sg.InputText(key="voicevox_speaker_no",
                          size=self.INPUT_SIZE_SHORT,
                          ),
             ],
        ]

        tts_tab_layout = [
            [sg.Frame("VOICEVOX", voicevox_items)],
        ]

        obs_items = [
            [sg.Text('アドレス'),
             sg.InputText(key="obs_host",
                          size=self.INPUT_SIZE_NORMAL,
                          ),
             ],
            [sg.Text('ポート番号'),
             sg.InputText(key="obs_port_no",
                          size=self.INPUT_SIZE_SHORT,
                          ),
             ],
            [sg.Text('パスワード'),
             sg.InputText(key="obs_password",
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          ),
             ],
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
                    # [sg.Tab('入力', stt_tab_layout)],
                    # [sg.Tab('チャットエンジン', chat_tab_layout)],
                    # [sg.Tab('音声合成', tts_tab_layout)],
                    # [sg.Tab('その他', other_tab_layout, )],
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

        settings_window.close()
        return close_button_clicked
