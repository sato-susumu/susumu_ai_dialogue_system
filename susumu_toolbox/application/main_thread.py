import threading
from enum import Enum
from typing import Optional

from event_channel.threaded_event_channel import ThreadedEventChannel

from susumu_toolbox.application.ai_tuber_framework import AiVTuberFramework
from susumu_toolbox.application.base_chat_framework import BaseChatFramework
from susumu_toolbox.application.text_chat_framework import TextChatFramework
from susumu_toolbox.application.voice_chat_framework import VoiceChatFramework
from susumu_toolbox.infrastructure.config import Config, BaseFunction


class MainThreadEvent(Enum):
    ON_START = "main_thread_start"
    ON_STOP = "main_thread_stop"


class MainThread:
    def __init__(self, config: Config):
        self.__config = config
        self.__thread = None
        self.__base: Optional[BaseChatFramework] = None
        self._event_channel = ThreadedEventChannel(blocking=False)
        self._is_running = False

    def event_subscribe(self, event_name: MainThreadEvent, func) -> None:
        self._event_channel.subscribe(event_name.value, func)

    def event_unsubscribe(self, event_name: MainThreadEvent, func) -> None:
        self._event_channel.unsubscribe(event_name.value, func)

    def start(self):
        if self.__thread:
            return
        self.__thread = threading.Thread(target=self.__run)
        self.__thread.start()

    def stop(self):
        if self.__thread is None:
            return
        self.__base.set_termination_flag()
        self.__thread.join()
        self.__base = None
        self.__thread = None
        self._event_channel.publish(MainThreadEvent.ON_STOP.value)
        self._is_running = False

    def update_config(self, config: Config):
        self.__config = config
        if self.__base:
            self.__base.update_config(config)

    def __run(self):
        current_ai_id = self.__config.get_ai_id_list()[0]
        system_settings = self.__config.get_ai_system_settings(current_ai_id)

        base_function = self.__config.get_common_base_function()
        if base_function == BaseFunction.TEXT_DIALOGUE:
            self.__base = TextChatFramework(self.__config, system_settings)
        elif base_function == BaseFunction.VOICE_DIALOGUE:
            self.__base = VoiceChatFramework(self.__config, system_settings)
        elif base_function == BaseFunction.AI_TUBER:
            self.__base = AiVTuberFramework(self.__config, system_settings)
        else:
            raise ValueError(f"Invalid base_function: {base_function}")
        self._event_channel.publish(MainThreadEvent.ON_START.value)
        self._is_running = True
        self.__base.run_forever()

    def is_running(self):
        return self._is_running
