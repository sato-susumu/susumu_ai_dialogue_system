import PySimpleGUI as sg

from susumu_toolbox.sample.ai_tuber_sample import AiTuberSample
from susumu_toolbox.sample.gui.base_window import BaseWindow
from susumu_toolbox.sample.gui.settings_window import SettingsWindow
from susumu_toolbox.sample.text_chat_sample import TextChatSample
from susumu_toolbox.sample.voice_chat_sample import VoiceChatSample
from susumu_toolbox.utility.config import Config
# noinspection PyMethodMayBeStatic
from susumu_toolbox.utility.system_setting import SystemSettings


class MainWindow(BaseWindow):
    def __init__(self, config: Config):
        super().__init__(config)

    def _run(self) -> None:
        base_function = self._config.get_common_base_function()
        system_settings = SystemSettings(self._config)
        if base_function == Config.BASE_FUNCTION_TEXT_DIALOGUE:
            base = TextChatSample(self._config, system_settings)
        elif base_function == Config.BASE_FUNCTION_VOICE_DIALOGUE:
            base = VoiceChatSample(self._config, system_settings)
        elif base_function == Config.BASE_FUNCTION_AI_TUBER:
            base = AiTuberSample(self._config, system_settings)
        else:
            raise ValueError(f"Invalid base_function: {base_function}")
        base.run_forever()

    def display(self):
        # TODO:ボタン以外にも表示
        buttons_layout = [[
            sg.Button('設定', size=self.BUTTON_SIZE_NORMAL, key="settings"),
            sg.Button('起動', size=self.BUTTON_SIZE_NORMAL, key="run"),
            sg.Button('終了', size=self.BUTTON_SIZE_NORMAL, key="exit"),
        ]]

        window_layout = [
            [sg.Column(buttons_layout, justification='center')],
        ]

        # TODO:(低)タイトルの設定ファイル化
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
