from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.tts.google_cloud_tts import GoogleCloudTTS, GoogleCloudTTSSpeaker
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout
if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

import PySimpleGUI as Sg


# noinspection DuplicatedCode
class GcpTtsSpeakerSelectWindow(BaseLayout):
    __KEY_OK = "OK"
    __KEY_CANCEL = "cancel"
    __KEY_LISTBOX = "listbox"

    def __init__(self, config: Config, main_window: MainWindow):
        super().__init__(config, main_window)
        _tts = GoogleCloudTTS(config)
        speakers = _tts.get_speakers()
        self._display_name_list = [s.display_name for s in speakers]
        self._speaker_name_list = [s.speaker_name for s in speakers]

    @classmethod
    def get_key(cls) -> str:
        return "gcp_tts_speaker_select_window"

    # noinspection PyMethodMayBeStatic
    def display(self) -> Optional[str]:
        buttons_layout = [[
            Sg.Button('OK', size=self.BUTTON_SIZE_NORMAL, key=self.__KEY_OK),
            Sg.Button('キャンセル', size=self.BUTTON_SIZE_NORMAL, key=self.__KEY_CANCEL),
        ]]

        window_layout = [
            [Sg.Text("スピーカーの選択")],
            [Sg.Listbox(self._display_name_list, size=(80, 20), key=self.__KEY_LISTBOX)],
            [Sg.Column(buttons_layout, justification='center')],
        ]

        title = self._config.get_gui_app_title()
        window = Sg.Window(title, window_layout, modal=True).Finalize()

        cancel = False
        while True:
            event, values = window.read()

            if event in (Sg.WINDOW_CLOSED, self.__KEY_CANCEL):
                cancel = True
                break
            elif event == self.__KEY_OK:
                break

        window.close()

        if cancel:
            return None

        selected_item = values[self.__KEY_LISTBOX][0]
        speaker_name = self._speaker_name_list[self._display_name_list.index(selected_item)]
        return speaker_name

