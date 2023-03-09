import os

# noinspection PyPep8Naming
import PySimpleGUI as sg

from gui_config import GuiConfig
from samples.chatgpt_text_chat_sample import ChatGPTTextChatSample
from susumu_toolbox.utility.config import Config


# noinspection PyMethodMayBeStatic
class GUI:
    _GUI_TITLE = "susumu_toolkit GUI"
    _OPEN_AI_API_KEY = "open_ai_api_key"

    def __init__(self):
        self._gui_config = GuiConfig()

    def _load(self) -> None:
        self._gui_config.load()

    def _save(self, values: dict) -> None:
        self._gui_config.open_ai_api_key = values[self._OPEN_AI_API_KEY]
        self._gui_config.save()

    def _get_sample_config(self) -> Config:
        config = Config()
        file_path = os.path.join(config.get_config_dir(), "sample_config.yaml")
        config.load_config(file_path)
        return config

    def _run(self) -> None:
        config = self._get_sample_config()
        config.set_openai_api_key(self._gui_config.open_ai_api_key)
        ChatGPTTextChatSample(config).run_forever()

    def execute(self) -> None:
        self._load()
        self._display()

    def _display(self) -> None:
        sg.theme('Bright Colors')

        setting_items = [
            [sg.Text("OpenAI APIキー"), sg.InputText(self._gui_config.open_ai_api_key,
                                                   size=(100, 1),
                                                   password_char="*",
                                                   key=self._OPEN_AI_API_KEY)],
            # [sg.Button("高度な設定")],
            [sg.Button("設定保存", key="save")],
        ]

        # noinspection PyTypeChecker
        setting_frame = [[sg.Frame("設定", setting_items,
                                   title_location=sg.TITLE_LOCATION_TOP_LEFT,
                                   )]]

        layout = [setting_frame,
                  [sg.Button("起動", key="run")],
                  [sg.Button("終了", key="exit")],
                  ]

        window = sg.Window('susumu_toolkit GUI', layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'exit'):
                break
            if event == 'run':
                self._run()
            if event == 'save':
                self._save(values)

        window.close()


if __name__ == "__main__":
    GUI().execute()
