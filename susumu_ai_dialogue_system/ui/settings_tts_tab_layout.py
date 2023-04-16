from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from susumu_ai_dialogue_system.ui.gcp_tts_speaker_select_window import GcpTtsSpeakerSelectWindow

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

import PySimpleGUI as Sg
from loguru import logger

from susumu_ai_dialogue_system.application.common.tts_test import TTSTest
from susumu_ai_dialogue_system.infrastructure.config import Config, OutputFunction
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout


# noinspection PyMethodMayBeStatic
class SettingsTtsTabLayout(BaseLayout):
    _KEY_TTS_VOICEVOX_TEST = "key_tts_voicevox_test"
    _KEY_TTS_GTTS_TEST = "key_tts_gtts_test"
    _KEY_TTS_GCP_TTS_TEST = "key_tts_gcp_tts_test"
    _KEY_TTS_GCP_TTS_CHANGE_SPEAKER_NAME = "key_tts_gcp_tts_change_speaker_name"
    _KEY_TTS_PYTTSX3_TEST = "key_tts_pyttsx3_test"
    _KEY_TTS_VOICEVOX_SPEAKER_COMBO = 'key_tts_voicevox_speaker_combo'
    _KEY_TTS_PLAY_TEXT = "key_tts_play_text"
    # VOICEVOXのスピーカーリスト。
    # TODO: 選択した名前はconfigに保存し、Windowに表示する。設定ボタンを追加し、押したときに動的にスピーカーを取得する
    _voicevox_speaker_dic = {'四国めたん-ノーマル': 2, '四国めたん-あまあま': 0, '四国めたん-ツンツン': 6,
                             '四国めたん-セクシー': 4, '四国めたん-ささやき': 36, '四国めたん-ヒソヒソ': 37,
                             'ずんだもん-ノーマル': 3, 'ずんだもん-あまあま': 1, 'ずんだもん-ツンツン': 7,
                             'ずんだもん-セクシー': 5, 'ずんだもん-ささやき': 22, 'ずんだもん-ヒソヒソ': 38,
                             '春日部つむぎ-ノーマル': 8, '雨晴はう-ノーマル': 10, '波音リツ-ノーマル': 9,
                             '玄野武宏-ノーマル': 11, '玄野武宏-喜び': 39, '玄野武宏-ツンギレ': 40,
                             '玄野武宏-悲しみ': 41, '白上虎太郎-ふつう': 12, '白上虎太郎-わーい': 32,
                             '白上虎太郎-びくびく': 33, '白上虎太郎-おこ': 34, '白上虎太郎-びえーん': 35,
                             '青山龍星-ノーマル': 13, '冥鳴ひまり-ノーマル': 14, '九州そら-ノーマル': 16,
                             '九州そら-あまあま': 15, '九州そら-ツンツン': 18, '九州そら-セクシー': 17,
                             '九州そら-ささやき': 19, 'もち子さん-ノーマル': 20, '剣崎雌雄-ノーマル': 21,
                             'WhiteCUL-ノーマル': 23, 'WhiteCUL-たのしい': 24, 'WhiteCUL-かなしい': 25,
                             'WhiteCUL-びえーん': 26, '後鬼-人間ver.': 27, '後鬼-ぬいぐるみver.': 28,
                             'No.7-ノーマル': 29, 'No.7-アナウンス': 30, 'No.7-読み聞かせ': 31,
                             'ちび式じい-ノーマル': 42, '櫻歌ミコ-ノーマル': 43,
                             '櫻歌ミコ-第二形態': 44, '櫻歌ミコ-ロリ': 45, '小夜/SAYO-ノーマル': 46,
                             'ナースロボ＿タイプＴ-ノーマル': 47, 'ナースロボ＿タイプＴ-楽々': 48,
                             'ナースロボ＿タイプＴ-恐怖': 49, 'ナースロボ＿タイプＴ-内緒話': 50}

    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_tts_tab_layout"

    def get_layout(self):
        default_speaker_no = self._config.get_voicevox_speaker_no()
        default_speaker_key = [k for k, v in self._voicevox_speaker_dic.items() if v == default_speaker_no][0]

        voicevox_items = [
            [Sg.Text('・利用にはVOICEVOXの起動が必要です。')],
            [Sg.Text('アドレス'),
             Sg.InputText(default_text=self._config.get_voicevox_host(),
                          key=self._config.KEY_VOICEVOX_HOST,
                          size=self.INPUT_SIZE_NORMAL,
                          enable_events=True,
                          ),
             ],
            [Sg.Text('ポート番号'),
             Sg.InputText(default_text=self._config.get_voicevox_port_no(),
                          key=self._config.KEY_VOICEVOX_PORT_NO,
                          size=self.INPUT_SIZE_SHORT,
                          enable_events=True,
                          ),
             ],
            [Sg.Combo(list(self._voicevox_speaker_dic.keys()),
                      default_value=default_speaker_key,
                      key=self._KEY_TTS_VOICEVOX_SPEAKER_COMBO,
                      size=(30, 1),
                      readonly=True,
                      enable_events=True,
                      ),
             ],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_TTS_VOICEVOX_TEST)],
        ]

        gtts_items = [
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_TTS_GTTS_TEST)],
        ]

        pyttsx3_items = [
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_TTS_PYTTSX3_TEST)],
        ]

        gcp_speaker_name = self._config.get_gcp_text_to_speech_speaker_name()
        google_cloud_tts_items = [
            [Sg.Text('・利用には別途GCP認証もしくは下記APIキーの設定が必要です。')],
            [Sg.Text('Google Text-to-SpeechのAPIキー'),
             Sg.InputText(default_text=self._config.get_gcp_text_to_speech_api_key(),
                          key=self._config.KEY_GCP_TEXT_TO_SPEECH_API_KEY,
                          password_char="*",
                          size=self.INPUT_SIZE_LONG,
                          enable_events=True,
                          )
             ],
            [Sg.Text('スピーカー名:'),
             Sg.Text(gcp_speaker_name,
                     key=self._config.KEY_GCP_TEXT_TO_SPEECH_SPEAKER_NAME),
             Sg.Button("スピーカー変更", size=(15, 1), key=self._KEY_TTS_GCP_TTS_CHANGE_SPEAKER_NAME)
             ],
            [Sg.Button("テスト", size=(15, 1), key=self._KEY_TTS_GCP_TTS_TEST)],
        ]

        tts_tab_layout = [
            [Sg.Frame("サンプル音声合成 pyttsx3", pyttsx3_items, expand_x=True)],
            [Sg.Frame("VOICEVOX 音声合成", voicevox_items, expand_x=True)],
            [Sg.Frame("Google Text-to-Speech 音声合成", google_cloud_tts_items, expand_x=True)],
            [Sg.Frame("サンプル音声合成 gTTS", gtts_items, expand_x=True)],
            [
                Sg.Text("テスト再生用文字列"),
                Sg.Multiline(default_text="音声合成の再生テストです",
                             key=self._KEY_TTS_PLAY_TEXT,
                             expand_x=True,
                             size=(50, 3),
                             horizontal_scroll=False,
                             enable_events=True,
                             ),
            ],
        ]
        return tts_tab_layout

    def __tts_test(self, event, values) -> None:
        config = self._config.clone()
        if event == self._KEY_TTS_VOICEVOX_TEST:
            config.set_common_output_function(OutputFunction.VOICEVOX)
        elif event == self._KEY_TTS_GTTS_TEST:
            config.set_common_output_function(OutputFunction.GTTS)
        elif event == self._KEY_TTS_GCP_TTS_TEST:
            config.set_common_output_function(OutputFunction.GOOGLE_CLOUD)
        elif event == self._KEY_TTS_PYTTSX3_TEST:
            config.set_common_output_function(OutputFunction.PYTTSX3)
        else:
            raise Exception("想定外のイベントです")

        text = values[self._KEY_TTS_PLAY_TEXT]
        try:
            TTSTest(config).run(text)
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)

    # noinspection PyUnusedLocal
    def _change_gcp_tts_speaker_name(self, values) -> Optional[str]:
        speaker_name = None
        try:
            window = GcpTtsSpeakerSelectWindow(self._config, self._main_window)
            speaker_name = window.display()
        except Exception as e:
            logger.error(e)
            Sg.PopupError(e, title="エラー", keep_on_top=True)
        return speaker_name

    def handle_event(self, event, values) -> None:
        match event:
            case self._config.KEY_VOICEVOX_HOST:
                self._config.set_voicevox_host(values[self._config.KEY_VOICEVOX_HOST])
            case self._config.KEY_VOICEVOX_PORT_NO:
                new_value = self._main_window.input_validation_number_only(event, values)
                self._config.set_voicevox_port_no(int(new_value))
            case self._KEY_TTS_VOICEVOX_SPEAKER_COMBO:
                selected_speaker_key = values[self._KEY_TTS_VOICEVOX_SPEAKER_COMBO]
                speaker_no = self._voicevox_speaker_dic[selected_speaker_key]
                self._config.set_voicevox_speaker_no(speaker_no)
            case self._config.KEY_GCP_TEXT_TO_SPEECH_API_KEY:
                self._config.set_gcp_text_to_speech_api_key(values[self._config.KEY_GCP_TEXT_TO_SPEECH_API_KEY])
            case self._KEY_TTS_GCP_TTS_CHANGE_SPEAKER_NAME:
                new_speaker_name = self._change_gcp_tts_speaker_name(values)
                if new_speaker_name is not None:
                    self._config.set_gcp_text_to_speech_speaker_name(new_speaker_name)
                    self._main_window.window[self._config.KEY_GCP_TEXT_TO_SPEECH_SPEAKER_NAME].update(
                        new_speaker_name)

        if event in (
                self._KEY_TTS_VOICEVOX_TEST, self._KEY_TTS_GTTS_TEST, self._KEY_TTS_GCP_TTS_TEST,
                self._KEY_TTS_PYTTSX3_TEST):
            self.__tts_test(event, values)
