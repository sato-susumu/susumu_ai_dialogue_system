import PySimpleGUI as sg

from susumu_toolbox.sample.gui.base_window import BaseWindow
# noinspection PyMethodMayBeStatic
from susumu_toolbox.utility.config import Config


class WelcomeWindow(BaseWindow):
    def __init__(self, config: Config):
        super().__init__(config)

    def display(self) -> bool:
        buttons_layout = [
            [
                sg.Button("OK", size=(15, 1), key="ok"),
            ],
        ]

        window_layout = [
            [sg.Text("このアプリを使用するにはOpenAIのAPI Keyが必要です。")],
            [sg.Text("まずは、設定ボタンを押し、OpenAIのAPI Keyを設定してください。")],
            [sg.Column(buttons_layout, justification='center')],
        ]

        welcome_window = sg.Window("初期画面", window_layout,
                                   size=self.WINDOW_SIZE,
                                   # modal=True,
                                   )

        while True:
            event, values = welcome_window.read()
            if event == sg.WIN_CLOSED:
                close_button_clicked = True
                break
            if event == "ok":
                close_button_clicked = False
                break

        welcome_window.close()
        return close_button_clicked
