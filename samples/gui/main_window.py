import PySimpleGUI as sg

from samples.ai_tuber_sample import AiTuberSample
from samples.gui.base_window import BaseWindow
from samples.gui.settings_window import SettingsWindow
from samples.text_chat_sample import TextChatSample
from samples.voice_chat_sample import VoiceChatSample
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class MainWindow(BaseWindow):
    def __init__(self, config: Config):
        super().__init__(config)

    def _run(self) -> None:
        base_function = self._config.get_common_base_function()
        if base_function == Config.BASE_FUNCTION_TEXT_DIALOGUE:
            base = TextChatSample(self._config)
        elif base_function == Config.BASE_FUNCTION_VOICE_DIALOGUE:
            base = VoiceChatSample(self._config)
        elif base_function == Config.BASE_FUNCTION_AI_TUBER:
            base = AiTuberSample(self._config)
        else:
            raise ValueError(f"Invalid base_function: {base_function}")
        base.run_forever()

    def display(self):
        buttons_layout = [[
            sg.Button('設定', size=self.BUTTON_SIZE_NORMAL, key="settings"),
            sg.Button('起動', size=self.BUTTON_SIZE_NORMAL, key="run"),
            sg.Button('終了', size=self.BUTTON_SIZE_NORMAL, key="exit"),
        ]]

        window_layout = [
            [sg.Column(buttons_layout, justification='center')],
        ]

        # TODO:タイトルの設定ファイル化
        main_window = sg.Window("susumu_toolkit GUI", window_layout,
                                size=self.WINDOW_SIZE)

        while True:
            event, values = main_window.read()
            if event in (sg.WIN_CLOSED, 'exit'):
                break
            if event == "run":
                main_window.Hide()
                self._run()
                break
            if event == "settings":
                main_window.Hide()
                close_button_clicked = SettingsWindow(self._config).display()
                if close_button_clicked:
                    break
                main_window.UnHide()
        main_window.close()
