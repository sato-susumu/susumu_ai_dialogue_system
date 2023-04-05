import os

import PySimpleGUI as Sg

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.main_layout import MainLayout
from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout


# noinspection PyMethodMayBeStatic
class MainWindow:
    __WINDOW_SIZE = (800, 600)
    KEY_WINDOW_EXIT = "key_window_exit"

    def __init__(self, config: Config):
        self.window = None
        self.__config = config
        self.__layout_list = [MainLayout(config, self), SettingsLayout(config, self)]

    def create_new_window(self, target_layout_name: str) -> None:
        # 例えば、設定画面のキャンセルボタンを押した場合、作成済みの各Elementを初期化するか、全Elementを再作成したい。
        # しかし、ウィンドウを維持したまま簡単に行う手段がない。
        # そのため、ウィンドウから再作成することで、全Elementを初期化する。

        Sg.theme(self.__config.get_gui_theme_name())
        window_layout = [
            [Sg.Column(layout.get_layout(), visible=False, key=layout.get_key()) for layout in self.__layout_list]]

        window_params = {
            'title': self.__config.get_gui_app_title(),
            'layout': window_layout,
            'size': self.__WINDOW_SIZE,
            'finalize': True
        }

        if self.window:
            window_params['location'] = self.window.current_location()

        new_window = Sg.Window(**window_params)

        for layout in self.__layout_list:
            new_window[layout.get_key()].update(visible=False)
        new_window[target_layout_name].update(visible=True)

        if self.window:
            self.window.close()
        self.window = new_window

        # 別に呼ばなくてもいいが、呼ばないと不具合に気付きにくくなるので呼んでおく
        self.update_all_elements_in_window(target_layout_name)

    def update_all_elements_in_window(self, target_layout_name: str) -> None:
        for layout in self.__layout_list:
            if layout.get_key() == target_layout_name:
                layout.update_elements()

    def update_config(self) -> None:
        config_file_path = self.__config.get_current_config_path()
        if os.path.exists(config_file_path):
            self.__config.load(config_file_path)
        for layout in self.__layout_list:
            layout.update_config(self.__config)

    def input_validation_number_only(self, event, values):
        if values[event] and values[event][-1] not in '0123456789':
            self.window[event].update(values[event][:-1])

    def display(self):
        self.create_new_window(MainLayout.get_key())

        path = self.__config.get_current_config_path()
        if not os.path.exists(path):
            Sg.popup_ok("このアプリを使用するにはOpenAIのAPI Keyの設定が必要です。\nまずは、設定ボタンを押し、OpenAIのAPI Keyを設定してください。",
                        title="OpenAIのAPI Keyが設定されていません。")

        while True:
            event, values = self.window.read()
            if event in (Sg.WIN_CLOSED, self.KEY_WINDOW_EXIT):
                break
            for layout in self.__layout_list:
                layout.handle_event(event, values)
        self.window.close()
        self.window = None
