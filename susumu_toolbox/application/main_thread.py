import threading

from susumu_toolbox.application.ai_tuber_framework import AiVTuberFramework
from susumu_toolbox.application.text_chat_framework import TextChatFramework
from susumu_toolbox.application.voice_chat_framework import VoiceChatFramework
from susumu_toolbox.infrastructure.config import Config, BaseFunction


class MainThread:
    def __init__(self, config: Config):
        self.__config = config
        self.__thread = None

    def start(self):
        self.__thread = threading.Thread(target=self.__run)
        self.__thread.start()

    def __run(self):
        current_ai_id = self.__config.get_ai_id_list()[0]
        system_settings = self.__config.get_ai_system_settings(current_ai_id)

        base_function = self.__config.get_common_base_function()
        if base_function == BaseFunction.TEXT_DIALOGUE:
            base = TextChatFramework(self.__config, system_settings)
        elif base_function == BaseFunction.VOICE_DIALOGUE:
            base = VoiceChatFramework(self.__config, system_settings)
        elif base_function == BaseFunction.AI_TUBER:
            base = AiVTuberFramework(self.__config, system_settings)
        else:
            raise ValueError(f"Invalid base_function: {base_function}")
        base.run_forever()

    def stop(self):
        self.__thread.join()
