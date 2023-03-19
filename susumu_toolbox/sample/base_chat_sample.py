import os

from susumu_toolbox.chat.base_chat import BaseChat
from susumu_toolbox.sample.common.function_factory import FunctionFactory
from susumu_toolbox.stt.base_stt import BaseSTT
from susumu_toolbox.translation.base_translator import BaseTranslator
from susumu_toolbox.translation.dummy_translator import DummyTranslator
from susumu_toolbox.tts.base_tts import BaseTTS
from susumu_toolbox.utility.config import Config
from susumu_toolbox.utility.system_setting import SystemSettings


# noinspection PyMethodMayBeStatic,DuplicatedCode
class BaseChatSample:
    def __init__(self, config: Config):
        self._config = config

    def create_chat(self) -> BaseChat:
        system = SystemSettings(self._config)
        path = os.path.join(system.get_config_dir(), "sample_system_settings.txt")
        system.load_settings(path)
        chat = FunctionFactory.create_chat(self._config, system)
        print("chat:", chat)
        return chat

    def create_stt(self, speech_contexts=None) -> BaseSTT:
        stt = FunctionFactory.create_stt(self._config, speech_contexts)
        print("stt:", stt)
        return stt

    def create_translator(self) -> BaseTranslator:
        return DummyTranslator(self._config)

    def create_tts(self) -> BaseTTS:
        tts = FunctionFactory.create_tts(self._config)
        print("tts:", tts)
        return tts

    def create_obs_client(self):
        obs = FunctionFactory.create_obs_client(self._config)
        print("obs:", obs)
        return obs
