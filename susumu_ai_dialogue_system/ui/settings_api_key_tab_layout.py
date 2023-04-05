from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from susumu_ai_dialogue_system.ui.settings_layout import SettingsLayout
    from susumu_ai_dialogue_system.ui.main_window import MainWindow

import PySimpleGUI as Sg

from susumu_ai_dialogue_system.infrastructure.config import Config
from susumu_ai_dialogue_system.ui.base_layout import BaseLayout


# noinspection PyMethodMayBeStatic
class SettingsApiKeyTabLayout(BaseLayout):
    def __init__(self, config: Config, settings_layout: SettingsLayout, main_window: MainWindow):
        super().__init__(config, main_window)
        self._settings_layout = settings_layout

    @classmethod
    def get_key(cls) -> str:
        raise "settings_api_key_tab_layout"

    def get_layout(self):
        openai_items = [
            [Sg.Text("OpenAI API Key"),
             Sg.InputText(
                 default_text=self._config.get_openai_api_key(),
                 key=self._config.KEY_OPENAI_API_KEY,
                 password_char="*",
                 size=self.INPUT_SIZE_LONG,
             )],
            [Sg.Text("API KeyはOpenAIでユーザー登録後、"),
             self.create_linked_text("https://platform.openai.com/account/api-keys",
                                     "https://platform.openai.com/account/api-keys"),
             Sg.Text("で作成できます。")],
            [Sg.Text("API Keyは他の人に知られないようにご注意ください。")],
        ]
        deepl_items = [
            [Sg.Text('DEEPL APIキー',
                     ),
             Sg.InputText(
                 default_text=self._config.get_deepl_auth_key(),
                 key=self._config.KEY_DEEPL_AUTH_KEY,
                 password_char="*",
                 size=self.INPUT_SIZE_LONG,
             )],
        ]

        api_keys_tab_layout = [
            [Sg.Frame("OpenAI", openai_items, expand_x=True)],
            [Sg.Frame("DeepL", deepl_items, expand_x=True, visible=False)],
        ]
        return api_keys_tab_layout

    def update_elements(self) -> None:
        pass

    def handle_event(self, event, values) -> None:
        pass
