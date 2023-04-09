from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.infrastructure.pyaudio_utility import PyAudioDevice, PyAudioUtility
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout
if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

import PySimpleGUI as Sg


class SecondaryAudioSelectWindow(BaseLayout):
    def __init__(self, config: Config, main_window: MainWindow):
        super().__init__(config, main_window)
        self.__current_ai_id = config.get_ai_id_list()[0]
        self._device_list: list[PyAudioDevice] = self._get_device_list()
        self._item_list: list[str] = self._get_item_list()

    @classmethod
    def get_key(cls) -> str:
        return "secondary_audio_select_window"

    # noinspection PyMethodMayBeStatic
    def _get_device_list(self) -> list[PyAudioDevice]:
        return PyAudioUtility().get_speaker_list()

    def _get_item_list(self) -> list[str]:
        return [f"{i + 1}:{device.host_api_name}-{device.device_name}" for i, device in enumerate(self._device_list)]

    def _get_default_device_key(self) -> Optional[str]:
        api_name = self._config.get_pyaudio_secondary_output_api_name()
        device_name = self._config.get_pyaudio_secondary_output_device_name()
        for key, device in zip(self._item_list, self._device_list):
            if device.host_api_name in api_name and device.device_name in device_name:
                return key
        return None

    # noinspection PyMethodMayBeStatic
    def display(self) -> tuple[Optional[str], Optional[str]]:
        buttons_layout = [[
            Sg.Button('OK', size=self.BUTTON_SIZE_NORMAL),
            Sg.Button('キャンセル', size=self.BUTTON_SIZE_NORMAL),
        ]]

        window_layout = [
            [Sg.Text("デバイスの選択")],
            [Sg.Listbox(self._item_list, size=(80, 20), key='SELECTED')],
            [Sg.Column(buttons_layout, justification='center')],
        ]

        title = self._config.get_gui_app_title()
        window = Sg.Window(title, window_layout, modal=True).Finalize()

        cancel = False
        while True:
            event, values = window.read()

            if event in (Sg.WINDOW_CLOSED, "キャンセル"):
                cancel = True
                break
            elif event == 'OK':
                break

        window.close()

        if cancel:
            return None, None

        selected_item = values['SELECTED'][0]
        device = self._device_list[self._item_list.index(selected_item)]
        return device.host_api_name, device.device_name
