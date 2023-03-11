import openai

from susumu_toolbox.chat.base_chat import BaseChat, ChatResult
from susumu_toolbox.utility.config import Config


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyShadowingNames
class ChatGPTChat(BaseChat):
    def __init__(self, config: Config, system_settings: str = ""):
        super().__init__(config)
        openai.api_key = config.get_openai_api_key()
        self._system_settings = system_settings
        self._messages = []
        if len(self._system_settings) != 0:
            self._append_message("system", self._system_settings)

    def _append_message(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})

    def send_message(self, text: str) -> None:
        self._append_message("user", text)

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages
        )
        result_text = result.choices[0].message.content
        self._append_message("assistant", result_text)

        self._event_channel.publish(self.EVENT_CHAT_MESSAGE, ChatResult(result_text, []))
