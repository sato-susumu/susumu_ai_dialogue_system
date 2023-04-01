import PySimpleGUI as Sg
from PySimpleGUI import Window

from susumu_toolbox.application.main_thread import MainThread
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_layout import BaseLayout
from susumu_toolbox.ui.settings_layout import SettingsLayout


# noinspection PyMethodMayBeStatic
class MainLayout(BaseLayout):
    KEY_MAIN_RUN = "key_main_run"
    KEY_MAIN_SETTINGS = "key_main_settings"

    def __init__(self, config: Config):
        super().__init__(config)
        self.__main_thread = None

    @classmethod
    def get_key(cls) -> str:
        return "main_layout"

    def __get_run_button_label(self) -> str:
        if self.__main_thread:
            return "停止"
        else:
            return "起動"

    def get_layout(self):
        from susumu_toolbox.ui.main_window import MainWindow

        buttons_layout = [[
            Sg.Button('設定', size=self.BUTTON_SIZE_NORMAL, key=self.KEY_MAIN_SETTINGS),
            Sg.Button(self.__get_run_button_label(), size=self.BUTTON_SIZE_NORMAL, key=self.KEY_MAIN_RUN),
            Sg.Button('終了', size=self.BUTTON_SIZE_NORMAL, key=MainWindow.KEY_WINDOW_EXIT),
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
        return window_layout

    def update_layout(self, window: Window) -> None:
        window["common_config_table"].update(values=self._get_common_config_table())
        window[self.KEY_MAIN_RUN].update(self.__get_run_button_label())

    def _get_common_config_table(self) -> list:
        common_config_table = [
            ['ベース機能', self._config.get_common_base_function_name()],
            ['入力', self._config.get_common_input_function_name()],
            ['チャットエンジン', self._config.get_common_chat_function_name()],
            ['出力', self._config.get_common_output_function_name()],
            ['OBS出力', "有効" if self._config.get_common_obs_enabled() else "無効"],
            ['感情解析とVMagicMirror連携',
             "有効" if self._config.get_common_v_magic_mirror_connection_enabled() else "無効"],
        ]
        return common_config_table

    def __main_thread_start(self) -> None:
        if self.__main_thread:
            return
        self.__main_thread = MainThread(self._config)
        self.__main_thread.start()

    def __main_thread_stop(self) -> None:
        if self.__main_thread is None:
            return
        self.__main_thread.stop()
        self.__main_thread = None

    def handle_event(self, event, values, main_window) -> None:
        match event:
            case self.KEY_MAIN_RUN:
                # main_window.window.Hide()
                if self.__main_thread is None:
                    self.__main_thread_start()
                else:
                    self.__main_thread_stop()
                main_window.update_layout(self.get_key())
            case self.KEY_MAIN_SETTINGS:
                main_window.change_layout(SettingsLayout.get_key())
