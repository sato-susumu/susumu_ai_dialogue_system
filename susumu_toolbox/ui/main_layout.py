from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import PySimpleGUI as Sg
from loguru import logger

from susumu_toolbox.application.main_thread import MainThread, MainThreadEvent
from susumu_toolbox.infrastructure.config import Config
from susumu_toolbox.ui.base_layout import BaseLayout
from susumu_toolbox.ui.settings_layout import SettingsLayout

if TYPE_CHECKING:
    from susumu_toolbox.ui.main_window import MainWindow


# noinspection PyMethodMayBeStatic
class MainLayout(BaseLayout):
    KEY_MAIN_RUN = "key_main_run"
    KEY_MAIN_SETTINGS = "key_main_settings"

    def __init__(self, config: Config, main_window: MainWindow):
        super().__init__(config, main_window)
        self.__main_thread: Optional[MainThread] = None

    @classmethod
    def get_key(cls) -> str:
        return "main_layout"

    def __get_run_button_text(self) -> str:
        if self.__main_thread:
            return "停止"
        else:
            return "起動"

    def __settings_button_disabled(self) -> bool:
        return self.__main_thread is not None

    def __run_button_disabled(self) -> bool:
        if self.__main_thread is None:
            return False
        if self.__main_thread.is_running():
            return False
        return True

    def get_layout(self):
        from susumu_toolbox.ui.main_window import MainWindow

        buttons_layout = [[
            Sg.Button('設定', size=self.BUTTON_SIZE_NORMAL, key=self.KEY_MAIN_SETTINGS,
                      disabled=self.__settings_button_disabled()),
            Sg.Button(self.__get_run_button_text(), size=self.BUTTON_SIZE_NORMAL, key=self.KEY_MAIN_RUN),
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

    def update_elements(self) -> None:
        self._main_window.window["common_config_table"].update(values=self._get_common_config_table())
        self._main_window.window[self.KEY_MAIN_RUN].update(text=self.__get_run_button_text(),
                                                           disabled=self.__run_button_disabled())
        self._main_window.window[self.KEY_MAIN_SETTINGS].update(disabled=self.__settings_button_disabled())

    def update_config(self, config: Config) -> None:
        logger.info("設定内容の一部をリアルタイム反映")
        super().update_config(config)
        if self.__main_thread:
            self.__main_thread.update_config(config)

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
        self.__main_thread.event_subscribe(MainThreadEvent.ON_START, self._handle_main_thread_started)
        self.__main_thread.event_subscribe(MainThreadEvent.ON_STOP, self.__handle_main_thread_stopped)
        self.__main_thread.start()

    def __main_thread_stop(self) -> None:
        if self.__main_thread is None:
            return
        logger.debug("メインスレッド停止待ち")
        self.__main_thread.stop()
        self.__main_thread.event_unsubscribe(MainThreadEvent.ON_START, self._handle_main_thread_started)
        self.__main_thread.event_unsubscribe(MainThreadEvent.ON_STOP, self.__handle_main_thread_stopped)
        self.__main_thread = None

    def _handle_main_thread_started(self) -> None:
        logger.debug("メインスレッド起動完了")
        self._main_window.update_all_elements_in_window(self.get_key())

    def __handle_main_thread_stopped(self) -> None:
        logger.debug("メインスレッド停止完了")
        self._main_window.update_all_elements_in_window(self.get_key())

    def handle_event(self, event, values) -> None:
        match event:
            case self.KEY_MAIN_RUN:
                if self.__main_thread is None:
                    self.__main_thread_start()
                else:
                    self.__main_thread_stop()
                self._main_window.update_all_elements_in_window(self.get_key())
            case self.KEY_MAIN_SETTINGS:
                self._main_window.create_new_window(SettingsLayout.get_key())
