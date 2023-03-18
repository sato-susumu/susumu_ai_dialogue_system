import os

from samples.base_text_chat_sample import BaseTextChatSample
from samples.gui.gui_function_factory import GuiFunctionFactory
from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.chat.chatgpt_chat import ChatGPTChat
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.system_setting import SystemSettings


# noinspection PyMethodMayBeStatic,DuplicatedCode
class GuiTextChatSample(BaseTextChatSample):
    def __init__(self, config: Config):
        super().__init__(config)

    def create_chat(self) -> BaseChat:
        # TODO: ParlAIとの切り替え
        system = SystemSettings(self._config)
        path = os.path.join(system.get_config_dir(), "sample_system_settings.txt")
        system.load_settings(path)
        return ChatGPTChat(self._config, system.get_system_settings())

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        stt = GuiFunctionFactory.create_stt(self._config, speech_contexts)
        print("stt:", stt)
        return stt

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator(self._config)

    def create_tts(self) -> BaseTTS:
        tts = GuiFunctionFactory.create_tts(self._config)
        print("tts:", tts)
        return tts


if __name__ == "__main__":
    _config = Config()
    _config.load()
    GuiTextChatSample(_config).run_forever()
