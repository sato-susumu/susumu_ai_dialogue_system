import json
import time

import openai
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain.schema import messages_to_dict
from loguru import logger

from susumu_ai_dialogue_system.application.common.langchain_parts_factory import LangChainPartsFactory
from susumu_ai_dialogue_system.infrastructure.chat.base_chat import BaseChat, ChatResult, ChatEvent
from susumu_ai_dialogue_system.infrastructure.config import Config


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyShadowingNames
class LangChainChat(BaseChat):
    def __init__(self, config: Config):
        super().__init__(config)
        openai.api_key = config.get_openai_api_key()

        chat = ChatOpenAI(temperature=0)

        self._conv_buffer_window_memory = LangChainPartsFactory.create_memory(config)
        logger.debug(f"memory: {type(self._conv_buffer_window_memory).__name__}")

        current_ai_id = config.get_ai_id_list()[0]
        system_settings = config.get_ai_system_settings(current_ai_id)
        template = system_settings.get_text()

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        self._conversation = ConversationChain(
            llm=chat,
            memory=self._conv_buffer_window_memory,
            prompt=prompt,
            verbose=self._config.get_langchain_conversation_verbose(),
        )

    def send_message(self, text: str) -> None:
        before = time.perf_counter()

        messages = self._conversation.predict(input=text)
        # history = self._conv_buffer_window_memory.chat_memory
        # messages_dict = json.dumps(messages_to_dict(history.messages), indent=2, ensure_ascii=False)
        # print(f"memory: {messages_dict}")

        after = time.perf_counter()
        logger.debug(f"LangChain conversation processing time={after - before:.3f} s")

        self._event_publish(ChatEvent.MESSAGE, ChatResult(messages, []))
