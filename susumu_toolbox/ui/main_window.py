import os

import PySimpleGUI as Sg

from susumu_toolbox.application.ai_tuber_sample import AiTuberSample
from susumu_toolbox.application.text_chat_sample import TextChatSample
from susumu_toolbox.application.voice_chat_sample import VoiceChatSample
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_window import BaseWindow
from susumu_toolbox.ui.settings_window import SettingsWindow


# noinspection PyMethodMayBeStatic
class MainWindow(BaseWindow):
    def __init__(self, config: Config):
        super().__init__(config)

    def _run(self) -> None:
        current_ai_id = self._config.get_ai_id_list()[0]
        system_settings = self._config.get_ai_system_settings(current_ai_id)

        base_function = self._config.get_common_base_function_key()
        if base_function == Config.BASE_FUNCTION_TEXT_DIALOGUE:
            base = TextChatSample(self._config, system_settings)
        elif base_function == Config.BASE_FUNCTION_VOICE_DIALOGUE:
            base = VoiceChatSample(self._config, system_settings)
        elif base_function == Config.BASE_FUNCTION_AI_TUBER:
            base = AiTuberSample(self._config, system_settings)
        else:
            raise ValueError(f"Invalid base_function: {base_function}")
        base.run_forever()

    def _get_common_config_table(self) -> list:
        common_config_table = [
            ['ベース機能', self._config.get_common_base_function_name()],
            ['入力', self._config.get_common_input_function_name()],
            ['チャットエンジン', self._config.get_common_chat_function_name()],
            ['出力', self._config.get_common_output_function_name()],
            ['OBS出力', "有効" if self._config.get_common_obs_enabled() else "無効"],
        ]
        return common_config_table

    def display(self):
        buttons_layout = [[
            Sg.Button('設定', size=self.BUTTON_SIZE_NORMAL, key="settings"),
            Sg.Button('起動', size=self.BUTTON_SIZE_NORMAL, key="run"),
            Sg.Button('終了', size=self.BUTTON_SIZE_NORMAL, key="exit"),
        ]]

        header = ['機能名', '設定値']
        common_config_items = [
            [Sg.Table(self._get_common_config_table(),
                      headings=header,
                      hide_vertical_scroll=True,
                      col_widths=[20, 50],
                      justification='left',
                      auto_size_columns=False,
                      key="common_config_table",
                      )],
        ]
        window_layout = [
            [Sg.Frame("現在の設定", common_config_items, expand_x=True)],
            [Sg.Column(buttons_layout, justification='center')],
        ]

        main_window = Sg.Window(self._config.get_gui_app_title(),
                                window_layout,
                                size=self.WINDOW_SIZE,
                                finalize=True,
                                )
        path = self._config.get_current_config_path()
        if not os.path.exists(path):
            Sg.popup_ok("このアプリを使用するにはOpenAIのAPI Keyの設定が必要です。\nまずは、設定ボタンを押し、OpenAIのAPI Keyを設定してください。",
                        title="OpenAIのAPI Keyが設定されていません。")

        while True:
            event, values = main_window.read()
            if event in (Sg.WIN_CLOSED, 'exit'):
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
                _config_file_path = self._config.get_current_config_path()
                if os.path.exists(_config_file_path):
                    self._config.load(_config_file_path)
                main_window["common_config_table"].update(values=self._get_common_config_table())
                main_window.UnHide()
        main_window.close()
