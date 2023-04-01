import os

import PySimpleGUI as Sg

from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.main_layout import MainLayout
from susumu_toolbox.ui.settings_layout import SettingsLayout


# noinspection PyMethodMayBeStatic
class MainWindow:
    __WINDOW_SIZE = (800, 600)
    KEY_WINDOW_EXIT = "key_window_exit"

    def __init__(self, config: Config):
        self.window = None
        self.__config = config
        self.__layout_list = [MainLayout(config), SettingsLayout(config)]

    def change_layout(self, target_layout_name: str) -> None:
        for layout in self.__layout_list:
            self.window[layout.get_key()].update(visible=False)

        self.window[target_layout_name].update(visible=True)
        self.update_layout(target_layout_name)

    def update_layout(self, target_layout_name: str) -> None:
        for layout in self.__layout_list:
            if layout.get_key() == target_layout_name:
                layout.update_layout(self.window)

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
        window_layout = [[Sg.Column(layout.get_layout(), visible=False, key=layout.get_key())
                          for layout in self.__layout_list]]
        self.window = Sg.Window(title=self.__config.get_gui_app_title(),
                                layout=window_layout,
                                size=self.__WINDOW_SIZE,
                                finalize=True,
                                )
        self.change_layout(MainLayout.get_key())

        path = self.__config.get_current_config_path()
        if not os.path.exists(path):
            Sg.popup_ok("このアプリを使用するにはOpenAIのAPI Keyの設定が必要です。\nまずは、設定ボタンを押し、OpenAIのAPI Keyを設定してください。",
                        title="OpenAIのAPI Keyが設定されていません。")

        while True:
            event, values = self.window.read()
            for layout in self.__layout_list:
                layout.handle_event(event, values, self)
            if event in (Sg.WIN_CLOSED, self.KEY_WINDOW_EXIT):
                break
        self.window.close()
