import time

import openai
from loguru import logger

from susumu_ai_dialogue_system.infrastructure.chat.base_chat import BaseChat, ChatResult, ChatEvent
from susumu_ai_dialogue_system.infrastructure.config import Config


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyShadowingNames
class ChatGPTChat(BaseChat):
    def __init__(self, config: Config):
        super().__init__(config)
        openai.api_key = config.get_openai_api_key()
        self._messages = []
        current_ai_id = config.get_ai_id_list()[0]
        system_settings = config.get_ai_system_settings(current_ai_id)
        system_settings_text = system_settings.get_text()
        if len(system_settings_text) != 0:
            self._append_message("system", system_settings_text)

    def _append_message(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})

    def _create_prompt(self):
        if len(self._messages) < 20:
            return self._messages
        return self._messages[0:1] + self._messages[-19:]

    def send_message(self, text: str) -> None:
        self._append_message("user", text)

        before = time.perf_counter()
        try:
            messages = self._create_prompt()
            if self._config.get_advanced_chat_gpt_history_log_enabled():
                logger.debug(f"ChatGPT history={messages}")
            result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
        except openai.error.RateLimitError as e:
            logger.debug("RateLimitError: OpenAI APIのリクエスト制限に達しました。")
            self._event_publish(ChatEvent.MESSAGE, ChatResult("", []))
            self._event_publish(ChatEvent.ERROR, e)
            raise

        after = time.perf_counter()
        logger.debug(f"ChatGPT processing time={after - before:.3f} s")

        usage = result.usage
        logger.debug(f"prompt_tokens={usage.prompt_tokens} "
                     f"completion_tokens={usage.completion_tokens} "
                     f"total_tokens={usage.total_tokens}")

        result_text = result.choices[0].message.content
        self._append_message("assistant", result_text)

        self._event_publish(ChatEvent.MESSAGE, ChatResult(result_text, []))
